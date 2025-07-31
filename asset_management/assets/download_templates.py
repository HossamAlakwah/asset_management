from io import BytesIO

import openpyxl
from django.http import HttpResponse
from openpyxl.styles import PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

from .models import NVR, Asset, Camera, Screen, StorageDevice

'''
Generate asset template
This function creates an Excel template for bulk asset upload with predefined headers and drop-downs.
'''
def generate_asset_template():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Assets Upload"

    # Define headers
    headers = [
        'Product', 'Serial', 'Type', 'CPU', 'CPU Generation', 'RAM',
        'Warranty', 'Comments',
        'Storage 1 Type', 'Storage 1 Size',
        'Storage 2 Type', 'Storage 2 Size'
    ]
    ws.append(headers)

    # Highlight mandatory fields
    red_fill = PatternFill(start_color="FFCCCC", end_color="FFCCCC", fill_type="solid")
    for col in ['A', 'B', 'C']:  # Product, Serial, Type
        ws[f"{col}1"].fill = red_fill

    # Define drop-downs (choices from model)
    def add_dropdown(col_letter, choices):
        dv = DataValidation(type="list", formula1=f'"{",".join(choices)}"', allow_blank=True)
        ws.add_data_validation(dv)
        dv.add(f"{col_letter}2:{col_letter}100")

    add_dropdown("C", [c[0] for c in Asset.ASSET_TYPE_CHOICES])     # Type
    add_dropdown("D", [c[0] for c in Asset.CPU_CHOICES])            # CPU
    add_dropdown("E", [c[0] for c in Asset.CPU_GEN_CHOICES])        # CPU Gen
    add_dropdown("F", [c[0] for c in Asset.RAM_CHOICES])            # RAM
    add_dropdown("I", [c[0] for c in StorageDevice.STORAGE_TYPE_CHOICES])  # Storage 1 Type
    add_dropdown("J", [c[0] for c in StorageDevice.STORAGE_SIZE_CHOICES])  # Storage 1 Size
    add_dropdown("K", [c[0] for c in StorageDevice.STORAGE_TYPE_CHOICES])  # Storage 2 Type
    add_dropdown("L", [c[0] for c in StorageDevice.STORAGE_SIZE_CHOICES])  # Storage 2 Size

    # Return file as HTTP response
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=asset_template.xlsx'
    return response

'''
Generate screen template
This function creates an Excel template for bulk screen upload with predefined headers and drop-down
'''
def generate_screen_template():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Screens Upload"

    headers = ['Product', 'Serial','Brand']
    ws.append(headers)

    # Highlight required fields
    red_fill = PatternFill(start_color="FFCCCC", end_color="FFCCCC", fill_type="solid")
    for col in ['A', 'B','C']:
        ws[f"{col}1"].fill = red_fill

    # Add dropdown for Product
    def add_dropdown(col_letter, choices):
        dv = DataValidation(type="list", formula1=f'"{",".join(choices)}"', allow_blank=False)
        ws.add_data_validation(dv)
        dv.add(f"{col_letter}2:{col_letter}100")

    add_dropdown("A", [c[0] for c in Screen.PRODUCT_CHOICES])

    # Return file
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=screen_template.xlsx'
    return response

''' Generate camera template
This function creates an Excel template for bulk NVRs upload with predefined headers'''
def generate_camera_template():
    wb = openpyxl.Workbook()

    # ==================== CAMERA SHEET ====================
    ws_cam = wb.active
    ws_cam.title = "Camera Upload"
    camera_headers = [
        'Model', 'Serial Number', 'Power Source', 
        'IP Address', 'MAC Address','Purchase Date'
    ]
    ws_cam.append(camera_headers)

    # Required: Model, Serial Number, Power Source
    red_fill = PatternFill(start_color="FFCCCC", end_color="FFCCCC", fill_type="solid")
    for col_letter in ['A', 'B', 'C']:
        ws_cam[f"{col_letter}1"].fill = red_fill

    # Dropdown for Status
    camera_status_choices = [c[0] for c in Camera.STATUS_CHOICES]
    dv_status_cam = DataValidation(type="list", formula1=f'"{",".join(camera_status_choices)}"', allow_blank=False)
    ws_cam.add_data_validation(dv_status_cam)
    dv_status_cam.add("G2:G100")


    # ==================== RETURN FILE ====================
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=infra_camera_template.xlsx'
    return response