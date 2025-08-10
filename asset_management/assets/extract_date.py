import io

import xlsxwriter
from django.contrib import messages
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse
from django.templatetags.static import static
from django.utils.html import escape

from .models import (
    NVR,
    UPS,
    AccessPoint,
    Asset,
    Camera,
    Firewall,
    Router,
    Screen,
    Switch,
    Telephone,
)

'''
the generate_assets_report function to handle both HTML and Excel formats
This function generates a report based on the selected branch and status, and returns it in the requested format.'''
def generate_assets_report(request, branch, selected_status, selected_format):
    print(branch, type(branch))
    if (str(branch))=='All':
        assets = Asset.objects.all()
        if selected_status and selected_status != 'All':
            assets = assets.filter(status=selected_status)
    else:
        assets = Asset.objects.filter(branch=branch)
    
        if selected_status and selected_status != 'All':
            assets = assets.filter(status=selected_status)

    if not assets.exists():
        messages.warning(request, 'No data available to extract based on the selected filters.')
        return None # Return None indicating no data to generate

    headers = [
        'Product', 'Serial', 'Status', 'Employee Name', 'Warranty',
        'On-Hand Date', 'Return Date', 'Comments', 'Type', 'Branch'
    ]

    if selected_format == 'excel':
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # Add formats
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 16,
            'align': 'center',
            'valign': 'vcenter'
        })
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#f36e16',
            'font_color': 'white',
            'border': 1
        })

        # 1. Leave first row for report title
        # Ensure branch.name is accessible. If branch is a string 'All', handle it.
        report_branch_name = branch.name if hasattr(branch, 'name') else str(branch)
        worksheet.merge_range('A1:J1', f'Assets Report for {report_branch_name}', title_format)
        
        # 2. Write headers starting from row 2 (since row 1 is title)
        worksheet.write_row(1, 0, headers, header_format)
        worksheet.set_row(0, 70)  # 30 points tall
        
        
        # 3. Write data starting from row 3
        for row_num, asset in enumerate(assets, start=2):
            warranty_date = asset.warranty.isoformat() if asset.warranty else ''
            on_hand_date = asset.on_hand_date.isoformat() if asset.on_hand_date else ''
            return_date = asset.return_date.isoformat() if asset.return_date else ''

            row_data = [
                asset.product,
                asset.serial,
                asset.status,
                asset.employee_name if asset.employee_name else '',
                warranty_date,
                on_hand_date,
                return_date,
                asset.comments if asset.comments else '',
                asset.type,
                asset.branch.name if asset.branch else '',
            ]
            worksheet.write_row(row_num, 0, row_data)

        # 4. Auto-fit all columns - FIXED VERSION
        for col_num, header in enumerate(headers):
            # Get all values for this column
            column_values = [str(header)]  # Start with header
            for asset in assets:
                # Map header to attribute name
                attr_name = header.lower().replace(' ', '_')
                
                # Handle specific mappings for asset attributes
                if attr_name == 'employee_name':
                    value = asset.employee_name if asset.employee_name else ''
                elif attr_name == 'warranty':
                    value = asset.warranty.isoformat() if asset.warranty else ''
                elif attr_name == 'on-hand_date': # Note: original header has '-', use actual attr name
                    value = asset.on_hand_date.isoformat() if asset.on_hand_date else ''
                elif attr_name == 'return_date':
                    value = asset.return_date.isoformat() if asset.return_date else ''
                elif attr_name == 'comments':
                    value = asset.comments if asset.comments else ''
                elif attr_name == 'type':
                    value = asset.type
                elif attr_name == 'branch':
                    value = asset.branch.name if asset.branch else ''
                elif hasattr(asset, attr_name):
                    value = str(getattr(asset, attr_name))
                else:
                    value = '' # Default for unmapped or missing attributes

                column_values.append(str(value)) # Ensure value is string for len()

            # Find maximum length
            if column_values:
                max_len = max(len(str(value)) for value in column_values)
                worksheet.set_column(col_num, col_num, max_len + 2) # +2 for padding

        workbook.close()
        output.seek(0)

        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        # Ensure branch.slug is accessible. If branch is a string 'All', provide a default slug.
        filename_slug = branch.slug if hasattr(branch, 'slug') and branch.slug else 'all-branches'
        response['Content-Disposition'] = f'attachment; filename="{filename_slug}_assets_report.xlsx"'
        return response

    elif selected_format == 'html':
        # Resolve the static URL for the logo here
        static_logo_url = request.build_absolute_uri(static('MLIT.png'))        
        print(static_logo_url)
        html_content = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Assets Report - {branch.name if hasattr(branch, 'name') else str(branch)}</title>
            <style>
                body {{
                    font-family: 'Helvetica Neue', Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                    color: #333;
                }}
                header {{
                    display: flex;
                    justify-content: flex-end;
                    margin-bottom: 20px;
                }}
                .logo {{
                    max-width: 150px;
                    height: auto;
                }}
                .report-title {{
                    font-size: 2.5em;
                    color: #000000;
                    text-align: center;
                    margin: 20px 0;
                    font-weight: 700;
                    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
                    padding-bottom: 10px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    font-size: 1em;
                }}
                th {{
                    background-color: #ff8000;
                    color: #ffffff;
                    text-transform: uppercase;
                    letter-spacing: 0.1em;
                }}
                tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
                tr:hover {{
                    background-color: #ecf0f1;
                }}
                .highlight-damage {{ /* Changed from .highlight to avoid confusion */
                    background-color: #f0c2c2; /* Light red for Damage status */
                    font-weight: bold;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    font-size: 0.9em;
                    color: #666;
                    padding: 10px 0;
                    border-top: 1px solid #ddd;
                }}
            </style>
        </head>
        <body>
            <header>
                <img src="{static_logo_url}" alt="Company Logo" class="logo">
            </header>
            <h1 class="report-title">Assets Report for {branch.name if hasattr(branch, 'name') else str(branch)}</h1>
            <table>
                <thead>
                    <tr>'''

        for header in headers:
            html_content += f'<th>{header}</th>'
        html_content += '''
                    </tr>
                </thead>
                <tbody>'''

        for asset in assets:
            # Apply highlight if status is 'Damage'
            status_class = "highlight-damage" if asset.status == "Damage" else ""
            
            # Format dates for HTML display
            warranty_html = asset.warranty.isoformat() if asset.warranty else '-'
            on_hand_html = asset.on_hand_date.isoformat() if asset.on_hand_date else '-'
            return_html = asset.return_date.isoformat() if asset.return_date else '-'

            html_content += f'''
                    <tr>
                        <td>{asset.product}</td>
                        <td>{asset.serial}</td>
                        <td class="{status_class}">{asset.status}</td>
                        <td>{asset.employee_name if asset.employee_name else '-'}</td>
                        <td>{warranty_html}</td>
                        <td>{on_hand_html}</td>
                        <td>{return_html}</td>
                        <td>{asset.comments if asset.comments else '-'}</td>
                        <td>{asset.type}</td>
                        <td>{asset.branch.name if asset.branch else '-'}</td>
                    </tr>'''

        html_content += '''
                </tbody>
            </table>
            <div class="footer">Generated by MLTI Asset Management System</div>
        </body>
        </html>'''

        response = HttpResponse(html_content, content_type='text/html')
        # Ensure branch.slug is accessible. If branch is a string 'All', provide a default slug.
        filename_slug = branch.slug if hasattr(branch, 'slug') and branch.slug else 'all-branches'
        response['Content-Disposition'] = f'attachment; filename="{filename_slug}_assets_report.html"'
        return response

    else:
        messages.error(request, "Unsupported format for extraction.")
        return None
    
    


'''
the generate_screens_report function to handle both HTML and Excel formats
This function generates a report based on the selected branch and status, and returns it in the requested'''
def generate_screens_report(request, branch, selected_status, selected_format):
    if str(branch) == 'All':
        screens = Screen.objects.all()
        if selected_status and selected_status != 'All':
            screens = screens.filter(status=selected_status)
    else:
        screens = Screen.objects.filter(branch=branch)
        if selected_status and selected_status != 'All':
            screens = screens.filter(status=selected_status)

    if not screens.exists():
        messages.warning(request, 'No data available to extract based on the selected filters.')
        return None

    headers = [
        'Product', 'Serial', 'Status', 'Employee', 'Branch'
    ]

    if selected_format == 'excel':
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # Styles
        title_format = workbook.add_format({'bold': True, 'font_size': 16, 'align': 'center'})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#0a6ebd', 'font_color': 'white', 'border': 1})

        report_branch_name = branch.name if hasattr(branch, 'name') else str(branch)
        worksheet.merge_range('A1:E1', f'Screens Report for {report_branch_name}', title_format)
        worksheet.write_row(1, 0, headers, header_format)

        for row_num, screen in enumerate(screens, start=2):
            row_data = [
                screen.product,
                screen.serial,
                screen.status,
                screen.employee.name if screen.employee else '',
                screen.branch.name if screen.branch else '',
            ]
            worksheet.write_row(row_num, 0, row_data)

        for col_num in range(len(headers)):
            worksheet.set_column(col_num, col_num, 20)

        workbook.close()
        output.seek(0)

        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename_slug = branch.slug if hasattr(branch, 'slug') else 'all-branches'
        response['Content-Disposition'] = f'attachment; filename="{filename_slug}_screens_report.xlsx"'
        return response

    elif selected_format == 'html':
        static_logo_url = request.build_absolute_uri(static('MLIT.png'))
        report_branch_name = branch.name if hasattr(branch, 'name') else str(branch)

        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Screens Report - {report_branch_name}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .logo {{
                    width: 150px;
                    float: right;
                }}
                h1 {{
                    text-align: center;
                    color: #333;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    background-color: #fff;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                th, td {{
                    padding: 12px;
                    border: 1px solid #ddd;
                    text-align: left;
                }}
                th {{
                    background-color: #0a6ebd;
                    color: white;
                }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .highlight-damage {{ background-color: #fdd; font-weight: bold; }}
                .footer {{
                    margin-top: 30px;
                    text-align: center;
                    color: #666;
                    font-size: 0.9em;
                }}
            </style>
        </head>
        <body>
            <img src="{static_logo_url}" class="logo" />
            <h1>Screens Report for {escape(report_branch_name)}</h1>
            <table>
                <thead>
                    <tr>
        '''

        for header in headers:
            html_content += f'<th>{escape(header)}</th>'
        html_content += '</tr></thead><tbody>'

        for screen in screens:
            status_class = "highlight-damage" if screen.status == "Damage" else ""
            html_content += f'''
            <tr class="{status_class}">
                <td>{escape(screen.product)}</td>
                <td>{escape(screen.serial)}</td>
                <td>{escape(screen.status)}</td>
                <td>{escape(screen.employee.name) if screen.employee else '-'}</td>
                <td>{escape(screen.branch.name) if screen.branch else '-'}</td>
            </tr>
            '''

        html_content += '''
                </tbody>
            </table>
            <div class="footer">Generated by MLTI Asset Management System</div>
        </body>
        </html>
        '''

        response = HttpResponse(html_content, content_type='text/html')
        filename_slug = branch.slug if hasattr(branch, 'slug') else 'all-branches'
        response['Content-Disposition'] = f'attachment; filename="{filename_slug}_screens_report.html"'
        return response

    else:
        messages.error(request, "Unsupported format for extraction.")
        return None


'''
the generate_telephones_report function to handle both HTML and Excel formats
This function generates a report based on the selected branch and status, and returns it in the requested'''
def generate_telephones_report(request, branch, selected_status, selected_format):
    if str(branch) == 'All':
        telephones = Telephone.objects.all()
        if selected_status and selected_status != 'All':
            telephones = telephones.filter(status=selected_status)
    else:
        telephones = Telephone.objects.filter(branch=branch)
        if selected_status and selected_status != 'All':
            telephones = telephones.filter(status=selected_status)

    if not telephones.exists():
        messages.warning(request, 'No data available to extract based on the selected filters.')
        return None

    headers = [
        'Product', 'Serial', 'Status', 'Employee', 'Branch'
    ]

    if selected_format == 'excel':
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # Styles
        title_format = workbook.add_format({'bold': True, 'font_size': 16, 'align': 'center'})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#0a6ebd', 'font_color': 'white', 'border': 1})

        report_branch_name = branch.name if hasattr(branch, 'name') else str(branch)
        worksheet.merge_range('A1:E1', f'Telephones Report for {report_branch_name}', title_format)
        worksheet.write_row(1, 0, headers, header_format)

        for row_num, telephone in enumerate(telephones, start=2):
            row_data = [
                telephone.product,
                telephone.serial,
                telephone.status,
                telephone.employee.name if telephone.employee else '',
                telephone.branch.name if telephone.branch else '',
            ]
            worksheet.write_row(row_num, 0, row_data)

        for col_num in range(len(headers)):
            worksheet.set_column(col_num, col_num, 20)

        workbook.close()
        output.seek(0)

        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename_slug = branch.slug if hasattr(branch, 'slug') else 'all-branches'
        response['Content-Disposition'] = f'attachment; filename="{filename_slug}_telephones_report.xlsx"'
        return response

    elif selected_format == 'html':
        static_logo_url = request.build_absolute_uri(static('MLIT.png'))
        report_branch_name = branch.name if hasattr(branch, 'name') else str(branch)

        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Telephones Report - {report_branch_name}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .logo {{
                    width: 150px;
                    float: right;
                }}
                h1 {{
                    text-align: center;
                    color: #333;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    background-color: #fff;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                th, td {{
                    padding: 12px;
                    border: 1px solid #ddd;
                    text-align: left;
                }}
                th {{
                    background-color: #0a6ebd;
                    color: white;
                }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .highlight-damage {{ background-color: #fdd; font-weight: bold; }}
                .footer {{
                    margin-top: 30px;
                    text-align: center;
                    color: #666;
                    font-size: 0.9em;
                }}
            </style>
        </head>
        <body>
            <img src="{static_logo_url}" class="logo" />
            <h1>Telephones Report for {escape(report_branch_name)}</h1>
            <table>
                <thead>
                    <tr>
        '''

        for header in headers:
            html_content += f'<th>{escape(header)}</th>'
        html_content += '</tr></thead><tbody>'

        for telephones in telephones:
            status_class = "highlight-damage" if telephones.status == "Damage" else ""
            html_content += f'''
            <tr class="{status_class}">
                <td>{escape(telephones.product)}</td>
                <td>{escape(telephones.serial)}</td>
                <td>{escape(telephones.status)}</td>
                <td>{escape(telephones.employee.name) if telephones.employee else '-'}</td>
                <td>{escape(telephones.branch.name) if telephones.branch else '-'}</td>
            </tr>
            '''

        html_content += '''
                </tbody>
            </table>
            <div class="footer">Generated by MLTI Asset Management System</div>
        </body>
        </html>
        '''

        response = HttpResponse(html_content, content_type='text/html')
        filename_slug = branch.slug if hasattr(branch, 'slug') else 'all-branches'
        response['Content-Disposition'] = f'attachment; filename="{filename_slug}_telephones_report.html"'
        return response

    else:
        messages.error(request, "Unsupported format for extraction.")
        return None

'''
the generate_cameras_report function to handle both HTML and Excel formats
This function generates a report based on the selected branch and status, and returns it in the requested'''
def generate_cameras_report(request, branch, selected_status, selected_format):
    if str(branch) == 'All':
        cameras = Camera.objects.all()
        if selected_status and selected_status != 'All':
            cameras = cameras.filter(status=selected_status)
    else:
        cameras = Camera.objects.filter(branch=branch)
        if selected_status and selected_status != 'All':
            cameras = cameras.filter(status=selected_status)

    if not cameras.exists():
        messages.warning(request, 'No data available to extract based on the selected filters.')
        return None

    headers = [
        'Model', 'Serial Number', 'Power Source',
        'IP Address', 'MAC Address', 'Location',
        'Status', 'Branch'
    ]

    if selected_format == 'excel':
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # Styles
        title_format = workbook.add_format({'bold': True, 'font_size': 16, 'align': 'center'})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#0a6ebd', 'font_color': 'white', 'border': 1})

        report_branch_name = branch.name if hasattr(branch, 'name') else str(branch)
        worksheet.merge_range('A1:H1', f'Cameras Report for {report_branch_name}', title_format)
        worksheet.write_row(1, 0, headers, header_format)

        for row_num, cam in enumerate(cameras, start=2):
            row_data = [
                cam.model,
                cam.serial_number,
                cam.power_source,
                cam.ip_address or '',
                cam.mac_address or '',
                cam.location or '',
                cam.status,
                cam.branch.name if cam.branch else '',
            ]
            worksheet.write_row(row_num, 0, row_data)

        for col_num in range(len(headers)):
            worksheet.set_column(col_num, col_num, 20)

        workbook.close()
        output.seek(0)

        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename_slug = branch.slug if hasattr(branch, 'slug') else 'all-branches'
        response['Content-Disposition'] = f'attachment; filename="{filename_slug}_cameras_report.xlsx"'
        return response

    elif selected_format == 'html':
        static_logo_url = request.build_absolute_uri(static('MLIT.png'))
        report_branch_name = branch.name if hasattr(branch, 'name') else str(branch)

        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Cameras Report - {escape(report_branch_name)}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .logo {{
                    width: 150px;
                    float: right;
                }}
                h1 {{
                    text-align: center;
                    color: #333;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    background-color: #fff;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                th, td {{
                    padding: 12px;
                    border: 1px solid #ddd;
                    text-align: left;
                }}
                th {{
                    background-color: #0a6ebd;
                    color: white;
                }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .highlight-damage {{ background-color: #fdd; font-weight: bold; }}
                .footer {{
                    margin-top: 30px;
                    text-align: center;
                    color: #666;
                    font-size: 0.9em;
                }}
            </style>
        </head>
        <body>
            <img src="{static_logo_url}" class="logo" />
            <h1>Cameras Report for {escape(report_branch_name)}</h1>
            <table>
                <thead>
                    <tr>
        '''

        for header in headers:
            html_content += f'<th>{escape(header)}</th>'
        html_content += '</tr></thead><tbody>'

        for cam in cameras:
            status_class = "highlight-damage" if cam.status == "Damage" else ""
            html_content += f'''
            <tr class="{status_class}">
                <td>{escape(cam.model)}</td>
                <td>{escape(cam.serial_number)}</td>
                <td>{escape(cam.power_source)}</td>
                <td>{escape(cam.ip_address) if cam.ip_address else '-'}</td>
                <td>{escape(cam.mac_address) if cam.mac_address else '-'}</td>
                <td>{escape(cam.location) if cam.location else '-'}</td>
                <td>{escape(cam.status)}</td>
                <td>{escape(cam.branch.name) if cam.branch else '-'}</td>
            </tr>
            '''

        html_content += '''
                </tbody>
            </table>
            <div class="footer">Generated by MLTI Asset Management System</div>
        </body>
        </html>
        '''

        response = HttpResponse(html_content, content_type='text/html')
        filename_slug = branch.slug if hasattr(branch, 'slug') else 'all-branches'
        response['Content-Disposition'] = f'attachment; filename="{filename_slug}_cameras_report.html"'
        return response

    else:
        messages.error(request, "Unsupported format for extraction.")
        return None



'''
the generate_NVRs_report function to handle both HTML and Excel formats
This function generates a report based on the selected branch and status, and returns it in the requested
'''
def generate_nvrs_report(request, branch, selected_status, selected_format):
    if str(branch) == 'All':
        nvrs = NVR.objects.all()
        if selected_status and selected_status != 'All':
            nvrs = nvrs.filter(status=selected_status)
    else:
        nvrs = NVR.objects.filter(branch=branch)
        if selected_status and selected_status != 'All':
            nvrs = nvrs.filter(status=selected_status)

    if not nvrs.exists():
        messages.warning(request, 'No data available to extract based on the selected filters.')
        return None

    headers = [
        'Model', 'Serial Number', 'HDD Capacity', 'Number of Ports',
        'IP Address', 'MAC Address', 'Location', 'Status', 'Branch'
    ]

    if selected_format == 'excel':
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        title_format = workbook.add_format({'bold': True, 'font_size': 16, 'align': 'center'})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#0a6ebd', 'font_color': 'white', 'border': 1})

        report_branch_name = branch.name if hasattr(branch, 'name') else str(branch)
        worksheet.merge_range('A1:I1', f'NVRs Report for {report_branch_name}', title_format)
        worksheet.write_row(1, 0, headers, header_format)

        for row_num, nvr in enumerate(nvrs, start=2):
            row_data = [
                nvr.model,
                nvr.serial_number,
                nvr.hdd_capacity,
                nvr.number_of_ports,
                nvr.ip_address or '',
                nvr.mac_address or '',
                nvr.location or '',
                nvr.status,
                nvr.branch.name if nvr.branch else '',
            ]
            worksheet.write_row(row_num, 0, row_data)

        for col_num in range(len(headers)):
            worksheet.set_column(col_num, col_num, 20)

        workbook.close()
        output.seek(0)

        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename_slug = branch.slug if hasattr(branch, 'slug') else 'all-branches'
        response['Content-Disposition'] = f'attachment; filename="{filename_slug}_nvrs_report.xlsx"'
        return response

    elif selected_format == 'html':
        static_logo_url = request.build_absolute_uri(static('MLIT.png'))
        report_branch_name = branch.name if hasattr(branch, 'name') else str(branch)

        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>NVRs Report - {escape(report_branch_name)}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .logo {{
                    width: 150px;
                    float: right;
                }}
                h1 {{
                    text-align: center;
                    color: #333;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    background-color: #fff;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                th, td {{
                    padding: 12px;
                    border: 1px solid #ddd;
                    text-align: left;
                }}
                th {{
                    background-color: #0a6ebd;
                    color: white;
                }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .highlight-damage {{ background-color: #fdd; font-weight: bold; }}
                .footer {{
                    margin-top: 30px;
                    text-align: center;
                    color: #666;
                    font-size: 0.9em;
                }}
            </style>
        </head>
        <body>
            <img src="{static_logo_url}" class="logo" />
            <h1>NVRs Report for {escape(report_branch_name)}</h1>
            <table>
                <thead>
                    <tr>
        '''
        for header in headers:
            html_content += f'<th>{escape(header)}</th>'
        html_content += '</tr></thead><tbody>'

        for nvr in nvrs:
            status_class = "highlight-damage" if nvr.status == "Damage" else ""
            html_content += f'''
            <tr class="{status_class}">
                <td>{escape(nvr.model)}</td>
                <td>{escape(nvr.serial_number)}</td>
                <td>{escape(nvr.hdd_capacity)}</td>
                <td>{escape(nvr.number_of_ports)}</td>
                <td>{escape(nvr.ip_address) if nvr.ip_address else '-'}</td>
                <td>{escape(nvr.mac_address) if nvr.mac_address else '-'}</td>
                <td>{escape(nvr.location) if nvr.location else '-'}</td>
                <td>{escape(nvr.status)}</td>
                <td>{escape(nvr.branch.name) if nvr.branch else '-'}</td>
            </tr>
            '''

        html_content += '''
                </tbody>
            </table>
            <div class="footer">Generated by MLTI Asset Management System</div>
        </body>
        </html>
        '''

        response = HttpResponse(html_content, content_type='text/html')
        filename_slug = branch.slug if hasattr(branch, 'slug') else 'all-branches'
        response['Content-Disposition'] = f'attachment; filename="{filename_slug}_nvrs_report.html"'
        return response

    else:
        messages.error(request, "Unsupported format for extraction.")
        return None



'''
the generate_firewall_report function to handle both HTML and Excel formats
This function generates a report based on the selected branch and status, and returns it in the requested
'''
def generate_firewalls_report(request, branch, selected_status, selected_format):
    if str(branch) == 'All':
        firewalls = Firewall.objects.all()
        if selected_status and selected_status != 'All':
            firewalls = firewalls.filter(status=selected_status)
    else:
        firewalls = Firewall.objects.filter(branch=branch)
        if selected_status and selected_status != 'All':
            firewalls = firewalls.filter(status=selected_status)

    if not firewalls.exists():
        messages.warning(request, 'No data available to extract based on the selected filters.')
        return None

    headers = [
        'Model', 'Serial Number', 'Firmware Version', 'Number of Ports',
        'IP Address', 'MAC Address', 'License Expiry Date',
        'Location', 'Status', 'Branch'
    ]

    if selected_format == 'excel':
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        title_format = workbook.add_format({'bold': True, 'font_size': 16, 'align': 'center'})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#0a6ebd', 'font_color': 'white', 'border': 1})

        report_branch_name = branch.name if hasattr(branch, 'name') else str(branch)
        worksheet.merge_range('A1:K1', f'Firewalls Report for {report_branch_name}', title_format)
        worksheet.write_row(1, 0, headers, header_format)

        for row_num, fw in enumerate(firewalls, start=2):
            row_data = [
                fw.model,
                fw.serial_number,
                fw.firmware_version or '',
                fw.number_of_ports or '',
                fw.ip_address or '',
                fw.mac_address or '',
                fw.license_expiry_date or '',
                fw.location or '',
                fw.status,
                fw.branch.name if fw.branch else '',
            ]
            worksheet.write_row(row_num, 0, row_data)

        for col_num in range(len(headers)):
            worksheet.set_column(col_num, col_num, 20)

        workbook.close()
        output.seek(0)

        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename_slug = branch.slug if hasattr(branch, 'slug') else 'all-branches'
        response['Content-Disposition'] = f'attachment; filename="{filename_slug}_firewalls_report.xlsx"'
        return response

    elif selected_format == 'html':
        static_logo_url = request.build_absolute_uri(static('MLIT.png'))
        report_branch_name = branch.name if hasattr(branch, 'name') else str(branch)

        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Firewalls Report - {escape(report_branch_name)}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .logo {{
                    width: 150px;
                    float: right;
                }}
                h1 {{
                    text-align: center;
                    color: #333;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    background-color: #fff;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                th, td {{
                    padding: 12px;
                    border: 1px solid #ddd;
                    text-align: left;
                }}
                th {{
                    background-color: #0a6ebd;
                    color: white;
                }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .highlight-damage {{ background-color: #fdd; font-weight: bold; }}
                .footer {{
                    margin-top: 30px;
                    text-align: center;
                    color: #666;
                    font-size: 0.9em;
                }}
            </style>
        </head>
        <body>
            <img src="{static_logo_url}" class="logo" />
            <h1>Firewalls Report for {escape(report_branch_name)}</h1>
            <table>
                <thead>
                    <tr>
        '''
        for header in headers:
            html_content += f'<th>{escape(header)}</th>'
        html_content += '</tr></thead><tbody>'

        for fw in firewalls:
            status_class = "highlight-damage" if fw.status == "Damage" else ""
            html_content += f'''
            <tr class="{status_class}">
                <td>{escape(fw.model)}</td>
                <td>{escape(fw.serial_number)}</td>
                <td>{escape(fw.firmware_version or "-")}</td>
                <td>{escape(fw.number_of_ports or "-")}</td>
                <td>{escape(fw.ip_address or "-")}</td>
                <td>{escape(fw.mac_address or "-")}</td>
                <td>{escape(fw.license_expiry_date or "-")}</td>
                <td>{escape(fw.location or "-")}</td>
                <td>{escape(fw.status)}</td>
                <td>{escape(fw.branch.name) if fw.branch else "-"}</td>
            </tr>
            '''

        html_content += '''
                </tbody>
            </table>
            <div class="footer">Generated by MLTI Asset Management System</div>
        </body>
        </html>
        '''

        response = HttpResponse(html_content, content_type='text/html')
        filename_slug = branch.slug if hasattr(branch, 'slug') else 'all-branches'
        response['Content-Disposition'] = f'attachment; filename="{filename_slug}_firewalls_report.html"'
        return response

    else:
        messages.error(request, "Unsupported format for extraction.")
        return None

'''
the generate_switches_report function to handle both HTML and Excel formats
This function generates a report based on the selected branch and status, and returns it in the requested format.'''

def generate_switches_report(request, branch, selected_status, selected_format):
    # === 1. Filter switches based on branch and status ===
    if str(branch) == 'All':
        switches = Switch.objects.all()
        if selected_status and selected_status != 'All':
            switches = switches.filter(status=selected_status)
    else:
        switches = Switch.objects.filter(branch=branch)
        if selected_status and selected_status != 'All':
            switches = switches.filter(status=selected_status)

    if not switches.exists():
        messages.warning(request, 'No data available to extract based on the selected filters.')
        return None

    headers = [
        'Model', 'Serial Number', 'Number of Ports', 'Number of POE Ports',
        'IP Address', 'MAC Address', 'Location', 'Status', 'Branch'
    ]

    # === 2. Excel Format ===
    if selected_format == 'excel':
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # Styles
        title_format = workbook.add_format({'bold': True, 'font_size': 16, 'align': 'center'})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#0a6ebd', 'font_color': 'white', 'border': 1})

        report_branch_name = branch.name if hasattr(branch, 'name') else str(branch)
        worksheet.merge_range('A1:I1', f'Switches Report for {report_branch_name}', title_format)
        worksheet.write_row(1, 0, headers, header_format)

        for row_num, sw in enumerate(switches, start=2):
            row_data = [
                sw.model,
                sw.serial_number,
                sw.number_of_ports,
                sw.number_of_poe_ports,
                sw.ip_address or '',
                sw.mac_address or '',
                sw.location or '',
                sw.status,
                sw.branch.name if sw.branch else '',
            ]
            worksheet.write_row(row_num, 0, row_data)

        for col_num in range(len(headers)):
            worksheet.set_column(col_num, col_num, 20)

        workbook.close()
        output.seek(0)

        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename_slug = branch.slug if hasattr(branch, 'slug') else 'all-branches'
        response['Content-Disposition'] = f'attachment; filename="{filename_slug}_switches_report.xlsx"'
        return response

    # === 3. HTML Format ===
    elif selected_format == 'html':
        static_logo_url = request.build_absolute_uri(static('MLIT.png'))
        report_branch_name = branch.name if hasattr(branch, 'name') else str(branch)

        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Switches Report - {escape(report_branch_name)}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .logo {{
                    width: 150px;
                    float: right;
                }}
                h1 {{
                    text-align: center;
                    color: #333;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    background-color: #fff;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                th, td {{
                    padding: 12px;
                    border: 1px solid #ddd;
                    text-align: left;
                }}
                th {{
                    background-color: #0a6ebd;
                    color: white;
                }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .highlight-damage {{ background-color: #fdd; font-weight: bold; }}
                .footer {{
                    margin-top: 30px;
                    text-align: center;
                    color: #666;
                    font-size: 0.9em;
                }}
            </style>
        </head>
        <body>
            <img src="{static_logo_url}" class="logo" />
            <h1>Switches Report for {escape(report_branch_name)}</h1>
            <table>
                <thead>
                    <tr>
        '''

        for header in headers:
            html_content += f'<th>{escape(header)}</th>'
        html_content += '</tr></thead><tbody>'

        for sw in switches:
            status_class = "highlight-damage" if sw.status == "Damage" else ""
            html_content += f'''
            <tr class="{status_class}">
                <td>{escape(sw.model)}</td>
                <td>{escape(sw.serial_number)}</td>
                <td>{sw.number_of_ports}</td>
                <td>{sw.number_of_poe_ports}</td>
                <td>{escape(sw.ip_address) if sw.ip_address else '-'}</td>
                <td>{escape(sw.mac_address) if sw.mac_address else '-'}</td>
                <td>{escape(sw.location) if sw.location else '-'}</td>
                <td>{escape(sw.status)}</td>
                <td>{escape(sw.branch.name) if sw.branch else '-'}</td>
            </tr>
            '''

        html_content += '''
                </tbody>
            </table>
            <div class="footer">Generated by MLTI Asset Management System</div>
        </body>
        </html>
        '''

        response = HttpResponse(html_content, content_type='text/html')
        filename_slug = branch.slug if hasattr(branch, 'slug') else 'all-branches'
        response['Content-Disposition'] = f'attachment; filename="{filename_slug}_switches_report.html"'
        return response

    # === 4. Fallback for unsupported format ===
    else:
        messages.error(request, "Unsupported format for extraction.")
        return None


'''
the generate_access_points_report function to handle both HTML and Excel formats
This function generates a report based on the selected branch and status, and returns it in the requested
'''
def generate_access_points_report(request, branch, selected_status, selected_format):
    if str(branch) == 'All':
        access_points = AccessPoint.objects.all()
        if selected_status and selected_status != 'All':
            access_points = access_points.filter(status=selected_status)
    else:
        access_points = AccessPoint.objects.filter(branch=branch)
        if selected_status and selected_status != 'All':
            access_points = access_points.filter(status=selected_status)

    if not access_points.exists():
        messages.warning(request, 'No data available to extract based on the selected filters.')
        return None

    headers = [
        'Model', 'Serial Number', 'IP Address', 'MAC Address',
        'Expiry Date', 'Location', 'Status', 'Branch'
    ]

    if selected_format == 'excel':
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        title_format = workbook.add_format({'bold': True, 'font_size': 16, 'align': 'center'})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#0a6ebd', 'font_color': 'white', 'border': 1})

        report_branch_name = branch.name if hasattr(branch, 'name') else str(branch)
        worksheet.merge_range('A1:H1', f'Access Points Report for {report_branch_name}', title_format)
        worksheet.write_row(1, 0, headers, header_format)

        for row_num, ap in enumerate(access_points, start=2):
            row_data = [
                ap.model,
                ap.serial_number,
                ap.ip_address or '',
                ap.mac_address or '',
                ap.expiry_date.strftime('%Y-%m-%d') if ap.expiry_date else '',
                ap.location or '',
                ap.status,
                ap.branch.name if ap.branch else '',
            ]
            worksheet.write_row(row_num, 0, row_data)

        for col_num in range(len(headers)):
            worksheet.set_column(col_num, col_num, 20)

        workbook.close()
        output.seek(0)

        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename_slug = branch.slug if hasattr(branch, 'slug') else 'all-branches'
        response['Content-Disposition'] = f'attachment; filename="{filename_slug}_access_points_report.xlsx"'
        return response

    elif selected_format == 'html':
        static_logo_url = request.build_absolute_uri(static('MLIT.png'))
        report_branch_name = branch.name if hasattr(branch, 'name') else str(branch)

        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Access Points Report - {escape(report_branch_name)}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .logo {{
                    width: 150px;
                    float: right;
                }}
                h1 {{
                    text-align: center;
                    color: #333;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    background-color: #fff;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                th, td {{
                    padding: 12px;
                    border: 1px solid #ddd;
                    text-align: left;
                }}
                th {{
                    background-color: #0a6ebd;
                    color: white;
                }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .highlight-damage {{ background-color: #fdd; font-weight: bold; }}
                .footer {{
                    margin-top: 30px;
                    text-align: center;
                    color: #666;
                    font-size: 0.9em;
                }}
            </style>
        </head>
        <body>
            <img src="{static_logo_url}" class="logo" />
            <h1>Access Points Report for {escape(report_branch_name)}</h1>
            <table>
                <thead>
                    <tr>
        '''
        for header in headers:
            html_content += f'<th>{escape(header)}</th>'
        html_content += '</tr></thead><tbody>'

        for ap in access_points:
            status_class = "highlight-damage" if ap.status == "Damage" else ""
            html_content += f'''
            <tr class="{status_class}">
                <td>{escape(ap.model)}</td>
                <td>{escape(ap.serial_number)}</td>
                <td>{escape(ap.ip_address) if ap.ip_address else '-'}</td>
                <td>{escape(ap.mac_address) if ap.mac_address else '-'}</td>
                <td>{ap.expiry_date.strftime('%Y-%m-%d') if ap.expiry_date else '-'}</td>
                <td>{escape(ap.location) if ap.location else '-'}</td>
                <td>{escape(ap.status)}</td>
                <td>{escape(ap.branch.name) if ap.branch else '-'}</td>
            </tr>
            '''

        html_content += '''
                </tbody>
            </table>
            <div class="footer">Generated by MLTI Asset Management System</div>
        </body>
        </html>
        '''

        response = HttpResponse(html_content, content_type='text/html')
        filename_slug = branch.slug if hasattr(branch, 'slug') else 'all-branches'
        response['Content-Disposition'] = f'attachment; filename="{filename_slug}_access_points_report.html"'
        return response

    else:
        messages.error(request, "Unsupported format for extraction.")
        return None

'''
the generate_routers_report function to handle both HTML and Excel formats
This function generates a report based on the selected branch and status, and returns it in the requested
'''
def generate_routers_report(request, branch, selected_status, selected_format):
    if str(branch) == 'All':
        routers = Router.objects.all()
        if selected_status and selected_status != 'All':
            routers = routers.filter(status=selected_status)
    else:
        routers = Router.objects.filter(branch=branch)
        if selected_status and selected_status != 'All':
            routers = routers.filter(status=selected_status)

    if not routers.exists():
        messages.warning(request, 'No data available to extract based on the selected filters.')
        return None

    headers = [
        'Model', 'Serial Number', 'IP Address', 'MAC Address',
        'Location', 'Status', 'Branch'
    ]

    if selected_format == 'excel':
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        title_format = workbook.add_format({'bold': True, 'font_size': 16, 'align': 'center'})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#0a6ebd', 'font_color': 'white', 'border': 1})

        report_branch_name = branch.name if hasattr(branch, 'name') else str(branch)
        worksheet.merge_range('A1:G1', f'Routers Report for {report_branch_name}', title_format)
        worksheet.write_row(1, 0, headers, header_format)

        for row_num, router in enumerate(routers, start=2):
            row_data = [
                router.model,
                router.serial_number,
                router.ip_address or '',
                router.mac_address or '',
                router.location or '',
                router.status,
                router.branch.name if router.branch else '',
            ]
            worksheet.write_row(row_num, 0, row_data)

        for col_num in range(len(headers)):
            worksheet.set_column(col_num, col_num, 20)

        workbook.close()
        output.seek(0)

        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename_slug = branch.slug if hasattr(branch, 'slug') else 'all-branches'
        response['Content-Disposition'] = f'attachment; filename="{filename_slug}_routers_report.xlsx"'
        return response

    elif selected_format == 'html':
        static_logo_url = request.build_absolute_uri(static('MLIT.png'))
        report_branch_name = branch.name if hasattr(branch, 'name') else str(branch)

        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Routers Report - {escape(report_branch_name)}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .logo {{
                    width: 150px;
                    float: right;
                }}
                h1 {{
                    text-align: center;
                    color: #333;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    background-color: #fff;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                th, td {{
                    padding: 12px;
                    border: 1px solid #ddd;
                    text-align: left;
                }}
                th {{
                    background-color: #0a6ebd;
                    color: white;
                }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .highlight-damage {{ background-color: #fdd; font-weight: bold; }}
                .footer {{
                    margin-top: 30px;
                    text-align: center;
                    color: #666;
                    font-size: 0.9em;
                }}
            </style>
        </head>
        <body>
            <img src="{static_logo_url}" class="logo" />
            <h1>Routers Report for {escape(report_branch_name)}</h1>
            <table>
                <thead>
                    <tr>
        '''
        for header in headers:
            html_content += f'<th>{escape(header)}</th>'
        html_content += '</tr></thead><tbody>'

        for router in routers:
            status_class = "highlight-damage" if router.status == "Damage" else ""
            html_content += f'''
            <tr class="{status_class}">
                <td>{escape(router.model)}</td>
                <td>{escape(router.serial_number)}</td>
                <td>{escape(router.ip_address) if router.ip_address else '-'}</td>
                <td>{escape(router.mac_address) if router.mac_address else '-'}</td>
                <td>{escape(router.location) if router.location else '-'}</td>
                <td>{escape(router.status)}</td>
                <td>{escape(router.branch.name) if router.branch else '-'}</td>
            </tr>
            '''

        html_content += '''
                </tbody>
            </table>
            <div class="footer">Generated by MLTI Asset Management System</div>
        </body>
        </html>
        '''

        response = HttpResponse(html_content, content_type='text/html')
        filename_slug = branch.slug if hasattr(branch, 'slug') else 'all-branches'
        response['Content-Disposition'] = f'attachment; filename="{filename_slug}_routers_report.html"'
        return response

    else:
        messages.error(request, "Unsupported format for extraction.")
        return None


'''
the generate_ups_report function to handle both HTML and Excel formats
This function generates a report based on the selected branch and status, and returns it in the requested
'''

def generate_ups_report(request, branch, selected_status, selected_format):
    # ===== Filter Data =====
    if str(branch) == 'All':
        ups_devices = UPS.objects.all()
        if selected_status and selected_status != 'All':
            ups_devices = ups_devices.filter(status=selected_status)
    else:
        ups_devices = UPS.objects.filter(branch=branch)
        if selected_status and selected_status != 'All':
            ups_devices = ups_devices.filter(status=selected_status)

    if not ups_devices.exists():
        messages.warning(request, 'No data available to extract based on the selected filters.')
        return None

    headers = [
        'Model', 'Serial Number', 'Location', 'IP Address',
        'Voltage', 'Power Source', 'Last Maintenance Date',
        'Next Maintenance Date', 'Status', 'Branch', 'Purchase Date', 'Comment'
    ]

    # ===== Excel Report =====
    if selected_format == 'excel':
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        title_format = workbook.add_format({'bold': True, 'font_size': 16, 'align': 'center'})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#0a6ebd', 'font_color': 'white', 'border': 1})

        report_branch_name = branch.name if hasattr(branch, 'name') else str(branch)
        worksheet.merge_range(0, 0, 0, len(headers) - 1, f'UPS Report for {report_branch_name}', title_format)
        worksheet.write_row(1, 0, headers, header_format)

        for row_num, ups in enumerate(ups_devices, start=2):
            row_data = [
                ups.model,
                ups.serial_number,
                ups.location or '',
                ups.ip_address or '',
                ups.voltage or '',
                ups.power_source or '',
                ups.last_maintenance_date.strftime('%Y-%m-%d') if ups.last_maintenance_date else '',
                ups.next_maintenance_date.strftime('%Y-%m-%d') if ups.next_maintenance_date else '',
                ups.status,
                ups.branch.name if ups.branch else '',
                ups.purchase_date.strftime('%Y-%m-%d') if ups.purchase_date else '',
                ups.comment or '',
            ]
            worksheet.write_row(row_num, 0, row_data)

        for col_num in range(len(headers)):
            worksheet.set_column(col_num, col_num, 20)

        workbook.close()
        output.seek(0)

        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename_slug = branch.slug if hasattr(branch, 'slug') else 'all-branches'
        response['Content-Disposition'] = f'attachment; filename="{filename_slug}_ups_report.xlsx"'
        return response

    # ===== HTML Report =====
    elif selected_format == 'html':
        static_logo_url = request.build_absolute_uri(static('MLIT.png'))
        report_branch_name = branch.name if hasattr(branch, 'name') else str(branch)

        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>UPS Report - {escape(report_branch_name)}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .logo {{
                    width: 150px;
                    float: right;
                }}
                h1 {{
                    text-align: center;
                    color: #333;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    background-color: #fff;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                th, td {{
                    padding: 12px;
                    border: 1px solid #ddd;
                    text-align: left;
                }}
                th {{
                    background-color: #0a6ebd;
                    color: white;
                }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .highlight-damage {{ background-color: #fdd; font-weight: bold; }}
                .footer {{
                    margin-top: 30px;
                    text-align: center;
                    color: #666;
                    font-size: 0.9em;
                }}
            </style>
        </head>
        <body>
            <img src="{static_logo_url}" class="logo" />
            <h1>UPS Report for {escape(report_branch_name)}</h1>
            <table>
                <thead>
                    <tr>
        '''
        for header in headers:
            html_content += f'<th>{escape(header)}</th>'
        html_content += '</tr></thead><tbody>'

        for ups in ups_devices:
            status_class = "highlight-damage" if ups.status == "Damage" else ""
            html_content += f'''
            <tr class="{status_class}">
                <td>{escape(ups.model)}</td>
                <td>{escape(ups.serial_number)}</td>
                <td>{escape(ups.location) if ups.location else '-'}</td>
                <td>{escape(ups.ip_address) if ups.ip_address else '-'}</td>
                <td>{escape(str(ups.voltage)) if ups.voltage is not None else '-'}</td>
                <td>{escape(ups.power_source) if ups.power_source else '-'}</td>
                <td>{ups.last_maintenance_date.strftime('%Y-%m-%d') if ups.last_maintenance_date else '-'}</td>
                <td>{ups.next_maintenance_date.strftime('%Y-%m-%d') if ups.next_maintenance_date else '-'}</td>
                <td>{escape(ups.status)}</td>
                <td>{escape(ups.branch.name) if ups.branch else '-'}</td>
                <td>{ups.purchase_date.strftime('%Y-%m-%d') if ups.purchase_date else '-'}</td>
                <td>{escape(ups.comment) if ups.comment else '-'}</td>
            </tr>
            '''

        html_content += '''
                </tbody>
            </table>
            <div class="footer">Generated by MLTI Asset Management System</div>
        </body>
        </html>
        '''

        response = HttpResponse(html_content, content_type='text/html')
        filename_slug = branch.slug if hasattr(branch, 'slug') else 'all-branches'
        response['Content-Disposition'] = f'attachment; filename="{filename_slug}_ups_report.html"'
        return response

    # ===== Unsupported format =====
    else:
        messages.error(request, "Unsupported format for extraction.")
        return None
