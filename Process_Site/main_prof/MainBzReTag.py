import pandas as pd
import time
from Process_Site.main_prof.proess_factors import *
from DataBase.NetData_req.tushare_home import *
from progress.bar import IncrementalBar

import numpy as np
from sklearn.decomposition import PCA

from Process_Site.utils import *

_Save_Path_tagged = "../Data/tagged_main_bz.csv"


def loading_main_bz_by_one(code):
    res = pd.read_csv("../data/main_bz/{}.csv".format(code))
    # print(res)
    return res


class MainBzReTag:
    saving_opt_hash = True

    def __init__(self):
        # self.data = self.loading_csv()
        pass

    def preloading(self):
        codes = get_codes()
        res = pd.DataFrame()
        for code in codes:
            print(code + " finish")
            try:
                res = self._process_df(res, code)
            except Exception as e:
                print(repr(e) + "\nwaiting........" + code)
                time.sleep(60.01)
                res = self._process_df(res, code)
        res.to_csv(_Save_Path_tagged)
        return res

    def _process_df(self, old, _code):
        temp = get_main_bz_by_year(_code)

        _index = extract_header(temp, "ts_code", "end_date")

        def replace_key(tar):
            if self.is_fit_keys(tar):
                return 1
            return 0

        temp_1 = temp[["bz_sales", "bz_profit", "bz_cost"]].copy()
        temp_1["is_data_factor"] = temp.bz_item.apply(replace_key)
        temp_1["tags"] = _index
        temp_1.set_index("tags", inplace=True)
        temp_1 = temp_1.groupby("tags").sum()
        if self.saving_opt_hash:
            temp_1.to_csv("../data/main_bz/{}.csv".format(_code))
            pass
        _res = pd.concat([old, temp_1])
        return _res

    @staticmethod
    def loading_csv():
        res = pd.read_csv(_Save_Path_tagged)
        return res

    key_words = ["信息", "数据", "互联网", "网"]

    def is_fit_keys(self, tar: str):
        for key in self.key_words:
            if key in tar:
                return True
        return False

    def total_res_connect(self):
        info_1 = self.loading_csv()
        info_1.set_index("tags", inplace=True)
        print(info_1)
        info_2 = pd.read_csv("../data/cluster_res.csv")
        print(info_2)
        # print()
        info_2.set_index("tags", inplace=True)
        res = pd.concat([info_1, info_2], axis=1)
        res.dropna(inplace=True)
        print(res)
        res.to_csv("./res.csv")

    def analysis_pca(self, code):
        main_bz = loading_main_bz_by_one(code)
        temp = main_bz[["bz_sales", "bz_profit", "bz_cost"]].apply(normalize)
        temp = temp.to_numpy()
        pca = PCA(n_components=temp.shape[1])
        pca.fit(temp)
        print(pca.explained_variance_ratio_)
        print(pca.singular_values_)
