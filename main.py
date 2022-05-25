# from Mining.Plumber_Mining import *
import os

import pandas as pd

from DataBase.NetData_req.FetchData import *
from DataBase.Load_csv_Data import *
from DataBase.NetData_req.tushare_home import *
import pickle

from Process_Site.main_prof.proess_factors import FactorProcess
from Analysis_Stage.clustering.clustering_business import *


def main():
    pass


def preloading_data():
    codes = get_codes()
    for code in codes:
        get_fina_main(code)


if __name__ == '__main__':
    # fetch_detail_factor()
    # res = preloading_detail_factor()
    # res.fillna(method="backfill", inplace=True)
    # res.to_csv("../data/res_detail_factor.csv", index=False)
    obj = FactorProcess()
    obj.save_cluster_res()
    pass
