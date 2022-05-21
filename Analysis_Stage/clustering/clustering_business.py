# dbscan 密度聚类
from sklearn.cluster import DBSCAN
# K-means聚类
from sklearn.cluster import KMeans

# ======================================================================================================================


def k_means_business(weight):
    clf = KMeans(n_clusters=5)
    res = clf.fit(weight)
    print(res)
    # 20个中心点
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
