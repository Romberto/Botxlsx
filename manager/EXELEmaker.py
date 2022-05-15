from openpyxl import Workbook


async def EXELEmaker(input_file_json, output_file_xlsx, article):
    src = input_file_json
    book = Workbook()
    sheet = book.active
    if article == 'Производитель':
        sheet['A1'] = 'Год'
        sheet['B1'] = 'Месяц'
        sheet['C1'] = 'Производитель'
        sheet['D1'] = 'Продукция'
        sheet['E1'] = 'Объем, тн'
        sheet['F1'] = 'Вагоны'
        sheet['G1'] = 'Регион отправления'
        sheet['H1'] = 'Станция отправления'
        sheet['I1'] = 'Фракция'
        sheet['J1'] = 'Порода'
        sheet['K1'] = 'Прочность'
        sheet['L1'] = 'Потребитель'
        sheet['M1'] = 'Станция потребления'
        sheet['N1'] = 'Регион потребления'

        row = 2
        for block in src:
            sheet[row][0].value = block['Год']
            sheet[row][1].value = block['Месяц']
            sheet[row][2].value = block['Производитель']
            sheet[row][3].value = block['Продукция']
            sheet[row][4].value = block['Объем, тн']
            sheet[row][5].value = block['Вагоны']
            sheet[row][6].value = block['Регион отправления']
            sheet[row][7].value = block['Станция отправления']
            sheet[row][8].value = block['Фракция']
            sheet[row][9].value = block['Порода']
            sheet[row][10].value = block['Прочность']
            sheet[row][11].value = block['Потребитель']
            sheet[row][12].value = block['Станция потребления']
            sheet[row][13].value = block['Регион потребления']
            row += 1
    elif article == 'Потребитель':
        sheet['A1'] = 'Год'
        sheet['B1'] = 'Месяц'
        sheet['C1'] = 'Потребитель'
        sheet['D1'] = 'Продукция'
        sheet['E1'] = 'Объем, тн'
        sheet['F1'] = 'Вагоны'
        sheet['G1'] = 'Регион потребления'
        sheet['H1'] = 'Станция потребления'
        sheet['I1'] = 'Фракция'
        sheet['J1'] = 'Порода'
        sheet['K1'] = 'Прочность'
        sheet['L1'] = 'Производитель'
        sheet['M1'] = 'Станция отправления'
        sheet['N1'] = 'Регион отправления'

        row = 2
        for block in src:
            sheet[row][0].value = block['Год']
            sheet[row][1].value = block['Месяц']
            sheet[row][2].value = block['Потребитель']
            sheet[row][3].value = block['Продукция']
            sheet[row][4].value = block['Объем, тн']
            sheet[row][5].value = block['Вагоны']
            sheet[row][6].value = block['Регион потребления']
            sheet[row][7].value = block['Станция потребления']
            sheet[row][8].value = block['Фракция']
            sheet[row][9].value = block['Порода']
            sheet[row][10].value = block['Прочность']
            sheet[row][11].value = block['Производитель']
            sheet[row][12].value = block['Станция отправления']
            sheet[row][13].value = block['Регион отправления']
            row += 1
    book.save(output_file_xlsx)