# dbscan 密度聚类
from matplotlib import pyplot as plt
from sklearn.cluster import DBSCAN
# K-means聚类
from sklearn.cluster import KMeans

import numpy as np
from sklearn.datasets import make_blobs

from sklearn.metrics.pairwise import pairwise_distances_argmin


# ======================================================================================================================


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


if __name__ == '__main__':
    make_random_pic()

    pass
