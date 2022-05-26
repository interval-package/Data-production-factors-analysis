import pandas as pd
import jieba
from sklearn.metrics import pairwise_distances_argmin

from DataBase.Load_csv_Data import read_bz_main_total
# import gensim

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.cluster import KMeans

import numpy as np

import matplotlib.pyplot as plt


class FactorProcess:
    tar_clo = "bz_item"
    date_clo = "end_date"
    invest_clos = ["bz_sales", "bz_profit", "bz_cost"]

    split_words = []
    split_words_time = []
    tags = []
    tags_time = []

    insight_tab = {
        "split_words": [],
        "tags": [],
    }

    invest_mat = []

    invest_header = []

    def __init__(self):
        self.data = read_bz_main_total()
        self.codes = self.data.keys()

    def process_factor_encode_type_overall(self):
        """
        :return: there is no return, but store the data to the member 'tag'
        :info this function is to  concat all the type info to one string list
        """
        for code, df in zip(self.codes, self.data.values()):
            res = df[self.tar_clo].tolist()
            res = self.process_str_element_to_string(res)
            self.split_words.append(res)
            self.tags.append(code)
        pass

    def process_factor_encode_type_by_time(self):
        """
        :return: there is no return, but store the data to the member 'tag'
        :info: this function is to  concat all the info of a period into one string list
        """
        for code, df in zip(self.codes, self.data.values()):
            res = df[[self.date_clo, self.tar_clo]]
            res = res.groupby(self.date_clo).bz_item.apply(list).to_dict()
            for key, value in zip(res.keys(), res.values()):
                temp = self.process_str_element_to_string(value)
                self.split_words_time.append(temp)
                self.tags_time.append(str(code) + "+" + str(key))
        pass

    @staticmethod
    def process_str_element_to_string(tar: list):
        res = ""
        for item in tar:
            temp = jieba.cut(item, cut_all=True)
            for st in temp:
                res += " " + st
        return res

    def process_invest_percent(self):
        """
        :return: the processed data of invest, store res in invest_mat
        : this function is to process the profit data
        """

        def avg(val: list):
            return sum(val) / len(val)

        for code, df in zip(self.codes, self.data.values()):
            df["ave_invest"] = df["bz_profit"] / df["bz_cost"]
            df["ave_sale"] = df["bz_sales"] / df["bz_cost"]
            res = df[[self.date_clo, "ave_invest", "ave_sale"]].dropna()
            tar_1 = res.groupby(self.date_clo).ave_invest.apply(list).to_dict()
            tar_2 = res.groupby(self.date_clo).ave_sale.apply(list).to_dict()
            # union dict
            # tar = {**tar_1, **tar_2}
            # tar = tar_1 | tar_2  # for py ver >= 3.9
            for key, value_1, value_2 in zip(tar_1.keys(), tar_2.values(), tar_2.values()):
                self.invest_mat.append([avg(value_1), avg(value_2)])
                self.invest_header.append(str(code) + "+" + str(key))
        pass

    type_list = ["ts_code", "end_date", "bz_item", "curr_type", "update_flag"]

    @staticmethod
    def _normalize(x):
        if x.name in FactorProcess.type_list:
            return x
        try:
            y = (x - np.min(x)) / (np.max(x) - np.min(x))
            return y
        except Exception as e:
            print(repr(e))
            # print(x.name)
            return x

    def process_factor_tagging(self):

        return

    def extract_Ti_Dif_overall(self):
        # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
        vectorizer = CountVectorizer(max_features=10)
        # 该类会统计每个词语的tf-idf权值
        tf_idf_transformer = TfidfTransformer()
        # 将文本转为词频矩阵并计算tf-idf
        tf_idf = tf_idf_transformer.fit_transform(vectorizer.fit_transform(self.split_words))
        # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
        x_train_weight = tf_idf.toarray()
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
        return x_train_weight

    def clustering_type_info(self):
        weight = self.extract_ti_idf_time()

        clf = KMeans(n_clusters=7)
        res = clf.fit(weight)
        # print(res)
        print("the center:")
        print(clf.cluster_centers_)
        # 每个样本所属的簇
        res = pd.DataFrame({"tags": self.tags_time, "type": list(clf.labels_)})
        return res.set_index("tags")

    def clustering_invest_info(self):
        if not self.invest_mat:
            self.process_invest_percent()
        # print(self.invest_mat)

        clf = KMeans(n_clusters=10)
        res = clf.fit(self.invest_mat)
        # print(res)
        print("the center:")
        print(clf.cluster_centers_)
        # 每个样本所属的簇
        res = pd.DataFrame({"tags": self.invest_header, "invest": list(clf.labels_)})
        return res.set_index("tags")

    cluster_res_path = "../data/cluster_res.csv"

    def save_cluster_res(self):
        self.process_factor_encode_type_by_time()
        self.process_invest_percent()
        print(len(self.tags_time), len(self.invest_header))
        df_2 = self.clustering_type_info()
        df_1 = self.clustering_invest_info()
        res = pd.concat([df_1, df_2], keys="tags", axis=1)
        # res = df_1.join(df_2, on=["tags"])
        print(res)
        res.to_csv(self.cluster_res_path)
        return

    def plot_k_means_res_invest(self):
        if not self.invest_mat:
            self.process_invest_percent()

        # weight = self.extract_ti_idf_time()
        weight = self.invest_mat

        clf = KMeans(n_clusters=6)
        res = clf.fit(weight)

        n_clusters = clf.n_clusters
        k_means_cluster_centers = clf.cluster_centers_

        colors = ["#4EACC5", "#FF9C34", "#4E9A06", "#4EACC5", "#FF9C34", "#4E9A06", "#4EACC5", "#FF9C34", "#4E9A06",
                  "#4EACC5", "#FF9C34", "#4E9A06", "#4EACC5", "#FF9C34", "#4E9A06", "#4EACC5"]

        k_means_labels = pairwise_distances_argmin(weight, k_means_cluster_centers)

        print(weight)
        X = np.array(weight)

        # KMeans
        for k, col in zip(range(n_clusters), colors):
            my_members = (k_means_labels == k)
            cluster_center = k_means_cluster_centers[k]
            print(my_members)
            plt.plot(X[my_members, 0], X[my_members, 1], ".", color=col, markersize=6)
            # plt.plot(X[my_members, 2], X[my_members, 3], ".", color=col, markersize=6)
            plt.plot(
                cluster_center[0],
                cluster_center[1],
                "o",
                markerfacecolor=col,
                markeredgecolor="k",
                markersize=10,
            )
        plt.show()

        pass
