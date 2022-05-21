# from Mining.Plumber_Mining import *
import os
from DataBase.NetData_req.FetchData import *
from DataBase.Load_csv_Data import read_csv_data
from DataBase.NetData_req.tushare_home import get_fina_main
import pickle


def main():
    codes = get_codes()

    res = dict()

    for code in codes:
        res[code] = read_csv_data(code)
    pass

    print(res)


if __name__ == '__main__':
    main()
    pass
