import openpyxl
import pandas as pd


class SpreadSheet:

    def __init__(self, data):
        self.data = data

    def create_excel(self):
        df = pd.DataFrame(self.data)
        df.to_excel('twitter_scrap.xlsx', index=False)
