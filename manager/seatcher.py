import json



"""
класс осуществляет поиск по фыйлу FILE_PATH_XLSX
"""

def get_names_company(article):
    with open('data/names_company.json', 'r') as f:
        src = json.load(f)
    return src[article]

class Searcher():

    def __init__(self, article, ):
        self.names = get_names_company(article)

    def pars_query(self, text):
        val = text.lower().strip()
        return [name for name in self.names if val in name.lower()]


if __name__ == '__main__':
    get_names_company('Производитель')