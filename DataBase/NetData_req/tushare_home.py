import tushare as ts

pro = ts.pro_api("72b1a4b449a6f512120b08005ee2ba7047f48b723e6ecb53a61fa17f")


def get_fina_main(code, stock_type=".SZ"):
    df = pro.fina_mainbz(ts_code=code + stock_type, type='P')
    print(code+"finish")
    df.to_csv("../data/main_prof/{}.csv".format(code), encoding="utf-8", index=False)
    return df


if __name__ == '__main__':
    pass
