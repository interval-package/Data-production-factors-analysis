import akshare as ak


def ak_analyze(codes):
    for code in codes:
        print(code)
        res = ak.stock_financial_analysis_indicator(code)
        print(res)
        res.to_csv("./data/ak_res/{}.csv".format(code), encoding="gbk", index=False)
