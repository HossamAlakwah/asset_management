import io
from datetime import date
from itertools import count
from turtle import Screen
from urllib.parse import unquote, urlparse

import pandas as pd
import xlsxwriter
from django.apps import apps
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Count, Prefetch, Q, Sum
from django.forms import inlineformset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .download_templates import (
    generate_asset_template,
    generate_camera_template,
    generate_screen_template,
)
from .extract_date import (
    generate_assets_report,
    generate_cameras_report,
    generate_screens_report,
)
from .models import (
    NVR,
    Asset,
    AssetLog,
    Branch,
    Camera,
    CameraLog,
    Employee,
    ReportableField,
    ReportableModel,
    Screen,
    ScreenLog,
    StorageDevice,
)
from .upload_data import (
    upload_bulk_asset,
    upload_bulk_cameras,
    upload_bulk_employee,
    upload_bulk_screens,
)


def logout_view(request):
    # Log out the user
    logout(request)

    # Clear session
    request.session.flush()

    # Prepare response with redirect
    response = redirect('/')

    # Optional: delete sessionid and csrftoken cookies
    response.delete_cookie('sessionid')
    response.delete_cookie('csrftoken')

    return response

@login_required
def branches_view(request):
    branches = Branch.objects.all().order_by('id')
    return render(request, 'branches.html', {'branches': branches})

@login_required
def view_branch(request, slug):
    branch = get_object_or_404(Branch, slug=slug)
    return render(request, 'branch_detail.html', {'branch': branch})

@login_required
def view_all(request):
    return render(request, 'all.html')


''' 

employee view and create employee
This view allows users to create a new employee and assign an asset if available.

'''
def employees_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        department = request.POST.get('department')
        title = request.POST.get('title')
        email = request.POST.get('email')
        asset_id = request.POST.get('assigned_asset')

        employee = Employee.objects.create(
            name=name,
            department=department,
            title=title,
            email=email,
            created_by=request.user
        )

        if asset_id:
            try:
                asset = Asset.objects.get(pk=asset_id)
                asset.employee_name = employee
                asset.status = 'In Use'
                asset.save()
            except Asset.DoesNotExist:
                pass

        return redirect('employees')

    employees = Employee.objects.all()
    assets = Asset.objects.filter(status='Stock', employee_name__isnull=True)
    return render(request, 'employees/employees.html', {
        'employees': employees,
        'assets': assets,
    })

@login_required
def create_employee(request):
    assets = Asset.objects.filter(status='Stock')  # Only unassigned assets
    branches = Branch.objects.filter(choosable=True)
    if request.method == 'POST':
        name = request.POST.get('name')
        department = request.POST.get('department')
        title = request.POST.get('title')
        email = request.POST.get('email')
        branch=request.POST.get('branch')
        branch = Branch.objects.filter(id=branch).first() 
        assigned_asset_id = request.POST.get('assigned_asset')

        if not all([name, department, title, email]):
            messages.error(request, "All fields are required.")
            return redirect('create_employee')

        try:
            with transaction.atomic():
                employee = Employee.objects.create(
                    name=name,
                    department=department,
                    title=title,
                    email=email,
                    branch=branch,
                    created_by=request.user
                )

            if assigned_asset_id:
                # Check if already assigned (avoid duplicates)
                already_assigned = employee.asset_set.filter(id=assigned_asset_id).exists()
                if not already_assigned:
                    asset = Asset.objects.get(pk=assigned_asset_id)
                    asset.employee_name = employee
                    asset.status = 'In Use'
                    asset.branch = employee.branch
                    asset.on_hand_date = timezone.now().date()
                    asset._changed_by = request.user
                    asset.save()


                messages.success(request, f"Employee '{employee.name}' created successfully.")
                return redirect('all_assets')

        except Exception as e:
            messages.error(request, f"Error: {e}")

    return render(request, 'employees/create_employee.html', {
        'assets': assets,
        'branches': branches,  # Pass branches to the template
    })


from django.views.decorators.clickjacking import xframe_options_exempt


@login_required
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    assets = Asset.objects.filter(status='Stock').exclude(employee_name__isnull=False)
    screens = Screen.objects.filter(status='Stock').exclude(employee__isnull=False)
    branches = Branch.objects.filter(choosable=True)

    if request.method == 'POST':
        name = request.POST.get('name')
        department = request.POST.get('department')
        title = request.POST.get('title')
        email = request.POST.get('email')
        branch_id = request.POST.get('branch')
        assigned_asset_id = request.POST.get('assigned_asset')
        assigned_screen_id = request.POST.get('assigned_screen')  # New

        if not all([name, department, title, email]):
            messages.error(request, "All fields are required.")
            return redirect('edit_employee', employee_id=employee.id)

        try:
            with transaction.atomic():
                employee.name = name
                employee.department = department
                employee.title = title
                employee.email = email
                employee.branch = Branch.objects.filter(id=branch_id).first()
                employee.save()

                # Assign Asset if selected
                if assigned_asset_id:
                    already_assigned = employee.asset_set.filter(id=assigned_asset_id).exists()
                    if not already_assigned:
                        asset = Asset.objects.get(pk=assigned_asset_id)
                        asset.employee_name = employee
                        asset.status = 'In Use'
                        asset.branch = employee.branch
                        asset.on_hand_date = timezone.now().date()
                        asset._changed_by = request.user
                        asset.save()

                # Assign Screen if selected
                if assigned_screen_id:
                    screen = Screen.objects.get(pk=assigned_screen_id)
                    screen.employee = employee
                    screen.status = 'In Use'
                    screen.branch = employee.branch
                    screen._changed_by = request.user
                    screen.save()

                messages.success(request, f"Employee '{employee.name}' updated successfully.")
                return redirect('edit_employee', employee_id=employee.id)

        except Exception as e:
            messages.error(request, f"Error: {e}")

    return render(request, 'employees/edit_employee.html', {
        'employee': employee,
        'assets': assets,
        'screens': screens,  
        'branches': branches,
        # 'assigned_screens': assigned_screens,
    })




@require_POST
@login_required
def unassign_asset(request, asset_id, employee_id):
    asset = get_object_or_404(Asset, id=asset_id, employee_name__id=employee_id)
    stock_branch = Branch.objects.get(name__iexact='Stock')

    try:
        asset.employee_name = None
        asset.status = 'Stock'
        asset.branch = stock_branch
        asset.return_date = timezone.now().date()
        asset._changed_by = request.user
        asset.save()

        messages.success(request, f"Asset '{asset.serial}' unassigned successfully.")
    except Exception as e:
        messages.error(request, f"Error while unassigning asset: {e}")

    return redirect('edit_employee', employee_id=employee_id)

@login_required
def all_assets(request):
    assets = Asset.objects.all()
    all_count = assets.count()
    laptops_total = assets.filter(type='Laptop').count()
    PCs_total = assets.filter(type='Desktop').count()
    unique_asset_types = list(
        assets.order_by('status').values_list('status', flat=True).distinct()
    )
    print(unique_asset_types)
    stock_count = assets.filter(status='Stock').count()
    in_use_count = assets.filter(status='In Use').count()
    damage_count = assets.filter(status='Damage').count()
    
    context = {
        'branch': None,
        'assets': assets,
        'all': all_count,
        'laptops_total': laptops_total,
        'PCs_total': PCs_total,
        "unique_asset_types": unique_asset_types,
        "stock_count": stock_count,
        "in_use_count": in_use_count,
        "damage_count": damage_count,
    }
    return render(request, 'assets/assets_all.html', context)



@login_required
def download_asset_template(request):
    return generate_asset_template()

def all_assets_log(request, slug):
    if slug == 'All':
        logs = AssetLog.objects.all().order_by('-change_time')
        context = {
            'logs': logs,
            'branch': None,
            'current_branch_slug': 'All',
        }
    else:
        branch = get_object_or_404(Branch, slug=slug)
        print(branch)
        asset_ids = Asset.objects.filter(branch=branch).values_list('id', flat=True)
        logs = AssetLog.objects.filter(asset_id__in=asset_ids).order_by('-change_time')

        context = {
            'logs': logs,
            'branch': branch,
            'current_branch_slug': branch.slug,
        }

    return render(request, 'assets/assets_logs.html', context)


@login_required
def branch_assets(request, slug):
    branch = get_object_or_404(Branch, slug=slug)
    assets = Asset.objects.filter(branch=branch)
    all_assets_count = assets.count()
    laptops_total = assets.filter(type='Laptop').count()
    PCs_total = assets.filter(type='Desktop').count()

    # Get unique asset types for the dropdown filter
    unique_asset_types = list(
        assets.order_by('type').values_list('type', flat=True).distinct()
    )

    logs = []

    context = {
        'assets': assets,
        'all': all_assets_count,
        'laptops_total': laptops_total,
        'PCs_total': PCs_total,
        'unique_asset_types': unique_asset_types,
        'logs': logs,
        'current_branch_slug': slug, 
    }
    return render(request, 'assets/branch_assets.html', context)

'''

upload bulk asset data from excel file 
laptops and PCs

'''

@require_POST 
@login_required
def upload_assets(request, slug):
    branch = get_object_or_404(Branch, slug=slug)
    if 'excel_file' in request.FILES:
        excel_file = request.FILES['excel_file']

        success = upload_bulk_asset(request, excel_file, branch, slug, request.user)

        if not success:
            if slug!='All':
                return redirect('branch_assets', slug=slug)
            else:
                return redirect('all_assets')

    else:
        messages.error(request, "No Excel file was uploaded.")

    if slug!='All':
        return redirect('branch_assets', slug=slug)
    else:
        return redirect('all_assets')

@login_required
def extract_assets_data(request, slug):
    branch = get_object_or_404(Branch, slug=slug)
    

    selected_status = request.POST.get('status') 
    selected_format = request.POST.get('format') 

    # Call the helper function to generate the report
    response = generate_assets_report(request, branch, selected_status, selected_format)

    if not response:
        return redirect('branch_assets', slug=slug)

    return response

@xframe_options_exempt
def asset_details(request, asset_id):
    asset = get_object_or_404(Asset, pk=asset_id)
    print(asset)
    return render(request, 'assets/asset_details.html', {'asset': asset})




def laptop_acknowledgment(request):
    return render(request, 'assets/test.html')




@login_required
def edit_asset(request, asset_id):
    asset = get_object_or_404(Asset, pk=asset_id)
    branches = Branch.objects.filter(choosable=True)
    employees = Employee.objects.all()

    if request.method == 'POST':
        # Fetch form fields
        product = request.POST.get('product')
        serial = request.POST.get('serial')
        status = request.POST.get('status')
        asset_type = request.POST.get('type')
        comments = request.POST.get('comments')
        branch_id = request.POST.get('branch')
        employee_id = request.POST.get('employee_name')

        warranty_str = request.POST.get('warranty')
        on_hand_date_str = request.POST.get('on_hand_date')
        return_date_str = request.POST.get('return_date')
        cpu = request.POST.get('cpu')
        cpu_gen = request.POST.get('cpu_generation')
        ram = request.POST.get('ram')

        # Validation
        missing_fields = []
        if not product: missing_fields.append("Product")
        if not serial: missing_fields.append("Serial")
        if not status: missing_fields.append("Status")
        if not asset_type: missing_fields.append("Asset Type")

        if missing_fields:
            messages.error(request, f"Please fill in: {', '.join(missing_fields)}")
            return render(request, 'assets/asset_edit.html', {
                'asset': asset,
                'branches': branches,
                'employees': employees,
                'cpu_choices': Asset.CPU_CHOICES,
                'cpu_gen_choices': Asset.CPU_GEN_CHOICES,
                'ram_choices': Asset.RAM_CHOICES,
            })

        # Parse dates
        try:
            warranty = timezone.datetime.strptime(warranty_str, '%Y-%m-%d').date() if warranty_str else None
            on_hand_date = timezone.datetime.strptime(on_hand_date_str, '%Y-%m-%d').date() if on_hand_date_str else None
            return_date = timezone.datetime.strptime(return_date_str, '%Y-%m-%d').date() if return_date_str else None
        except ValueError:
            messages.error(request, "Invalid date format.")
            return render(request, 'assets/asset_edit.html', {
                'asset': asset,
                'branches': branches,
                'employees': employees,
                'cpu_choices': Asset.CPU_CHOICES,
                'cpu_gen_choices': Asset.CPU_GEN_CHOICES,
                'ram_choices': Asset.RAM_CHOICES,
            })

        # Status rules
        if status == 'In Use' and not on_hand_date:
            messages.error(request, "On-Hand Date is required when status is 'In Use'.")
            return render(request, 'assets/asset_edit.html', {
                'asset': asset,
                'branches': branches,
                'employees': employees,
                'cpu_choices': Asset.CPU_CHOICES,
                'cpu_gen_choices': Asset.CPU_GEN_CHOICES,
                'ram_choices': Asset.RAM_CHOICES,
            })

        if asset.status in ['In Use', 'Damage'] and status == 'Stock' and not return_date:
            messages.error(request, "Return Date is required when returning to Stock.")
            return render(request, 'assets/asset_edit.html', {
                'asset': asset,
                'branches': branches,
                'employees': employees,
                'cpu_choices': Asset.CPU_CHOICES,
                'cpu_gen_choices': Asset.CPU_GEN_CHOICES,
                'ram_choices': Asset.RAM_CHOICES,
            })

        # Get related objects
        try:
            branch = Branch.objects.get(pk=branch_id)
        except Branch.DoesNotExist:
            messages.error(request, "Selected branch does not exist.")
            return render(request, 'assets/asset_edit.html', {
                'asset': asset,
                'branches': branches,
                'employees': employees,
                'cpu_choices': Asset.CPU_CHOICES,
                'cpu_gen_choices': Asset.CPU_GEN_CHOICES,
                'ram_choices': Asset.RAM_CHOICES,
            })
        print(employee_id)
        employee = Employee.objects.get(pk=employee_id) if employee_id else None

        # Final update
        asset.product = product
        asset.serial = serial
        asset.status = status
        asset.type = asset_type
        asset.branch = branch
        asset.comments = comments
        asset.warranty = warranty
        asset.on_hand_date = on_hand_date if status == 'In Use' else None
        asset.return_date = return_date if status in ['Stock', 'Damage'] else None
        asset.employee_name = employee if status == 'In Use' else None
        asset.cpu = cpu
        asset.cpu_generation = cpu_gen
        asset.ram = ram
        asset._changed_by = request.user

        with transaction.atomic():
            asset.save()


        messages.success(request, "Asset updated successfully.")
        return redirect('edit_asset', asset_id=asset.pk)

    return render(request, 'assets/asset_edit.html', {
        'asset': asset,
        'branches': branches,
        'employees': employees,
        'cpu_choices': Asset.CPU_CHOICES,
        'cpu_gen_choices': Asset.CPU_GEN_CHOICES,
        'ram_choices': Asset.RAM_CHOICES,
    })


from .forms import (
    AssetForm,
    CameraEditForm,
    CameraForm,
    ScreenForm,
    StorageDeviceFormSet,
)


@login_required
def add_asset(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        formset = StorageDeviceFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            asset = form.save(commit=False)
            asset.created_by = request.user
            asset.status = 'Stock'
            asset.branch = Branch.objects.get(slug='stock')
            asset._changed_by = request.user
            asset.save()

            storage_devices = formset.save(commit=False)
            for device in storage_devices:
                device.asset = asset
                device.save()
            formset.save_m2m()

            messages.success(request, 'Asset added successfully.')
            return redirect('all_assets')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AssetForm()
        formset = StorageDeviceFormSet() 

    return render(request, 'assets/asset_create.html', {
        'form': form,
        'formset': formset,  
    })

##############################################################################    


'''
Create dynamic report view
This view allows users to select a model and apply filters to generate a report.
'''



def dynamic_report_view(request):
    report_model_id = request.GET.get("model")
    filters = request.GET.copy()
    filters.pop("model", None)

    selected_model = None
    fields = []
    data = []

    if report_model_id:
        selected_model = ReportableModel.objects.get(id=report_model_id)
        fields = ReportableField.objects.filter(model=selected_model, is_visible=True)

        # Dynamically get model class
        app_label, model_name = selected_model.model_path.split(".")
        model_class = apps.get_model(app_label, model_name)

        queryset = model_class.objects.all()

        # Apply filters
        for field in fields:
            if field.is_filter:
                value = request.GET.get(field.field_name)
                if value:
                    filter_key = field.field_name
                    queryset = queryset.filter(**{filter_key: value})

        data = queryset.values(*[f.field_name for f in fields])

    context = {
        "report_models": ReportableModel.objects.all(),
        "selected_model": selected_model,
        "fields": fields,
        "data": data,
        "filters": request.GET,
    }

    return render(request, "reports/dynamic_report.html", context)




def get_model_fields(request):
    model_path = request.GET.get('model_path')  # e.g. "assets.Asset"
    if not model_path or '.' not in model_path:
        return JsonResponse({'error': 'Invalid model path'}, status=400)

    try:
        app_label, model_name = model_path.split('.')
        model_class = apps.get_model(app_label, model_name)

        fields = []
        for field in model_class._meta.get_fields():
            if not field.auto_created and hasattr(field, 'name'):
                fields.append({
                    'name': field.name,
                    'verbose_name': getattr(field, 'verbose_name', field.name).title()
                })
        print(fields)
        return JsonResponse({'fields': fields})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

'''
screens & PC-screens part
'''

'''
Screens view
This view displays all screens and their statuses
'''
@login_required
def all_screens(request):
    screens = Screen.objects.select_related('employee', 'branch')
    print(screens)
    all_count = screens.count()
    screen_total = screens.filter(product='Screen').count()
    screen_pc_total = screens.filter(product='Screen-PC').count()
    unique_asset_types = list(
        screens.order_by('status').values_list('status', flat=True).distinct()
    )
    print(unique_asset_types)
    stock_count = screens.filter(status='Stock').count()
    in_use_count = screens.filter(status='In Use').count()
    damage_count = screens.filter(status='Damage').count()
    
    context = {
        'branch': None,
        'screens': screens,
        'all': all_count,
        'screen_total': screen_total,
        'screen_pc_total': screen_pc_total,
        "unique_asset_types": unique_asset_types,
        "stock_count": stock_count,
        "in_use_count": in_use_count,
        "damage_count": damage_count,
    }
    return render(request, 'screens/screens_all.html', context)

'''
Create screen view
This view allows users to create a new screen
'''
@login_required
def create_screen(request):
    if request.method == 'POST':
        form = ScreenForm(request.POST)
        if form.is_valid():
            screen = form.save(commit=False)
            screen.created_by = request.user
            screen._changed_by = request.user  # ✅ for signal
            screen.status = 'Stock'
            screen.branch = Branch.objects.get(slug='stock')
            screen.save()
            messages.success(request, f"Screen {screen.serial} created successfully.")
            return redirect('all_screens')
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        form = ScreenForm()

    return render(request, 'screens/screens_create.html', {
        'form': form
    })


'''edit screen view
This view allows users to edit an existing screen'''

@login_required
def edit_screen(request, screen_id):
    screen = get_object_or_404(Screen, pk=screen_id)
    employees = Employee.objects.all()
    branches = Branch.objects.filter(choosable=True)

    if request.method == 'POST':
        product = request.POST.get('product')
        serial = request.POST.get('serial')
        brand = request.POST.get('brand')
        status = request.POST.get('status')
        employee_id = request.POST.get('employee')
        branch_id = request.POST.get('branch')

        employee = Employee.objects.get(pk=employee_id) if employee_id else None
        branch = Branch.objects.get(pk=branch_id) if branch_id else None

        # ✅ VALIDATION LOGIC
        if status == 'In Use':
            if not employee:
                messages.error(request, "Employee is required when status is 'In Use'.")
                return redirect('edit_screen', screen_id=screen.id)
            if branch and branch.name.lower() == 'stock':
                messages.error(request, "Branch must not be 'stock' when status is 'In Use'.")
                return redirect('edit_screen', screen_id=screen.id)

        elif status in ['Stock', 'Damage']:
            if employee:
                messages.error(request, "Employee must be empty when status is 'Stock' or 'Damage'.")
                return redirect('edit_screen', screen_id=screen.id)
            if not branch or branch.name.lower() != 'stock':
                messages.error(request, "Branch must be 'stock' when status is 'Stock' or 'Damage'.")
                return redirect('edit_screen', screen_id=screen.id)

        # ✅ Save changes
        screen.product = product
        screen.serial = serial
        screen.brand = brand
        screen.status = status
        screen.employee = employee if status == 'In Use' else None
        screen.branch = employee.branch if employee and status == 'In Use' else branch
        screen.updated_at = timezone.now()
        screen._changed_by = request.user
        screen.save()

        messages.success(request, f"Screen {serial} updated.")
        return redirect('edit_screen', screen_id=screen.id)

    return render(request, 'screens/screens_edit.html', {
        'screen': screen,
        'employees': employees,
        'branches': branches,
        'screen_product_choices': Screen.PRODUCT_CHOICES,
        'screen_status_choices': Screen.STATUS_CHOICES,
    })



''' unsign screen from employee
This view allows users to unassign a screen from an employee and return it to stock.'''
@require_POST
@login_required
def unassign_screen(request, screen_id, employee_id):
    screen = get_object_or_404(Screen, id=screen_id, employee__id=employee_id)
    stock_branch = Branch.objects.get(name__iexact='Stock')

    screen.employee = None
    screen.status = 'Stock'
    screen.branch = stock_branch
    screen.updated_at = timezone.now()
    screen.save()

    messages.success(request, f"Screen '{screen.serial}' unassigned successfully.")
    return redirect('edit_employee', employee_id=employee_id)

'''
Screen logs view
This view displays logs related to screen changes for a specific branch or all branches.
'''
@login_required
def all_screen_log(request, slug):
    if slug == 'All':
        logs = ScreenLog.objects.all().order_by('-change_time')
        branch = None
    else:
        branch = get_object_or_404(Branch, slug=slug)
        screen_ids = Screen.objects.filter(branch=branch).values_list('id', flat=True)
        logs = ScreenLog.objects.filter(screen_id__in=screen_ids).order_by('-change_time')

    return render(request, 'screens/screens_logs.html', {
        'logs': logs,
        'branch': branch,
        'current_branch_slug': slug,
    })
'''
branch screens view
This view displays all screens for a specific branch, including their statuses and types.
'''
@login_required
def branch_screens(request, slug):
    branch = get_object_or_404(Branch, slug=slug)
    screens = Screen.objects.filter(branch=branch)

    total = screens.count()
    screen_pcs = screens.filter(product='Screen-PC').count()
    regular_screens = screens.filter(product='Screen').count()

    return render(request, 'screens/branch_screens.html', {
        'screens': screens,
        'total': total,
        'screen_pcs': screen_pcs,
        'regular_screens': regular_screens,
        'current_branch_slug': slug,
    })

'''
Extract screens data
This view allows users to extract screen data based on selected status and format.
'''
@login_required
def extract_screens_data(request, slug):
    branch = get_object_or_404(Branch, slug=slug) if slug != 'All' else 'All'
    selected_status = request.POST.get('status')
    selected_format = request.POST.get('format')
    
    return generate_screens_report(request, branch, selected_status, selected_format)

@login_required
def download_screens_template(request):
    return generate_screen_template()

@require_POST
@login_required
def upload_screens(request, slug):
    branch = get_object_or_404(Branch, slug=slug)
    if 'excel_file' not in request.FILES:
        messages.error(request, "No file uploaded.")
        return redirect('all_screens')

    excel_file = request.FILES['excel_file']
    success = upload_bulk_screens(request, excel_file, branch, slug, request.user)
    if not success:
        messages.error(request, "Request failed, please try again")
        return redirect('all_screens')


    return redirect('all_screens')


def screen_details(request, screen_id):
    screen = get_object_or_404(Screen, pk=screen_id)
    print(screen)
    return render(request, 'screens/screens_details.html', {'screen': screen})

@require_POST
@login_required
def unassign_screen(request, screen_id, employee_id):
    screen = get_object_or_404(Screen, id=screen_id, employee__id=employee_id)
    stock_branch = Branch.objects.get(name__iexact='Stock')

    try:
        screen.employee = None
        screen.status = 'Stock'
        screen.branch = stock_branch
        screen.return_date = timezone.now().date()
        screen._changed_by = request.user
        screen.save()

        messages.success(request, f"Screen '{screen.serial}' unassigned successfully.")
    except Exception as e:
        messages.error(request, f"Error while unassigning screen: {e}")

    return redirect('edit_employee', employee_id=employee_id)


'''Infra part'''

def infrastructure_assets_view(request):

    return render(request, 'infra/infra.html')

'''Cameras part'''

@login_required
def all_cameras(request):
    unique_asset_types = list(
        Camera.objects.order_by('status').values_list('status', flat=True).distinct()
    )
    cameras = Camera.objects.all().order_by('id')
    all_count = cameras.count()
    stock_count = cameras.filter(status='Stock').count()
    in_use_count = cameras.filter(status='In Use').count()
    damage_count = cameras.filter(status='Damage').count()

    context = {
        'cameras': cameras,
        'all': all_count,
        'stock_count': stock_count,
        'in_use_count': in_use_count,
        'damage_count': damage_count,
        "unique_asset_types":unique_asset_types,
    }

    return render(request, 'infra/cameras/cameras_all.html', context)

@login_required
def branch_cameras(request, slug):
    branch = get_object_or_404(Branch, slug=slug)
    cameras = Camera.objects.filter(branch=branch)

    total = cameras.count()
    stock_count = cameras.filter(status='Stock').count()
    in_use_count = cameras.filter(status='In Use').count()
    damage_count = cameras.filter(status='Damage').count()

    context = {
        'branch': branch,
        'cameras': cameras,
        'all': total,
        'stock_count': stock_count,
        'in_use_count': in_use_count,
        'damage_count': damage_count,
        'current_branch_slug': slug,
    }

    return render(request, 'infra/cameras/cameras_branch.html', context)

@xframe_options_exempt
def camera_details(request, camera_id):
    camera = get_object_or_404(Camera, pk=camera_id)
    print(camera)
    return render(request, 'infra/cameras/camera_details.html', {'camera': camera})

def edit_camera(request, camera_id):
    camera = get_object_or_404(Camera, pk=camera_id)

    stock_branch = Branch.objects.filter(name__iexact='stock').first()
    choosable_branches = Branch.objects.filter(choosable=True)

    if request.method == 'POST':
        form = CameraEditForm(request.POST, instance=camera)

        if form.is_valid():
            camera = form.save(commit=False)
            status = form.cleaned_data.get('status')

            # Force branch to stock if not In Use
            if status != 'In Use':
                camera.branch = stock_branch
                camera.location='stock'
            else:
                # Ensure user selected a valid choosable branch
                branch = form.cleaned_data.get('branch')
                if branch and branch.choosable:
                    camera.branch = branch
                else:
                    messages.error(request, "Please select a valid branch.")
                    return render(request, 'infra/cameras/camera_edit.html', {
                        'form': form,
                        'camera': camera,
                        'choosable_branches': choosable_branches,
                        'stock_branch': stock_branch,
                        'status': status,
                    })

            # Clear location if status changed from Stock to In Use
            if camera.status == 'Stock' and status == 'In Use':
                camera.location = None  # will be required via form validation

            camera._changed_by = request.user
            camera.save()

            return redirect('camera_details', camera_id=camera.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CameraEditForm(instance=camera)

    return render(request, 'infra/cameras/camera_edit.html', {
        'form': form,
        'camera': camera,
        'choosable_branches': choosable_branches,
        'stock_branch': stock_branch,
        'status': camera.status,
    })


def add_camera(request):
    if request.method == 'POST':
        form = CameraForm(request.POST)
        if form.is_valid():
            camera = form.save(commit=False)
            camera.created_by = request.user
            camera.status = 'Stock'
            camera.branch = Branch.objects.get(name__iexact='stock')
            camera._changed_by = request.user
            camera.save()

            messages.success(request, 'Camera added successfully.')
            return redirect('all_cameras')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CameraForm()

    return render(request, 'infra/cameras/camera_create.html', {
        'form': form,
    })
    
    
    
@login_required
def all_cameras_log(request, slug):
    if slug == 'All':
        logs = CameraLog.objects.all().order_by('-change_time')
        branch = None
    else:
        branch = get_object_or_404(Branch, slug=slug)
        camera_ids = Camera.objects.filter(branch=branch).values_list('id', flat=True)
        logs = CameraLog.objects.filter(camera_id__in=camera_ids).order_by('-change_time')

    return render(request, 'infra/cameras/camera_logs.html', {
        'logs': logs,
        'branch': branch,
        'current_branch_slug': slug,
    })
    
@require_POST 
@login_required
def upload_cameras(request, slug):
    print(slug)
    branch = get_object_or_404(Branch, slug=slug)
    if 'excel_file' in request.FILES:
        excel_file = request.FILES['excel_file']

        success = upload_bulk_cameras(request, excel_file, branch, slug, request.user)

        if not success:
            if slug!='stock':
                return redirect('branch_assets', slug=slug)
            else:
                return redirect('all_cameras')

    else:
        messages.error(request, "No Excel file was uploaded.")

    if slug!='stock':
        return redirect('branch_assets', slug=slug)
    else:
        return redirect('all_cameras')

@login_required
def download_cameras_template(request):
    return generate_camera_template()

'''
Extract cameras data
This view allows users to extract screen data based on selected status and format.
'''
@login_required
def extract_cameras_data(request, slug):
    branch = get_object_or_404(Branch, slug=slug) if slug != 'All' else 'All'
    selected_status = request.POST.get('status')
    selected_format = request.POST.get('format')
    
    return generate_cameras_report(request, branch, selected_status, selected_format)