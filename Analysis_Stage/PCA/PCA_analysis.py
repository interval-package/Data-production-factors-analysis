import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap
from sklearn.decomposition import PCA

from Process_Site.detail_data_process.detail_data_process import *
from Process_Site.main_prof.MainBzReTag import *

import matplotlib.pyplot as plt


def PCA_analysis(code, is_save=False, is_display=False):
    info_1 = DetailData.load_csv_data(code)
    info_1 = info_1[["tags", "net_profit", "r_and_d"]]
    info_1.set_index("tags", inplace=True)
    # 删除空行
    # length = len(info_1) * 0.5
    # print("clearing empty cols, with threshold = {}".format(length))
    # for col in info_1.columns:
    #     if info_1[col].count() < length:
    #         info_1.drop(columns=col, inplace=True)

    info_1.fillna(method="bfill", inplace=True)
    info_2 = loading_main_bz_by_one(code)
    info_2.set_index("tags", inplace=True)

    info_2.drop(["bz_sales","bz_profit"], axis=1)
    res = pd.concat([info_1, info_2], axis=1)
    res.dropna(axis=0, inplace=True)

    temp = res.apply(normalize, axis=1)
    # print(temp)
    arr = temp.to_numpy()
    # res.to_csv("./temp.csv", index=False)
    pca = PCA(n_components=4)
    pca.fit(arr)
    explained_variance_ratio = pca.explained_variance_ratio_
    singular_values = pca.singular_values_

    tar = pd.DataFrame(data=[res.columns[:], explained_variance_ratio, singular_values])

    if is_save:
        res.to_csv("../Data/pca_res/raw_data/{}pca_data.csv".format(code), index=False)
        tar.to_csv("../Data/pca_res/res_info/{}pca_res.csv".format(code), index=False)

    if is_display:
        pass

    # print(tar)

    return tar


def plot_decision_regions(x, y, classifier, resolution=0.02):
    markers = ['s', 'x', 'o', '^', 'v']
    colors = ['r', 'g', 'b', 'gray', 'cyan']
    cmap = ListedColormap(colors[:len(np.unique(y))])

    x1_min, x1_max = x[:, 0].min() - 1, x[:, 0].max() + 1
    x2_min, x2_max = x[:, 1].min() - 1, x[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution), np.arange(x2_min, x2_max, resolution))
    z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    z = z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, z, alpha=0.4, cmap=cmap)

    for idx, cc in enumerate(np.unique(y)):
        plt.scatter(x=x[y == cc, 0],
                    y=x[y == cc, 1],
                    alpha=0.6,
                    c=cmap(idx),
                    edgecolor='black',
                    marker=markers[idx],
                    label=cc)
