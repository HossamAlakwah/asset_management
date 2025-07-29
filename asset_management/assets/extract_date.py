import io

import xlsxwriter
from django.contrib import messages
from django.contrib.staticfiles.storage import staticfiles_storage  # Import this!
from django.http import HttpResponse
from django.templatetags.static import static

from .models import Asset  # , Screen, Telecom_Access  # Assuming these are your models

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
    
    
import io

import xlsxwriter
from django.contrib import messages
from django.http import HttpResponse
from django.templatetags.static import static
from django.utils.html import escape

from .models import Screen

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
