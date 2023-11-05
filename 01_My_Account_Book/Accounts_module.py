import pandas as pd
import os

class Account_Book():
    
    def __init__(self, _filename):
        self.file = os.path.join(os.path.dirname(__file__), _filename)

    def load_file(self, col, cond=None):

        df = pd.read_excel(self.file, parse_dates=True)

        if col == '모두':
            return df

        else:  
            result = df[df[col] == cond]
            return result

    def make_file(filename):
        PATH = os.path.dirname(__file__)
        column_name = ["날짜", "품목", "수입", "지출", "메모"]

        df = pd.DataFrame(columns=column_name)

        with pd.ExcelWriter(os.path.join(PATH, filename)) as f:
            df.to_excel(f, sheet_name="Account", index=False)


class CRUD_Data(Account_Book):

    def __init__(self, _file, _date, _item, _income=int, _expense=int, _memo='None'):

        super().__init__(_file)

        self.date = _date
        self.item = _item
        self.income = _income
        self.expense = _expense
        self.memo = _memo


    def write_data(self):
        df = pd.read_excel(self.file, parse_dates=True)
        data = [self.date, self.item, self.income, self.expense, self.memo]
        column_name = ["날짜", "품목", "수입", "지출", "메모"]

        new_df = pd.DataFrame([data], columns=column_name)

        df = pd.concat([df, new_df], ignore_index=True, join="inner")

        return df


    def delete_data(self, num):
        df = pd.read_excel(self.file, parse_dates=True)
        df = df.drop(num, axis=0)

        return df

    def renew_data(self, num):
        df = pd.read_excel(self.file, parse_dates=True)
        df = df.reset_index(drop=True)

        data = [self.date, self.item, self.income, self.expense, self.memo]
        
        df.loc[num] = data

        return df

    def save_file(self, df):
        with pd.ExcelWriter(self.file) as f:
            df.to_excel(f, sheet_name="Account", index=False)