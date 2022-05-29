# dbscan 密度聚类
import xlrd
from matplotlib import pyplot as plt
from sklearn.cluster import DBSCAN
# K-means聚类
from sklearn.cluster import KMeans

import numpy as np
from sklearn.datasets import make_blobs

from sklearn.metrics.pairwise import pairwise_distances_argmin


# ======================================================================================================================
from Process_Site.main_prof.proess_factors import FactorProcess


def k_means_business(weight):
    clf = KMeans(n_clusters=5)
    res = clf.fit(weight)
    print(res)
    print(clf.cluster_centers_)
    # 每个样本所属的簇
    print(clf.labels_)

    # i = 1
    # while i <= len(clf.labels_):
    #     print(i, clf.labels_[i - 1])
    #     i = i + 1
    # # 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
    # print(clf.inertia_)


# ======================================================================================================================


# Compute DBSCAN
def DBSCAN_business(weight):
    db = DBSCAN(eps=0.005, min_samples=10).fit(weight)
    print(db.core_sample_indices_)
    print(db.labels_)


def make_random_pic():
    np.random.seed(0)
    colors = ["#4EACC5", "#FF9C34", "#4E9A06", "#2E8A06", "#3E9A16"]
    batch_size = 45
    centers = [[1.4, 2.25], [2.08, 1], [0.6789, 0.7122], [0.72, 0.31], [0.40267, 1.40267]]
    n_clusters = len(centers)
    X, labels_true = make_blobs(n_samples=800, centers=centers, cluster_std=0.3)

    k_means = KMeans(init="k-means++", n_clusters=n_clusters, n_init=10)
    k_means.fit(X)

    k_means_cluster_centers = k_means.cluster_centers_

    k_means_labels = pairwise_distances_argmin(X, k_means_cluster_centers)

    for k, col in zip(range(n_clusters), colors):
        my_members = k_means_labels == k
        cluster_center = k_means_cluster_centers[k]
        plt.plot(X[my_members, 0], X[my_members, 1], "w", markerfacecolor=col, marker=".")
        plt.plot(
            cluster_center[0],
            cluster_center[1],
            "o",
            markerfacecolor=col,
            markeredgecolor="k",
            markersize=6,
        )
    plt.show()

    return


def inertia_calc():
    obj = FactorProcess()
    obj.process_invest_percent()
    obj.process_factor_encode_type_by_time()

    weight = obj.extract_ti_idf_time()

    SSE = []  # 存放每次结果的误差平方和

    iter_times = []

    centers = []

    X = range(1, 16)

    for i in X:  # 尝试要聚成的类数
        estimator = KMeans(n_clusters=i)  # 构造聚类器
        estimator.fit(weight)
        SSE.append(estimator.inertia_)
        iter_times.append(estimator.n_iter_)
        centers.append(estimator.cluster_centers_)

  # 跟k值要一样
    plt.xlabel('i')
    plt.ylabel('SSE')
    plt.plot(X, SSE, 'o-')
    plt.show()  # 画出图

    plt.xlabel('i')
    plt.ylabel('iter times')
    plt.plot(X, iter_times, 'o-')
    plt.show()  # 画出图
    pass


# ======================================================================================================================

class k_means_main:
    def __init__(self):
        self._cur_path_load_data()
        self.main()
        pass

    def main(self):
        pass

    def _cur_path_load_data(self):
        try:
            workBook = xlrd.open_workbook("../../DataBase/data/K-Means_2021.xlsx")
        except Exception as e:
            print(repr(e))
            workBook = xlrd.open_workbook("./DataBase/data/K-Means_2021.xlsx")
        sheet1_content1 = workBook.sheets()
        print(sheet1_content1)
        return


if __name__ == '__main__':
    k_means_main()

    pass
