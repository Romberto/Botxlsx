import datetime

from manager.PDFmaker import PDFmaker
from manager.models import LookingReport, Users


def main():
    filter_dict = {
        'chosen_name_company': 'Украина',
        'start_year': '2020',
        'start_month': '03',
        'end_year': '2020',
        'end_month': '03',
        'article': 'Производитель'
    }
    pd = PDFmaker(filter_dict, 841163160)
    time = datetime.datetime.now()

    pd.pdf_maker(f'data/test_{time}.pdf')


if __name__ == '__main__':
    main()
