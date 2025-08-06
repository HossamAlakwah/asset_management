# upload_data.py

import pandas as pd
from django.contrib import messages
from django.db import transaction

from .models import (
    NVR,
    AccessPoint,
    Asset,
    Branch,
    Camera,
    Employee,
    Firewall,
    Router,
    StorageDevice,
    Telephone,
)

'''

upload bulk employees 

'''
def upload_bulk_employee(request, excel_file, user):
    # Basic file type validation
    if not excel_file.name.endswith(('.xls', '.xlsx')):
        messages.error(request, "Invalid file format. Please upload an Excel file (.xls or .xlsx).")
        return False

    try:
        df = pd.read_excel(excel_file)

        expected_columns = ['Name', 'Department', 'Title', 'Email']
        if not all(col in df.columns for col in expected_columns):
            missing = [col for col in expected_columns if col not in df.columns]
            messages.error(request, f"Missing required columns in Excel: {', '.join(missing)}.")
            return False

        imported = 0
        skipped = 0
        errors = []

        with transaction.atomic():
            for idx, row in df.iterrows():
                try:
                    name = str(row['Name']).strip()
                    department = str(row['Department']).strip()
                    title = str(row['Title']).strip()
                    email = str(row['Email']).strip().lower()

                    # Skip if email already exists
                    if Employee.objects.filter(email=email).exists():
                        skipped += 1
                        continue

                    Employee.objects.create(
                        name=name,
                        department=department,
                        title=title,
                        email=email,
                        created_by=user
                    )
                    imported += 1

                except Exception as e:
                    errors.append(f"Row {idx + 2}: Error processing '{row.get('Email', 'N/A')}' – {e}")

        if errors:
            for error in errors:
                messages.error(request, error)
            messages.warning(request, f"Import completed with {len(errors)} error(s), {imported} new employees added, {skipped} skipped.")
        else:
            messages.success(request, f"{imported} employees successfully imported. {skipped} duplicate emails skipped.")

        return True

    except pd.errors.EmptyDataError:
        messages.error(request, "The uploaded Excel file is empty.")
    except Exception as e:
        messages.error(request, f"Unexpected error: {e}")
        return False

'''

Assets upload

'''

def upload_bulk_asset(request, excel_file, branch, slug, user):
    # === 1. Validate file type ===
    if not excel_file.name.endswith(('.xls', '.xlsx')):
        messages.error(request, "Invalid file format. Please upload an Excel file (.xls or .xlsx).")
        return False

    try:
        df = pd.read_excel(excel_file)

        expected_columns = [
            'Product', 'Serial', 'Type', 'CPU', 'CPU Generation', 'RAM',
            'Warranty', 'Comments',
            'Storage 1 Type', 'Storage 1 Size',
            'Storage 2 Type', 'Storage 2 Size'
        ]
        if not all(col in df.columns for col in expected_columns):
            missing = [col for col in expected_columns if col not in df.columns]
            messages.error(request, f"Missing columns: {', '.join(missing)}")
            return False

        try:
            branch = Branch.objects.get(slug='stock')
        except Branch.DoesNotExist:
            messages.error(request, "Branch with slug='stock' not found.")
            return False

        imported_count = 0
        skipped_count = 0
        errors = []

        with transaction.atomic():
            for index, row in df.iterrows():
                try:
                    serial = str(row['Serial']).strip()

                    if Asset.objects.filter(serial=serial).exists():
                        skipped_count += 1
                        continue

                    asset = Asset(
                        product=str(row['Product']).strip(),
                        serial=serial,
                        type=str(row['Type']).strip(),
                        cpu=str(row['CPU']).strip() if pd.notna(row['CPU']) else None,
                        cpu_generation=str(row['CPU Generation']).strip() if pd.notna(row['CPU Generation']) else None,
                        ram=str(row['RAM']).strip() if pd.notna(row['RAM']) else None,
                        warranty=pd.to_datetime(row['Warranty']).date() if pd.notna(row['Warranty']) else None,
                        comments=str(row['Comments']).strip() if pd.notna(row['Comments']) else None,
                        status='Stock',
                        branch=branch,
                        created_by=user,
                    )
                    asset._changed_by = user
                    asset.save()

                    # === Add up to two storage devices ===
                    for n in [1, 2]:
                        storage_type = str(row.get(f'Storage {n} Type')).strip() if pd.notna(row.get(f'Storage {n} Type')) else None
                        storage_size = str(row.get(f'Storage {n} Size')).strip() if pd.notna(row.get(f'Storage {n} Size')) else None
                        if storage_type and storage_size:
                            StorageDevice.objects.create(
                                asset=asset,
                                type=storage_type,
                                size=storage_size
                            )

                    imported_count += 1

                except Exception as e:
                    errors.append(f"Row {index + 2}: Error for Serial '{row.get('Serial', 'N/A')}': {e}")

        # === Final messages ===
        if errors:
            for error in errors:
                messages.error(request, error)
            messages.warning(request, f"Uploaded with {len(errors)} error(s), {imported_count} assets added, {skipped_count} skipped.")
        else:
            messages.success(request, f"Successfully uploaded {imported_count} assets. {skipped_count} skipped (duplicates).")

        return True

    except pd.errors.EmptyDataError:
        messages.error(request, "Uploaded Excel file is empty.")
    except Exception as e:
        messages.error(request, f"Unexpected error during upload: {e}")

    return False


'''

Screens upload

'''
def upload_bulk_screens(request, excel_file, branch, slug, user):
    import pandas as pd

    from .models import Branch, Screen

    # === 1. Validate file ===
    if not excel_file.name.endswith(('.xls', '.xlsx')):
        messages.error(request, "Invalid file format. Please upload an Excel file (.xls or .xlsx).")
        return False

    try:
        df = pd.read_excel(excel_file)
        expected_columns = ['Product', 'Serial','Brand']

        if not all(col in df.columns for col in expected_columns):
            missing = [col for col in expected_columns if col not in df.columns]
            messages.error(request, f"Missing required columns: {', '.join(missing)}")
            return False

        try:
            branch = Branch.objects.get(slug='stock')
        except Branch.DoesNotExist:
            messages.error(request, "Branch with slug='stock' not found.")
            return False

        imported = 0
        skipped = 0
        errors = []

        with transaction.atomic():
            for idx, row in df.iterrows():
                try:
                    product = row['Product']
                    serial = row['Serial']
                    brand = row['Brand']

                    if pd.isna(product) or pd.isna(serial) or pd.isna(brand):
                        errors.append(
                            f"Row {idx + 2}: Missing required field(s) – "
                            f"Product: {'✔' if not pd.isna(product) else '✘'}, "
                            f"Serial: {'✔' if not pd.isna(serial) else '✘'}, "
                            f"Brand: {'✔' if not pd.isna(brand) else '✘'}"
                        )
                        continue

                    # Convert to string after validation
                    product = str(product).strip()
                    serial = str(serial).strip()
                    brand = str(brand).strip()

                    if Screen.objects.filter(serial=serial).exists():
                        errors.append(f"Skipped duplicate serial"+ serial)
                        skipped += 1
                        continue

                    screen = Screen(
                        product=product,
                        serial=serial,
                        brand=brand,
                        status='Stock',
                        employee=None,
                        branch=branch,
                        created_by=user
                    )
                    screen._changed_by = user
                    screen.save()
                    imported += 1

                except Exception as e:
                    errors.append(f"Row {idx + 2}: Error for Serial '{row.get('Serial', 'N/A')}': {e}")

        # Final feedback
        if errors:
            for error in errors:
                messages.error(request, error)
            messages.warning(request, f"Upload completed with {len(errors)} error(s), {imported} screens added, {skipped} skipped.")
        else:
            messages.success(request, f"{imported} screens successfully imported. {skipped} duplicate serials skipped.")

        return True

    except pd.errors.EmptyDataError:
        messages.error(request, "Uploaded Excel file is empty.")
    except Exception as e:
        messages.error(request, f"Unexpected error during screen upload: {e}")

    return False


'''

Telephones upload

'''
def upload_bulk_telephones(request, excel_file, branch, slug, user):


    # === 1. Validate file ===
    if not excel_file.name.endswith(('.xls', '.xlsx')):
        messages.error(request, "Invalid file format. Please upload an Excel file (.xls or .xlsx).")
        return False

    try:
        df = pd.read_excel(excel_file)
        expected_columns = ['Product', 'Serial','Brand']

        if not all(col in df.columns for col in expected_columns):
            missing = [col for col in expected_columns if col not in df.columns]
            messages.error(request, f"Missing required columns: {', '.join(missing)}")
            return False

        try:
            branch = Branch.objects.get(slug='stock')
        except Branch.DoesNotExist:
            messages.error(request, "Branch with slug='stock' not found.")
            return False

        imported = 0
        skipped = 0
        errors = []

        with transaction.atomic():
            for idx, row in df.iterrows():
                try:
                    product = row['Product']
                    serial = row['Serial']
                    brand = row['Brand']

                    if pd.isna(product) or pd.isna(serial) or pd.isna(brand):
                        errors.append(
                            f"Row {idx + 2}: Missing required field(s) – "
                            f"Product: {'✔' if not pd.isna(product) else '✘'}, "
                            f"Serial: {'✔' if not pd.isna(serial) else '✘'}, "
                            f"Brand: {'✔' if not pd.isna(brand) else '✘'}"
                        )
                        continue

                    # Convert to string after validation
                    product = str(product).strip()
                    serial = str(serial).strip()
                    brand = str(brand).strip()

                    if Telephone.objects.filter(serial=serial).exists():
                        errors.append(f"Skipped duplicate serial"+ serial)
                        skipped += 1
                        continue

                    telephone = Telephone(
                        product=product,
                        serial=serial,
                        brand=brand,
                        status='Stock',
                        employee=None,
                        branch=branch,
                        created_by=user
                    )
                    telephone._changed_by = user
                    telephone.save()
                    imported += 1

                except Exception as e:
                    errors.append(f"Row {idx + 2}: Error for Serial '{row.get('Serial', 'N/A')}': {e}")

        # Final feedback
        if errors:
            for error in errors:
                messages.error(request, error)
            messages.warning(request, f"Upload completed with {len(errors)} error(s), {imported} telephones added, {skipped} skipped.")
        else:
            messages.success(request, f"{imported} telephones successfully imported. {skipped} duplicate serials skipped.")

        return True

    except pd.errors.EmptyDataError:
        messages.error(request, "Uploaded Excel file is empty.")
    except Exception as e:
        messages.error(request, f"Unexpected error during telephone upload: {e}")

    return False

'''
upload bulk camera functions
'''
def upload_bulk_cameras(request, excel_file, branch, slug, user):
    # === 1. Validate file ===
    if not excel_file.name.endswith(('.xls', '.xlsx')):
        messages.error(request, "Invalid file format. Please upload an Excel file (.xls or .xlsx).")
        return False

    try:
        df = pd.read_excel(excel_file)
        expected_columns = ['Model', 'Serial Number', 'Power Source', 'IP Address', 'MAC Address', 'Purchase Date']

        if not all(col in df.columns for col in expected_columns):
            missing = [col for col in expected_columns if col not in df.columns]
            messages.error(request, f"Missing required columns: {', '.join(missing)}")
            return False

        try:
            stock_branch = Branch.objects.get(slug='stock')
        except Branch.DoesNotExist:
            messages.error(request, "Branch with slug='stock' not found.")
            return False

        imported = 0
        skipped = 0
        errors = []

        with transaction.atomic():
            for idx, row in df.iterrows():
                try:
                    model = row['Model']
                    serial = row['Serial Number']
                    power = row['Power Source']
                    ip = row.get('IP Address')
                    mac = row.get('MAC Address')
                    purchase = row.get('Purchase Date')

                    # Check required fields
                    if pd.isna(model) or pd.isna(serial) or pd.isna(power):
                        errors.append(
                            f"Row {idx + 2}: Missing required field(s) – "
                            f"Model: {'✔' if not pd.isna(model) else '✘'}, "
                            f"Serial: {'✔' if not pd.isna(serial) else '✘'}, "
                            f"Power Source: {'✔' if not pd.isna(power) else '✘'}"
                        )
                        continue

                    # Normalize input
                    model = str(model).strip()
                    serial = str(serial).strip()
                    power = str(power).strip()
                    ip = str(ip).strip() if not pd.isna(ip) else None
                    mac = str(mac).strip() if not pd.isna(mac) else None
                    purchase = pd.to_datetime(purchase).date() if not pd.isna(purchase) else None

                    if Camera.objects.filter(serial_number=serial).exists():
                        errors.append(f"Skipped duplicate serial {serial}")
                        skipped += 1
                        continue

                    camera = Camera(
                        model=model,
                        serial_number=serial,
                        power_source=power,
                        ip_address=ip,
                        mac_address=mac,
                        status='Stock',
                        location='Stock',
                        purchase_date=purchase,
                        branch=stock_branch,
                        created_by=user
                    )
                    camera._changed_by = user
                    camera.save()


                except Exception as e:
                    errors.append(f"Row {idx + 2}: Error for Serial '{row.get('Serial Number', 'N/A')}': {e}")

        # Final messages
        if errors:
            for error in errors:
                messages.error(request, error)
            messages.warning(request, f"Upload completed with {len(errors)} error(s), {imported} cameras added, {skipped} skipped.")
        else:
            messages.success(request, f"{imported} cameras successfully imported. {skipped} duplicate serials skipped.")

        return True

    except pd.errors.EmptyDataError:
        messages.error(request, "Uploaded Excel file is empty.")
    except Exception as e:
        messages.error(request, f"Unexpected error during camera upload: {e}")

    return False

'''
upload bulk NVR functions
'''

def upload_bulk_nvrs(request, excel_file, branch, slug, user):
    print('uploading')
    print(user)
    if not excel_file.name.endswith(('.xls', '.xlsx')):
        messages.error(request, "Invalid file format. Please upload an Excel file (.xls or .xlsx).")
        return False

    try:
        df = pd.read_excel(excel_file)
        expected_columns = [
            'Model', 'Serial Number', 'HDD Capacity', 'Number of Ports',
            'IP Address', 'MAC Address', 'Purchase Date'
        ]

        if not all(col in df.columns for col in expected_columns):
            missing = [col for col in expected_columns if col not in df.columns]
            messages.error(request, f"Missing required columns: {', '.join(missing)}")
            return False

        try:
            stock_branch = Branch.objects.get(slug='stock')
        except Branch.DoesNotExist:
            messages.error(request, "Branch with slug='stock' not found.")
            return False

        imported = 0
        skipped = 0
        errors = []

        with transaction.atomic():
            for idx, row in df.iterrows():
                try:
                    model = row['Model']
                    serial = row['Serial Number']
                    hdd = row['HDD Capacity']
                    ports = row['Number of Ports']
                    ip = row.get('IP Address')
                    mac = row.get('MAC Address')
                    purchase = row.get('Purchase Date')

                    if pd.isna(model) or pd.isna(serial) or pd.isna(hdd) or pd.isna(ports):
                        errors.append(
                            f"Row {idx + 2}: Missing required field(s) – "
                            f"Model: {'✔' if not pd.isna(model) else '✘'}, "
                            f"Serial: {'✔' if not pd.isna(serial) else '✘'}, "
                            f"HDD Capacity: {'✔' if not pd.isna(hdd) else '✘'}, "
                            f"Number of Ports: {'✔' if not pd.isna(ports) else '✘'}"
                        )
                        continue

                    model = str(model).strip()
                    serial = str(serial).strip()
                    hdd = str(hdd).strip()
                    ports = int(ports)
                    ip = str(ip).strip() if not pd.isna(ip) else None
                    mac = str(mac).strip() if not pd.isna(mac) else None
                    purchase = pd.to_datetime(purchase).date() if not pd.isna(purchase) else None

                    if NVR.objects.filter(serial_number=serial).exists():
                        errors.append(f"Skipped duplicate serial {serial}")
                        skipped += 1
                        continue

                    nvr = NVR(
                        model=model,
                        serial_number=serial,
                        hdd_capacity=hdd,
                        number_of_ports=ports,
                        ip_address=ip,
                        mac_address=mac,
                        purchase_date=purchase,
                        status='Stock',
                        location='Stock',
                        branch=stock_branch,
                        created_by=user
                    )
                    nvr._changed_by = user
                    nvr.save()
                    imported += 1

                except Exception as e:
                    errors.append(f"Row {idx + 2}: Error for Serial '{row.get('Serial Number', 'N/A')}': {e}")

        # Final messages
        if errors:
            for error in errors:
                messages.error(request, error)
            messages.warning(request, f"Upload completed with {len(errors)} error(s), {imported} NVRs added, {skipped} skipped.")
        else:
            messages.success(request, f"{imported} NVRs successfully imported. {skipped} duplicate serials skipped.")

        return True

    except pd.errors.EmptyDataError:
        messages.error(request, "Uploaded Excel file is empty.")
    except Exception as e:
        messages.error(request, f"Unexpected error during NVR upload: {e}")

    return False


'''
upload bulk NFirewalls functions
'''
def upload_bulk_firewalls(request, excel_file, branch, slug, user):
    if not excel_file.name.endswith(('.xls', '.xlsx')):
        messages.error(request, "Invalid file format. Please upload an Excel file (.xls or .xlsx).")
        return False

    try:
        df = pd.read_excel(excel_file)
        expected_columns = [
            'Model', 'Serial Number', 'Firmware Version', 'Number of Ports',
            'IP Address', 'MAC Address', 'License Expiry Date'
        ]

        if not all(col in df.columns for col in expected_columns):
            missing = [col for col in expected_columns if col not in df.columns]
            messages.error(request, f"Missing required columns: {', '.join(missing)}")
            return False

        try:
            stock_branch = Branch.objects.get(slug='stock')
        except Branch.DoesNotExist:
            messages.error(request, "Branch with slug='stock' not found.")
            return False

        imported = 0
        skipped = 0
        errors = []

        with transaction.atomic():
            for idx, row in df.iterrows():
                try:
                    model = row['Model']
                    serial = row['Serial Number']
                    firmware = row.get('Firmware Version')
                    ports = row.get('Number of Ports')
                    ip = row.get('IP Address')
                    mac = row.get('MAC Address')
                    license_expiry = row.get('License Expiry Date')

                    if pd.isna(model) or pd.isna(serial):
                        errors.append(
                            f"Row {idx + 2}: Missing required field(s) – "
                            f"Model: {'✔' if not pd.isna(model) else '✘'}, "
                            f"Serial: {'✔' if not pd.isna(serial) else '✘'}"
                        )
                        continue

                    model = str(model).strip()
                    serial = str(serial).strip()
                    firmware = str(firmware).strip() if not pd.isna(firmware) else None
                    ports = int(ports) if not pd.isna(ports) else None
                    ip = str(ip).strip() if not pd.isna(ip) else None
                    mac = str(mac).strip() if not pd.isna(mac) else None
                    license_expiry = pd.to_datetime(license_expiry).date() if not pd.isna(license_expiry) else None

                    if Firewall.objects.filter(serial_number=serial).exists():
                        errors.append(f"Skipped duplicate serial {serial}")
                        skipped += 1
                        continue

                    firewall = Firewall(
                        model=model,
                        serial_number=serial,
                        firmware_version=firmware,
                        number_of_ports=ports,
                        ip_address=ip,
                        mac_address=mac,
                        license_expiry_date=license_expiry,
                        status='Stock',
                        location='Stock',
                        branch=stock_branch,
                        created_by=user
                    )
                    firewall._changed_by = user
                    firewall.save()
                    imported += 1

                except Exception as e:
                    errors.append(f"Row {idx + 2}: Error for Serial '{row.get('Serial Number', 'N/A')}': {e}")

        if errors:
            for error in errors:
                messages.error(request, error)
            messages.warning(request, f"Upload completed with {len(errors)} error(s), {imported} firewalls added, {skipped} skipped.")
        else:
            messages.success(request, f"{imported} firewalls successfully imported. {skipped} duplicate serials skipped.")

        return True

    except pd.errors.EmptyDataError:
        messages.error(request, "Uploaded Excel file is empty.")
    except Exception as e:
        messages.error(request, f"Unexpected error during firewall upload: {e}")

    return False

'''
upload bulk switch function
'''
def upload_bulk_switches(request, excel_file, branch, slug, user):
    import pandas as pd
    from django.db import transaction

    from .models import Branch, Switch

    # === 1. Validate file ===
    if not excel_file.name.endswith(('.xls', '.xlsx')):
        messages.error(request, "Invalid file format. Please upload an Excel file (.xls or .xlsx).")
        return False

    try:
        df = pd.read_excel(excel_file)
        expected_columns = [
            'Model', 'Serial Number', 'Number of Ports',
            'Number of POE Ports', 'IP Address', 'MAC Address', 'Purchase Date'
        ]

        if not all(col in df.columns for col in expected_columns):
            missing = [col for col in expected_columns if col not in df.columns]
            messages.error(request, f"Missing required columns: {', '.join(missing)}")
            return False

        try:
            branch = Branch.objects.get(slug='stock')
        except Branch.DoesNotExist:
            messages.error(request, "Branch with slug='stock' not found.")
            return False

        imported = 0
        skipped = 0
        errors = []

        with transaction.atomic():
            for idx, row in df.iterrows():
                try:
                    model = row['Model']
                    serial = row['Serial Number']
                    num_ports = row['Number of Ports']
                    num_poe_ports = row['Number of POE Ports']
                    ip = row.get('IP Address')
                    mac = row.get('MAC Address')
                    purchase_date = row.get('Purchase Date')

                    # Required field check
                    if pd.isna(model) or pd.isna(serial) or pd.isna(num_ports) or pd.isna(num_poe_ports):
                        errors.append(
                            f"Row {idx + 2}: Missing required field(s) – "
                            f"Model: {'✔' if not pd.isna(model) else '✘'}, "
                            f"Serial: {'✔' if not pd.isna(serial) else '✘'}, "
                            f"Number of Ports: {'✔' if not pd.isna(num_ports) else '✘'}, "
                            f"POE Ports: {'✔' if not pd.isna(num_poe_ports) else '✘'}"
                        )
                        continue

                    serial = str(serial).strip()

                    if Switch.objects.filter(serial_number=serial).exists():
                        errors.append(f"Skipped duplicate serial: {serial}")
                        skipped += 1
                        continue

                    switch = Switch(
                        model=str(model).strip(),
                        serial_number=serial,
                        number_of_ports=int(num_ports),
                        number_of_poe_ports=int(num_poe_ports),
                        ip_address=str(ip).strip() if pd.notna(ip) else None,
                        mac_address=str(mac).strip() if pd.notna(mac) else None,
                        purchase_date=purchase_date if pd.notna(purchase_date) else None,
                        branch=branch,
                        status='Stock',
                        location='stock',
                        created_by=user,
                        comment=None
                    )
                    switch._changed_by = user
                    switch.save()
                    imported += 1

                except Exception as e:
                    errors.append(f"Row {idx + 2}: Error for Serial '{row.get('Serial Number', 'N/A')}': {e}")

        # Final feedback
        if errors:
            for error in errors:
                messages.error(request, error)
            messages.warning(request, f"Upload completed with {len(errors)} error(s), {imported} switches added, {skipped} skipped.")
        else:
            messages.success(request, f"{imported} switches successfully imported. {skipped} duplicate serials skipped.")

        return True

    except pd.errors.EmptyDataError:
        messages.error(request, "Uploaded Excel file is empty.")
    except Exception as e:
        messages.error(request, f"Unexpected error during switch upload: {e}")

    return False

'''
upload bulk access point function
'''
def upload_bulk_access_points(request, excel_file, branch, slug, user):
    if not excel_file.name.endswith(('.xls', '.xlsx')):
        messages.error(request, "Invalid file format. Please upload an Excel file (.xls or .xlsx).")
        return False

    try:
        df = pd.read_excel(excel_file)
        expected_columns = [
            'Model', 'Serial Number', 'IP Address', 'MAC Address', 'Expiry Date'
        ]

        if not all(col in df.columns for col in expected_columns):
            missing = [col for col in expected_columns if col not in df.columns]
            messages.error(request, f"Missing required columns: {', '.join(missing)}")
            return False

        try:
            stock_branch = Branch.objects.get(slug='stock')
        except Branch.DoesNotExist:
            messages.error(request, "Branch with slug='stock' not found.")
            return False

        imported = 0
        skipped = 0
        errors = []

        with transaction.atomic():
            for idx, row in df.iterrows():
                try:
                    model = row['Model']
                    serial = row['Serial Number']
                    ip = row.get('IP Address')
                    mac = row.get('MAC Address')
                    expiry = row.get('Expiry Date')

                    if pd.isna(model) or pd.isna(serial):
                        errors.append(f"Row {idx + 2}: Missing required field(s)")
                        continue

                    model = str(model).strip()
                    serial = str(serial).strip()
                    ip = str(ip).strip() if not pd.isna(ip) else None
                    mac = str(mac).strip() if not pd.isna(mac) else None
                    expiry = pd.to_datetime(expiry).date() if not pd.isna(expiry) else None

                    if AccessPoint.objects.filter(serial_number=serial).exists():
                        errors.append(f"Skipped duplicate serial {serial}")
                        skipped += 1
                        continue

                    ap = AccessPoint(
                        model=model,
                        serial_number=serial,
                        ip_address=ip,
                        mac_address=mac,
                        expiry_date=expiry,
                        status='Stock',
                        location='Stock',
                        branch=stock_branch,
                        created_by=user
                    )
                    ap._changed_by = user
                    ap.save()
                    imported += 1

                except Exception as e:
                    errors.append(f"Row {idx + 2}: Error for Serial '{serial}': {e}")

        if errors:
            for error in errors:
                messages.error(request, error)
            messages.warning(request, f"Upload completed with {len(errors)} error(s), {imported} access points added, {skipped} skipped.")
        else:
            messages.success(request, f"{imported} access points successfully imported. {skipped} duplicates skipped.")

        return True

    except pd.errors.EmptyDataError:
        messages.error(request, "Uploaded Excel file is empty.")
    except Exception as e:
        messages.error(request, f"Unexpected error during access point upload: {e}")

    return False

'''
upload bulk router function
'''
def upload_bulk_routers(request, excel_file, branch, slug, user):
    if not excel_file.name.endswith(('.xls', '.xlsx')):
        messages.error(request, "Invalid file format. Please upload an Excel file (.xls or .xlsx).")
        return False

    try:
        df = pd.read_excel(excel_file)
        expected_columns = [
            'Model', 'Serial Number', 'IP Address', 'MAC Address'
        ]

        if not all(col in df.columns for col in expected_columns):
            missing = [col for col in expected_columns if col not in df.columns]
            messages.error(request, f"Missing required columns: {', '.join(missing)}")
            return False

        try:
            stock_branch = Branch.objects.get(slug='stock')
        except Branch.DoesNotExist:
            messages.error(request, "Branch with slug='stock' not found.")
            return False

        imported = 0
        skipped = 0
        errors = []

        with transaction.atomic():
            for idx, row in df.iterrows():
                try:
                    model = row['Model']
                    serial = row['Serial Number']
                    ip = row.get('IP Address')
                    mac = row.get('MAC Address')

                    if pd.isna(model) or pd.isna(serial):
                        errors.append(f"Row {idx + 2}: Missing required field(s)")
                        continue

                    model = str(model).strip()
                    serial = str(serial).strip()
                    ip = str(ip).strip() if not pd.isna(ip) else None
                    mac = str(mac).strip() if not pd.isna(mac) else None

                    if Router.objects.filter(serial_number=serial).exists():
                        errors.append(f"Skipped duplicate serial {serial}")
                        skipped += 1
                        continue

                    router = Router(
                        model=model,
                        serial_number=serial,
                        ip_address=ip,
                        mac_address=mac,
                        status='Stock',
                        location='Stock',
                        branch=stock_branch,
                        created_by=user
                    )
                    router._changed_by = user
                    router.save()
                    imported += 1

                except Exception as e:
                    errors.append(f"Row {idx + 2}: Error for Serial '{serial}': {e}")

        if errors:
            for error in errors:
                messages.error(request, error)
            messages.warning(request, f"Upload completed with {len(errors)} error(s), {imported} routers added, {skipped} skipped.")
        else:
            messages.success(request, f"{imported} routers successfully imported. {skipped} duplicates skipped.")

        return True

    except pd.errors.EmptyDataError:
        messages.error(request, "Uploaded Excel file is empty.")
    except Exception as e:
        messages.error(request, f"Unexpected error during router upload: {e}")

    return False
