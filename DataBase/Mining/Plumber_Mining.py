import pdfplumber
import pandas as pd
import re

# import DataBase.DataBaseReader
from DataBase.LoadCompanyName import *
from typing import List


class PdfPlumberMiner(object):
    keywords = {"加权平均净资产收益率": [],
                "净利润": [],
                "资产总额": [],
                "负债总额": [],
                "存货": [],
                "营业收入": [],
                "营业成本": [],
                "研发投入": [],
                "员工数": [],
                "技术人员数": [],
                "企业涉及业务": []}

    def __init__(self, read_path, save_path='./res.xlsx'):
        self.pdf = pdfplumber.open(read_path)
        self.save_path = save_path
        pass

    def bf_mining(self, judge_action):
        for page in self.pdf.pages:
            table_list = page.extract_table()
            if table_list is not None:
                judge_action(table_list)
        pass

    def disp_page(self, table):
        print(pd.DataFrame(data=table))
        pass

    def analyze(self, raw_list):
        tab = pd.DataFrame(data=raw_list[0:1], columns=raw_list[0])
        for col in raw_list[0]:
            fitter = self.fit_key(col)
            if fitter is not None:
                print("col fit")
                try:
                    self.keywords[fitter].append(tab[col].tolist())
                except AttributeError as e:
                    print(repr(e))
                    pass

        for row in raw_list[1:]:
            if row is not None:
                for col in row:
                    fitter = self.fit_key(col)
                    if fitter is not None:
                        print("row fit")
                        self.keywords[fitter].append(row)
        return None

    def deep_analyze(self, raw_list):
        skipper = []
        for row in raw_list:
            if row is not None:
                for col, i in zip(row, range(len(row))):
                    fitter = self.fit_key(col)
                    if fitter is not None:
                        print("fit key: " + fitter)
                        self.keywords[fitter].append(row)
                        if i not in skipper:
                            self.keywords[fitter].append([data[i] for data in raw_list])
                            skipper.append(i)
        return

    def raw_analyze(self, raw_list: list):
        for row in raw_list[1:]:
            if row is not None:
                for col in row:
                    if self.fit_key(col):
                        return pd.DataFrame(raw_list[1:], columns=raw_list[0])
        print("whole table not fit")
        return None

    def analyze_every(self, raw_list: list) -> list or None:
        for row in raw_list:
            if row is not None:
                for col in row:
                    if self.fit_key(col):
                        return row
        print("whole table not fit")
        return None

    def analyze_col(self, raw_list: list) -> list or None:
        res = []
        tab = pd.DataFrame(raw_list[1:], columns=raw_list[0])
        for col in raw_list[0]:
            if col is not None:
                if self.fit_key(col):
                    res.append(tab[col])
        if res:
            return res
        else:
            return None

    def fit_key(self, info):
        if info is not None:
            for key in self.keywords.keys():
                if key in info:
                    return key
        return None

    def cleaning_res(self):
        for key in self.keywords.keys():
            for tab, i in zip(self.keywords[key], range(len(self.keywords[key]))):
                flag = False
                for item in tab:
                    if bool(re.search(r'\d', item)):
                        flag = True
                if ~flag:
                    del self.keywords[key][i]

    def disp_self_res(self):
        # self.cleaning_res()
        for key in self.keywords.keys():
            print("key is " + key)
            for tab in self.keywords[key]:
                print(tab)


def plain_data_saver():
    return


def raw_analyze(raw_table):
    return


def read_pdf(read_path, save_path):
    pdf_2020 = pdfplumber.open(read_path)
    result_df = pd.DataFrame()
    for page in pdf_2020.pages:
        table = page.extract_table()
        if table is not None:
            df_detail = pd.DataFrame(table[1:], columns=table[0])
            print(df_detail)
            res = input()
            if res == str(1):
                print("saved")
                df_detail.dropna()
                # df_detail.to_excel(excel_writer=save_path, index=False, encoding='utf-8')
            # result_df = pd.concat([df_detail, result_df], ignore_index=True)


if __name__ == '__main__':
    pass
