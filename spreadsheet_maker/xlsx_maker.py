import openpyxl
import pandas as pd


class SpreadSheet:

    def __init__(self):
        pass

    @staticmethod
    def create_excel(data):
        df = pd.DataFrame(data)
        df.to_excel('twitter_scrap.xlsx', index=False)
