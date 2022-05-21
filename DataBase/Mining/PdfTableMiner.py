import camelot as cm
# using camelot to read table

# using pdfminer to locate tar
from pdfminer.pdfparser import PDFParser, PDFDocument

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFInterpreterError
from PIL import Image
import fitz
import re
import os

import pdfplumber
import pandas as pd


class PdfTableMiner(object):
    def __init__(self, filename, password=''):
        """
        初始化所有对象，将内容分割为页
        :param filename: pdf路径
        :param password: 密码
        """
        with open(filename, 'rb') as file:
            # 创建文档分析器
            self.parser = PDFParser(file)
        # 创建文档
        self.doc = PDFDocument(self.parser, password=password)
        # 连接文档与文档分析器
        self.parser.set_document(self.doc)
        # self.doc.set_parser(self.parser)
        # 检测文档是否提供txt转换, 不提供就忽略, 抛出异常
        if not self.doc.is_extractable:
            raise PDFInterpreterError
        else:
            # 创建PDF资源管理器, 管理共享资源
            self.resource_manager = PDFResourceManager()
            # 创建一个PDF设备对象
            self.laparams = LAParams()
            self.device = PDFPageAggregator(self.resource_manager, laparams=self.laparams)
            # 创建一个PDF解释器对象
            self.interpreter = PDFPageInterpreter(self.resource_manager, self.device)
            # pdf的page对象列表
            self.doc_pdfs = list(self.doc.get_pages())
        pass


def read_pdf(read_path, save_path):
    pdf_2020 = pdfplumber.open(read_path)
    result_df = pd.DataFrame()
    for page in pdf_2020.pages:
        table = page.extract_table()
        print(table)
        df_detail = pd.DataFrame(table[1:], columns=table[0])
        result_df = pd.concat([df_detail, result_df], ignore_index=True)
    result_df.dropna(axis=1, how='all', inplace=True)
    result_df.columns = ['奖项', '作品编号', '作品名称', '参赛学校', '作者', '指导老师']
    result_df.to_excel(excel_writer=save_path, index=False, encoding='utf-8')


