# from Mining.Plumber_Mining import *
import os
from DataBase.NetData_req.FetchData import *
from DataBase.Load_csv_Data import read_csv_data
from DataBase.NetData_req.tushare_home import get_fina_main
import pickle

from Process_Site.main_prof.proess_factors import FactorProcess
from Analysis_Stage.clustering.clustering_business import *


def main():
    obj = FactorProcess()
    obj.process_factor_encode()
    obj.process_time_factor_encode()
    obj.clustering()
    # weight = obj.extract_ti_idf_time()
    # print(weight)
    # k_means_business(weight)
    # print(obj.insight_tab)
    # DBSCAN_business(weight)
    pass


if __name__ == '__main__':
    main()
    pass
