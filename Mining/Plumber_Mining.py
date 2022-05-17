import pdfplumber
import pandas as pd
import re

# import DataBase.DataBaseReader
from DataBase.LoadCompanyName import *
from typing import List


class PdfPlumberMiner(object):
    keywords = ["加权平均净资产收益率", "净利润", "资产总额", "负债总额",
                "存货", "营业收入", "营业成本", "研发投入",
                "员工数", "技术人员数", "企业涉及业务"]

    def __init__(self, read_path, save_path='./res.xlsx'):
        self.pdf = pdfplumber.open(read_path)
        self.save_path = save_path
        pass

    def bf_mining(self, judge_action):
        for page in self.pdf.pages:
            table = page.extract_table()
            if table is not None:
                judge_action(table)
        pass

    def analyze(self, raw_list):
        res = self.raw_analyze(raw_list)
        if res is not None:
            res.dropna()
            print(res)
        return

    def raw_analyze(self, raw_list: list):
        for row in raw_list:
            if row is not None:
                for col in row:
                    if self.fit_key(col):
                        print("fit with " + col)
                        return pd.DataFrame(raw_list[1:], columns=raw_list[0])
        print("whole table not fit")
        return None

    def fit_key(self, info):
        if info is not None:
            for key in self.keywords:
                if key in info:
                    return True
        return False

    def mine_pdf(self):
        return


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
