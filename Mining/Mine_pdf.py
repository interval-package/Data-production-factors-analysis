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


def to_pic(doc, zoom, pg, pic_path):
    """
    将单页pdf转换为pic
    :param doc: 图片的doc对象
    :param zoom: 图片缩放比例, type int, 数值越大分辨率越高
    :param pg: 对象在doc_pics中的索引
    :param pic_path: 图片保存路径
    :return: 图片的路径
    """
    rotate = int(0)
    trans = fitz.Matrix(zoom, zoom).preRotate(rotate)
    pm = doc.getPixmap(matrix=trans, alpha=False)
    path = os.path.join(pic_path, str(pg)) + '.png'
    pm.writePNG(path)
    return path


def get_crops(pic_path, canvas_size, position, cropped_pic_name, cropped_pic_path):
    """
    按给定位置截取图片
    :param pic_path: 被截取的图片的路径
    :param canvas_size: 图片为pdf时的尺寸, tuple, (0, 0, width, height)
    :param position: 要截取的位置, tuple, (y1, y2)
    :param cropped_pic_name: 截取的图片名称
    :param cropped_pic_path: 截取的图片保存路径
    :return:
    """
    img = Image.open(pic_path)
    # 当前图片的尺寸 tuple(width, height)
    pic_size = img.size
    # 截图的范围扩大值
    size_increase = 10
    x1 = 0
    x2 = pic_size[0]
    y1 = pic_size[1] * (1 - (position[1] + size_increase)/canvas_size[3])
    y2 = pic_size[1] * (1 - (position[0] - size_increase)/canvas_size[3])
    cropped_img = img.crop((x1, y1, x2, y2))
    # 保存截图文件的路径
    path = os.path.join(cropped_pic_path, cropped_pic_name) + '.png'
    cropped_img.save(path)
    print('成功截取图片:', cropped_pic_name)


class PdfTableMiner(object):
    def __init__(self, filename, password=''):
        """
        初始化
        :param filename: pdf路径
        :param password: 密码
        """
        with open(filename, 'rb') as file:
            # 创建文档分析器
            self.parser = PDFParser(file)
        # 创建文档
        self.doc = PDFDocument()
        # 连接文档与文档分析器
        self.parser.set_document(self.doc)
        self.doc.set_parser(self.parser)
        # 初始化, 提供初始密码, 若无则为空字符串
        self.doc.initialize(password)
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
        #  打开PDF文件, 生成一个包含图片doc对象的可迭代对象
        self.doc_pics = fitz.open(filename)

    def get_pic_loc(self, doc):
        """
        获取单页中图片的位置
        :param doc: pdf的doc对象
        :return: 返回一个list, 元素为图片名称和上下y坐标元组组成的tuple. 当前页的尺寸
        """
        self.interpreter.process_page(doc)
        layout = self.device.get_result()
        # pdf的尺寸, tuple, (width, height)
        canvas_size = layout.bbox
        # 图片名称坐标
        loc_top = []
        # 来源坐标
        loc_bottom = []
        # 图片名称与应截取的区域y1, y2坐标
        loc_named_pic = []
        # 遍历单页的所有LT对象
        for i in layout:
            if hasattr(i, 'get_text'):
                text = i.get_text().strip()
                # 匹配关键词
                if re.search(r'图表*\s\d+[:：]', text):
                    loc_top.append((i.bbox, text))
                elif re.search(r'来源[:：]', text):
                    loc_bottom.append((i.bbox, text))
        zip_loc = zip(loc_top, loc_bottom)
        for i in zip_loc:
            y1 = i[1][0][1]
            y2 = i[0][0][3]
            name = i[0][1]
            loc_named_pic.append((name, (y1, y2)))
        return loc_named_pic, canvas_size

    def main(self, pic_path, cropped_pic_path, pgn=None):
        """
        主函数
        :param pic_path: 被截取的图片路径
        :param cropped_pic_path: 图片的截图的保存路径
        :param pgn: 指定获取截图的对象的索引
        :return:
        """
        if pgn is not None:
            # 获取当前页的doc
            doc_pdf = self.doc_pdfs[pgn]
            doc_pic = self.doc_pics[pgn]
            # 将当前页转换为PNG, 返回值为图片路径
            path = to_pic(doc_pic, 2, pgn, pic_path)
            loc_name_pic, canvas_size = self.get_pic_loc(doc_pdf)
            if loc_name_pic:
                for i in loc_name_pic:
                    position = i[1]
                    cropped_pic_name = re.sub('/', '_', i[0])
                    get_crops(path, canvas_size, position, cropped_pic_name, cropped_pic_path)


if __name__ == '__main__':
    pdf_path = '要处理的PDF的路径'
    test = PdfTableMiner(pdf_path)
    pic_path = 'PNG的保存路径'
    cropped_pic_path = '截图的保存路径'
    page_count = test.doc_pics.pageCount
    for i in range(page_count):
        test.main(pic_path, cropped_pic_path, pgn=i)

