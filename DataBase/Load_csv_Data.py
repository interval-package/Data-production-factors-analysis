import pandas as pd
import os

from DataBase.NetData_req.FetchData import get_codes

dir_main_prof = os.path.join("..", "data", "main_prof")

detail_factor_path = "../data/res_detail_factor.csv"


def preloading_detail_factor(is_clear=False, is_save=False):
    _res = pd.read_csv(detail_factor_path)
    length = len(_res) * 0.8

    if is_clear:
        print("clearing empty cols, with threshold = {}".format(length))
        for col in _res.columns:
            if _res[col].count() < length:
                _res.drop(columns=col, inplace=True)
    if is_save:
        _res.to_csv(detail_factor_path, index=False)

    return _res


def read_bz_main_total():
    codes = get_codes()
    res = dict()
    for code in codes:
        res[code] = read_main_bz_csv_data(code)
    return res


def read_main_bz_csv_data(code, file_dir=dir_main_prof):
    """
    :return: return a list of dataframe
    tar_path: the file path containing the data
    """
    path = os.path.join(file_dir, "{}.csv".format(code))
    # print(path)
    res = pd.read_csv(path)
    return res
