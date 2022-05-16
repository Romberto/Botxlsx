import json
from decimal import Decimal, ROUND_UP

from fpdf import FPDF

from manager.manager import delimiter_volume
from manager.models import Report, Users, LookingReport


class PDFmaker():
    def __init__(self, filter_dict, chat_id):
        self.name_company = filter_dict['chosen_name_company']
        self.chosen_name_company = filter_dict['chosen_name_company'].replace(' ', "_")
        self.start_year = filter_dict['start_year']
        self.start_month = filter_dict['start_month']
        self.end_year = filter_dict['end_year']
        self.end_month = filter_dict['end_month']
        self.article = filter_dict['article']
        self.chat_id = chat_id

    def make_report_LookingReport(self):
        user = Users.select().where(Users.chat_id == self.chat_id).first()
        description = f"отчёт формировал :{user.first_name} {user.last_name}" \
                      f"компания {self.article} {self.name_company}" \
                      f"период выборки с {self.start_month}.{self.start_year} по {self.end_month}.{self.end_year}"
        lr = LookingReport()
        lr.create_table(safe=True)
        lr.create(
            user=user,
            description=description
        )

    # принимает выборку из бызы данных ,  возвращает список словарей
    def iter_query(self, query):
        company_list = []
        for item in query:
            company_list.append({
                'Год': item.year,
                'Месяц': item.month,
                'Производитель': item.manufacturer,
                'Продукция': item.product,
                'Объем, тн': item.volume,
                'Вагоны': item.swagons,
                'Регион отправления': item.departure_region,
                'Станция отправления': item.departure_station,
                'Фракция': item.fraction,
                'Порода': item.breed,
                'Прочность': item.durance,
                'Потребитель': item.customer,
                'Станция потребления': item.customer_stantion,
                'Регион потребления': item.customer_region,
            })
        return company_list

    # делает выборку из общей базы

    def filter_database(self):

        if self.article == 'Производитель':
            query = Report.select().where(
                Report.year >= int(self.start_year),
                Report.year <= int(self.end_year),
                Report.month >= int(self.start_month),
                Report.month <= int(self.end_month),
                Report.manufacturer == self.name_company)
            return self.iter_query(query)
        elif self.article == 'Потребитель':
            query = Report.select().where(
                Report.year >= int(self.start_year),
                Report.year <= int(self.end_year),
                Report.month >= int(self.start_month),
                Report.month <= int(self.end_month),
                Report.customer == self.name_company)
            return self.iter_query(query)

    # анологичный период годом ранее
    def filter_old_database(self):

        old_volume = 0
        if self.article == 'Производитель':
            query = Report.select().where(
                Report.year >= (int(self.start_year) - 1),
                Report.year <= (int(self.end_year) - 1),
                Report.month >= int(self.start_month),
                Report.month <= int(self.end_month),
                Report.manufacturer == self.name_company)

            for row in self.iter_query(query):
                old_volume += row['Объем, тн']
            return old_volume

        elif self.article == 'Потребитель':
            query = Report.select().where(
                Report.year >= (int(self.start_year) - 1),
                Report.year <= (int(self.end_year) - 1),
                Report.month >= int(self.start_month),
                Report.month <= int(self.end_month),
                Report.customer == self.name_company)
            for row in self.iter_query(query):
                old_volume += row['Объем, тн']
            return old_volume

    def get_region_list(self, article):
        src = self.filter_database()
        result = {}

        if article == 'Производитель':

            for item in src:

                region = item['Регион потребления']
                stantion = item['Станция потребления']
                consumer = item['Потребитель']
                vol = item['Объем, тн']
                volume = Decimal(vol).quantize(Decimal('1.'), rounding=ROUND_UP)
                if not region in result.keys():
                    stantions = []
                    stantions.append(stantion)
                    result[region] = {consumer: [volume, stantions]}
                else:
                    if consumer in result[region].keys():
                        st = result[region][consumer][1]
                        if not stantion in result[region][consumer][1]:
                            st.append(stantion)
                        vol = result[region][consumer][0] + volume
                        result[region].update({consumer: [vol, st]})
                    else:
                        st = [stantion]
                        result[region].update({consumer: [volume, st]})

            summa = 0
            for reg, data in result.items():
                for customer, setting in data.items():
                    summa += int(setting[0])

            result.update({'volume_total': summa})

            return result

        elif article == 'Потребитель':

            for item in src:
                region = item['Регион отправления']
                consumer = item['Производитель']
                vol = item['Объем, тн']
                volume = Decimal(vol).quantize(Decimal('1.'), rounding=ROUND_UP)
                stantion = item['Станция отправления']

                if not region in result.keys():
                    stantions = [stantion]
                    result[region] = {consumer: [volume, stantions]}
                else:
                    if consumer in result[region].keys():
                        vol = result[region][consumer][0] + volume
                        stantions = result[region][consumer][1]
                        if not stantion in stantions:
                            stantions.append(stantion)
                        result[region].update({consumer: [vol, stantions]})
                    else:
                        stantions = result[region][consumer][1]
                        if not stantion in stantions:
                            stantions.append(stantion)
                        result[region].update({consumer: [volume, stantions]})

            summa = 0
            for reg, data in result.items():
                for customer, setting in data.items():
                    summa += int(setting[0])

            result.update({'volume_total': summa})

            return result

    def get_data_table(self):
        corte = []
        report_dict = self.get_region_list(self.article)
        for region, data in report_dict.items():
            if region == 'volume_total':
                continue
            sum = 0
            for customer, settings in data.items():
                sum += settings[0]
            if self.article == 'Производитель':
                corte.append(('*' + region, '*ст. потребл.', '*' + str(sum)))
            elif self.article == 'Потребитель':
                corte.append(('*' + region, '*ст. отправ.', '*' + str(sum)))

            for consumer, setting in list(data.items()):
                volume = setting[0]
                stantion = setting[1]
                corte.append((consumer, stantion, str(volume)))

        return corte

    def make_report_str(self):
        result = []
        company = self.name_company
        date_start = self.start_month + '_' + self.start_year
        date_end = self.end_month + '_' + self.end_year

        result.append(f'*{self.article}  {company}')

        result.append(f'!период с {date_start} по {date_end}')


        return result

    # формирует отчёт pdf
    def pdf_maker(self, text_output, ):
        pdf = FPDF()

        # Add a page
        pdf.add_page()
        # set style and size of font
        # that you want in the pdf
        pdf.add_font('FreeSans', '', r'fonts/FreeSans.ttf', uni=True)
        pdf.add_font('FreeSansBo', 'B', r'fonts/FreeSansBold.ttf', uni=True)
        pdf.set_font("FreeSans", size=12)
        # open the text file in read mode
        f = self.make_report_str()
        # insert the texts in pdf
        for x in f:
            if x.startswith('!'):
                x = x.replace("!", "")
                pdf.set_text_color(0, 0, 10)
                pdf.set_font("FreeSansBo", style='B', size=14)

            if x.startswith('*'):
                x = x.replace("*", "")
                pdf.set_text_color(0, 0, 10)
                pdf.set_font("FreeSansBo", style='B', size=18)
            if x.endswith('\n'):
                x = x.replace('\n', '')
            pdf.cell(50, 8, txt=x, ln=10)
            pdf.set_text_color(0, 0, 10)
        old_volume = self.filter_old_database()
        report_dict = self.get_region_list(self.article)
        total_volume = report_dict["volume_total"]
        try:
            p = 100 * int(total_volume) / int(old_volume)
            percent = 100 - p
        except ZeroDivisionError:
            percent = 0

        t = ('общий объём', f'{total_volume}',)
        for a, b in enumerate(t):
            if a == 0:
                b = b.replace("!", "")
                pdf.set_text_color(0, 0, 10)
                pdf.set_font("FreeSansBo", style='B', size=14)
                pdf.cell(50, 8, str(b), align='J', border=0)
            elif a == 1:
                b = b.replace("!", "")
                pdf.set_text_color(0, 0, 10)
                pdf.set_font("FreeSansBo", style='B', size=14)
                b = str(b)
                b = delimiter_volume(b)
                pdf.cell(50, 8, str(b), align='J', border=0, ln=1)

        date_start = self.start_month + '_' + str(int(self.start_year) - 1)
        date_end = self.end_month + '_' + str(int(self.end_year) - 1)
        # строчка сравнение
        t2 = (f'сравение с периодом c {date_start} по {date_end}', f' {int(percent)} %')
        for a, b in enumerate(t2):
            if a == 0:
                if old_volume < total_volume:
                    b = b.replace('-', '+')
                    pdf.set_text_color(0, 128, 0)
                else:
                    pdf.set_text_color(255, 0, 0)
                pdf.cell(150, 12, str(b), align='J', border=0)
            elif a == 1:
                if old_volume < total_volume:
                    b = b.replace('-', '+')
                    pdf.set_text_color(0, 128, 0)
                else:
                    b = ' -' + b
                    pdf.set_text_color(255, 0, 0)
                pdf.cell(30, 12, str(b), align='J', border=0, ln=1)
        #  ширина ячеек
        col_width = 150
        # проходимся по списку с данными
        table_data = self.get_data_table()

        for row in table_data:
            line_height = (pdf.font_size + 0.6)
            # получаем данные колонки таблицы
            if type(row[1]) == list:

                q = len(row[1])
                line_height = (pdf.font_size) * (q+0.6)

            pdf.set_font("FreeSans", size=10)
            for x, y in enumerate(row):
                if (x == 0):  # dynamically change the column width with certain conditions
                    if y.startswith('*'):
                        y = y.replace("*", "")
                        pdf.set_text_color(255, 0, 0)
                        pdf.cell(col_width - 50, line_height, str(y), align='J',
                                 border=1)  ## width = 2.0                      pdf.set_text_color(0, 0, 10)
                    else:
                        pdf.cell(col_width - 50, line_height, str(y[:40]), align='J', border=1, )

                elif (x == 1):
                    if type(y) == str:
                        if y.startswith('*'):
                            y = y.replace("*", "")
                            pdf.set_text_color(255, 0, 0)
                            pdf.cell(50, line_height, str(y), align='C', border=1)  ## width = 2.0
                            pdf.set_text_color(0, 0, 10)
                        else:
                            pdf.cell(50, line_height, str(y), align='C', border=1)
                    else:
                        offset = pdf.x + 50
                        top = pdf.y
                        for stan in y:
                            offsetst = pdf.x
                            topst = pdf.y + line_height/(q)
                            pdf.cell(50,line_height/(q),stan,align='C',border=1)
                            pdf.x = offsetst
                            pdf.y = topst
                        pdf.x = offset
                        pdf.y = top
                        pdf.set_text_color(0, 0, 10)
                elif (x == 2):
                    if y.startswith('*'):
                        y = y.replace("*", "")
                        pdf.set_text_color(255, 0, 0)
                        y = delimiter_volume(y)
                        pdf.cell(20, line_height, str(y), align='C', border=1, ln=1)  ## width = 2.0
                        pdf.set_text_color(0, 0, 10)
                    else:
                        y = str(y)
                        y = delimiter_volume(y)
                        pdf.cell(20, line_height, str(y), align='C', border=1, ln=1)

        pdf.output(text_output)
        self.make_report_LookingReport()
