import io
from datetime import date
from itertools import count
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
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .download_templates import generate_asset_template
from .extract_date import generate_assets_report
from .models import (
    Asset,
    AssetLog,
    Branch,
    Employee,
    ReportableField,
    ReportableModel,
    StorageDevice,
)
from .upload_data import upload_bulk_asset, upload_bulk_employee


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
    branches = Branch.objects.filter(choosable=True)

    if request.method == 'POST':
        name = request.POST.get('name')
        department = request.POST.get('department')
        title = request.POST.get('title')
        email = request.POST.get('email')
        branch_id = request.POST.get('branch')
        assigned_asset_id = request.POST.get('assigned_asset')  # From modal
        print("Assigned Asset ID:", assigned_asset_id)

        # Basic validation
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

                messages.success(request, f"Employee '{employee.name}' updated successfully.")
                return redirect('edit_employee', employee_id=employee.id)

        except Exception as e:
            messages.error(request, f"Error: {e}")

    return render(request, 'employees/edit_employee.html', {
        'employee': employee,
        'assets': assets,
        'branches': branches,
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
    branch = get_object_or_404(Branch, slug=slug)
    if slug != 'All':
        # Get the branch object
        
        
        # Get assets currently in this branch
        asset_ids = Asset.objects.filter(branch=branch).values_list('id', flat=True)

        # Get logs for those assets only
        logs = AssetLog.objects.filter(asset_id__in=asset_ids).order_by('-change_time')

        context = {
            'logs': logs,
            'branch': branch,
            'current_branch_slug': branch.slug,  # Useful for displaying branch info or a back button
        }
    else:
        # All logs for all assets, regardless of branch
        logs = AssetLog.objects.all().order_by('-change_time')

        context = {
            'logs': logs,
            'branch': branch, 
            'current_branch_slug': branch.slug, # No specific branch
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


from .forms import AssetForm, StorageDeviceFormSet


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

# views.py
from django.apps import apps
from django.http import JsonResponse

from .models import ReportableModel


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

