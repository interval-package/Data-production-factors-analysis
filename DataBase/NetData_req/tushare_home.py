import pandas as pd
import tushare as ts
import numpy as np

from DataBase.NetData_req.FetchData import get_codes

pro = ts.pro_api("72b1a4b449a6f512120b08005ee2ba7047f48b723e6ecb53a61fa17f")


def get_fina_main(code, stock_type=".SZ"):
    df = pro.fina_mainbz(ts_code=code + stock_type, type='P')
    print(code + "finish")
    df.to_csv("../data/main_prof/{}.csv".format(code), encoding="utf-8", index=False)
    return df


def get_main_bz_by_year(code, stock_type=".SZ", start_date="20170101"):
    df = pro.fina_mainbz(ts_code=code + stock_type, start_date=start_date, type='P', end_type=4)
    print(code + "finish")
    # df.to_csv("../data/main_prof/{}.csv".format(code), encoding="utf-8", index=False)
    return df


def fetch_detail_factor():
    codes = get_codes()
    res = get_detail(codes[0])

    for code in codes[1:]:
        print(code)
        res = pd.concat([res, get_detail(code)])

    res.to_csv("../data/res_detail_factor.csv", index=False)
    return


# fetch detail data

type_list = ["ts_code", "ann_date", "f_ann_date", "end_date", "comp_type", "report_type", "end_type", "update_flag",
             "update_flag"]


def _normalize(x):
    if x.name in type_list:
        return x
    try:
        y = (x - np.min(x)) / (np.max(x) - np.min(x))
        return y
    except Exception as e:
        print(x.name)
        return x


def get_detail(code, stock_type=".SZ", start_date="20170101", is_normalize=True):
    # 现金流
    cash = pro.cashflow(ts_code=code + stock_type, start_date=start_date, type='P', end_type=4)

    # 利润
    profit = pro.income(ts_code=code + stock_type, start_date=start_date, type='P', end_type=4)

    # 资产负债表
    balance = pro.balancesheet(ts_code=code + stock_type, start_date=start_date, type='P', end_type=4)

    res = pd.merge(cash, profit)
    res = pd.merge(res, balance)

    if is_normalize:
        res = res.apply(_normalize)
    return res


if __name__ == '__main__':
    pass
