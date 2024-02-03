# helpers.py
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import xlsxwriter
import io

def studentlist_pdf(template_source, context_dict={}):
    template = get_template(template_source)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)  # Encode as UTF-8
    if not pdf.err:
        return result.getvalue()
    return None

def studentlist_xls(context_dict={}):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Write headers
    headers = ['CRN Number', 'Name', 'Branch', 'Year', 'CGPA', 'Email']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    # Write data
    row = 1
    for student in context_dict.get('ServiceData', []):
        worksheet.write(row, 0, student.crn_number)
        worksheet.write(row, 1, student.name)
        worksheet.write(row, 2, student.branch)
        worksheet.write(row, 3, student.year)
        worksheet.write(row, 4, student.CGPA)
        worksheet.write(row, 5, student.email)
        row += 1

    workbook.close()
    output.seek(0)
    return output.getvalue()