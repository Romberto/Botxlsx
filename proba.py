import datetime
from pprint import pprint

from fpdf import FPDF

from manager.PDFmaker import PDFmaker
from manager.models import LookingReport, Users


def looking_report(i: int):
    delta_day = datetime.datetime.now() - datetime.timedelta(days=i)
    query = LookingReport.select().where(LookingReport.datetime > delta_day)
    data_text = []
    for n, item in enumerate(query):
        data_text.append((n + 1, item.datetime.date(), item.description.replace('\n', ' ')))
    pdf = FPDF()

    # Add a page
    pdf.add_page()
    # set style and size of font
    # that you want in the pdf
    pdf.add_font('FreeSans', '', r'fonts/FreeSans.ttf', uni=True)
    pdf.add_font('FreeSansBo', 'B', r'fonts/FreeSansBold.ttf', uni=True)
    pdf.set_font("FreeSans", size=12)
    pdf.set_text_color(0, 0, 10)
    text = f"информация об отчётах за {i} дней"
    pdf.cell(200, 12, text, align='C', border=0, ln=1)
    for item in data_text:
        for n, text in enumerate(item):
            if n == 0:
                text = str(text)+')'
                pdf.cell(10, 16, text, align='J', border=1, ln=0)
            elif n == 1:
                date_str = datetime.datetime.strftime(text, '%d.%m')
                pdf.cell(20, 16, date_str, align='C', border=1, ln=0)
            elif n == 2:
                pdf.multi_cell(145, 8, text, align='J', border=1)

    pdf.output('data/report.pdf')


if __name__ == '__main__':
    looking_report(1)
