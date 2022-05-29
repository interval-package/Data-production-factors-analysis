import pandas as pd
import numpy as np
import xlrd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin


class k_means_main:
    def __init__(self):
        self._cur_path_load_data()
        # self.main()
        self.one_time_cluster(4)
        pass

    def main(self):

        mat = self.mat
        X = range(2, 6)

        SSE = []
        iter_times = []
        centers = []

        for i in X:  # 尝试要聚成的类数
            estimator = KMeans(n_clusters=i)  # 构造聚类器
            estimator.fit(mat)
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

    def one_time_cluster(self, n_clusters):
        colors = ["#4EACC5", "#FF9C34", "#4E9A06", "#2E3A06", "#3E9316"]
        X = self.mat
        print(X)
        k_means = KMeans(init="k-means++", n_clusters=n_clusters, n_init=10)
        k_means.fit(X)

        k_means_cluster_centers = k_means.cluster_centers_

        k_means_labels = pairwise_distances_argmin(list(X), k_means_cluster_centers)

        # csv = pd.DataFrame(data=k_means.cluster_centers_,columns=None)
        # csv.to_csv("./res.csv")

        lb = k_means.labels_

        df = pd.DataFrame({"name": self.raw[:, 1], "label": lb})
        print(df)
        for key, _df in df.groupby("label"):
            temp = _df.values
            temp = temp.swapaxes(0, 1)
            np.savetxt("./res_{}.csv".format(key), temp, delimiter=',', fmt="%s")
            # _df.to_csv("./res_{}.csv".format(key))
            pass

        for k, col in zip(range(n_clusters), colors):
            my_members = k_means_labels == k
            cluster_center = k_means_cluster_centers[k]
            plt.plot(X[my_members, 2], X[my_members, 5], "*", color=col)
            plt.plot(
                cluster_center[2],
                cluster_center[5],
                "o",
                markerfacecolor=col,
                markeredgecolor="k",
                markersize=6,
            )
        plt.xlabel('development factor')
        plt.ylabel('research factor')
        plt.show()
        pass

    def _cur_path_load_data(self):
        df = pd.read_csv("../../DataBase/data/K-Means_2021.csv", encoding="gbk")
        # df.set_index("证券代码")
        res = df.values
        self.raw = res
        self.mat = res[:, -6:]
        self.mat[:, -1] /= 10
        return


if __name__ == '__main__':
    k_means_main()
    pass
