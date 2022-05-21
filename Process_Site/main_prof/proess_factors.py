import pandas as pd
import jieba
from DataBase.Load_csv_Data import read_bz_main_total
import gensim

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.cluster import KMeans


class FactorProcess:
    tar_clo = "bz_item"
    date_clo = "end_date"

    split_words = []
    split_words_time = []
    tags = []
    tags_time = []

    insight_tab = {
        "split_words": [],
        "tags": [],
    }

    encode_weight = None

    def __init__(self):
        self.data = read_bz_main_total()
        self.codes = self.data.keys()

    def process_factor_encode(self):
        for code, df in zip(self.codes, self.data.values()):
            res = df[self.tar_clo].tolist()
            res = self.process_str_element_to_string(res)
            self.split_words.append(res)
            self.tags.append(code)
        pass

    def process_time_factor_encode(self):
        for code, df in zip(self.codes, self.data.values()):
            res = df[[self.date_clo, self.tar_clo]]
            res = res.groupby(self.date_clo).bz_item.apply(list).to_dict()
            for key, value in zip(res.keys(), res.values()):
                temp = self.process_str_element_to_string(value)
                self.split_words_time.append(temp)
                self.tags_time.append(str(code)+"+"+str(key))
        pass

    @staticmethod
    def process_str_element_to_string(tar: list):
        res = ""
        for item in tar:
            temp = jieba.cut(item, cut_all=True)
            for st in temp:
                res += " " + st
        return res

    def extract_info_Ti_Dif(self):
        # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
        vectorizer = CountVectorizer(max_features=10)
        # 该类会统计每个词语的tf-idf权值
        tf_idf_transformer = TfidfTransformer()
        # 将文本转为词频矩阵并计算tf-idf
        tf_idf = tf_idf_transformer.fit_transform(vectorizer.fit_transform(self.split_words))
        # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
        x_train_weight = tf_idf.toarray()

        # self.encode_weight = x_train_weight
        return x_train_weight

    def extract_ti_idf_time(self):
        # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
        vectorizer = CountVectorizer(max_features=10)
        # 该类会统计每个词语的tf-idf权值
        tf_idf_transformer = TfidfTransformer()
        # 将文本转为词频矩阵并计算tf-idf
        tf_idf = tf_idf_transformer.fit_transform(vectorizer.fit_transform(self.split_words_time))
        # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
        x_train_weight = tf_idf.toarray()
        # self.insight_tab["res"] = x_train_weight
        # self.encode_weight = x_train_weight
        return x_train_weight

    def clustering(self):
        weight = self.extract_ti_idf_time()

        clf = KMeans(n_clusters=5)
        res = clf.fit(weight)
        print(res)
        print("the center:")
        print(clf.cluster_centers_)
        # 每个样本所属的簇
        for name, tag in zip(self.insight_tab["tags"], clf.labels_):
            print(name+": "+str(tag))
        return
