import json

from peewee import chunked


import openpyxl

from manager.models import Report


async def get_data(input_file):
    rep = Report()
    rep.drop_table(safe=True)
    rep.create_table(safe=True)
    wb = openpyxl.load_workbook(input_file, read_only=True)
    ws = wb.active
    i = 0
    keys = []
    result = []
    names = {'Производитель': [], 'Потребитель': []}
    for row in ws.rows:
        if i == 0:
            i += 1

            for ceel in row:
                keys.append(ceel.value)
        else:
            line = []
            for ceel in row:
                line.append(ceel.value)
            if not line[2] in names['Производитель'] :
                names['Производитель'].append(line[2])
            if not line[11] in names['Потребитель']:
                names['Потребитель'].append(line[11])
            result.append({
                'year': line[0],
                'month': line[1],
                'manufacturer': line[2],
                'product': line[3],
                'volume': line[4],
                'swagons': line[5],
                'departure_region': line[6],
                'departure_station': line[7],
                'fraction': line[8],
                'breed': line[9],
                'durance': line[10],
                'customer': line[11],
                'customer_stantion': line[12],
                'customer_region': line[13],
            })

    for batch in chunked(result, 100):
        rep.insert_many(batch).execute()
    with open('data/names_company.json', 'w')as file:
        json.dump(names, file, indent=4, ensure_ascii=False)


async def update_data(input_file):
    rep = Report()
    wb = openpyxl.load_workbook(input_file, read_only=True)
    ws = wb.active
    i = 0
    keys = []
    result = []
    with open('data/names_company.json', 'r') as f:
        names = json.load(f)

    for row in ws.rows:
        if i == 0:
            i += 1

            for ceel in row:
                keys.append(ceel.value)
        else:
            line = []
            for ceel in row:
                line.append(ceel.value)
            if not line[2] in names['Производитель']:
                names['Производитель'].append(line[2])
            if not line[11] in names['Потребитель']:
                names['Потребитель'].append(line[11])
            result.append({
                'year': line[0],
                'month': line[1],
                'manufacturer': line[2],
                'product': line[3],
                'volume': line[4],
                'swagons': line[5],
                'departure_region': line[6],
                'departure_station': line[7],
                'fraction': line[8],
                'breed': line[9],
                'durance': line[10],
                'customer': line[11],
                'customer_stantion': line[12],
                'customer_region': line[13],
            })

    for batch in chunked(result, 100):
        rep.insert_many(batch).execute()
    with open('data/names_company.json', 'w')as file:
        json.dump(names, file, indent=4, ensure_ascii=False)