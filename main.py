# from Mining.Plumber_Mining import *
import matplotlib.pyplot as plt

from DataBase.NetData_req.FetchData import read_type_df, code_to_name
from DataBase.NetData_req.tushare_home import *
from Process_Site.main_prof.MainBzReTag import MainBzReTag
from Analysis_Stage.PCA.PCA_analysis import *


def main():
    fetch_detail_factor()
    # obj = MainBzReTag()
    # obj.preloading()
    # obj.total_res_connect()
    # codes = get_codes()
    # obj.analysis_pca(codes[0])
    pass


def main_2():
    codes = get_codes()
    count = 0
    for code in codes:
        print(code)
        try:
            res = PCA_analysis(code, is_save=True)

        except Exception as e:
            print(repr(e))
            print(code + " invalid")
            count += 1
            continue

    print(count)


def main_3():
    obj = FactorProcess()
    obj.process_invest_percent()
    obj.process_factor_encode_type_by_time()
    invest, type_info = obj.save_cluster_res()
    invest.reset_index(inplace=True)
    type_info.reset_index(inplace=True)

    inv_res = invest.groupby("invest")

    for item in inv_res:
        print(item[1])
        print()

    type_res = type_info.groupby("type")

    def to_code(var: str) -> str:
        return code_to_name(int(var.split(sep="+")[0]))

    for item in type_res:
        temp_df = item[1]
        res = temp_df["tags"].apply(to_code)
        pd.Series(res.unique()).to_csv("../data/cluster_res/type_{}_res.csv".format(item[0]), index=False)
        item[1].to_csv("../data/cluster_res/type_{}_raw.csv".format(item[0]), index=False)
    # obj.process_factor_encode_type_overall()
    # obj.plot_k_means_res_invest()
    pass


def disp_res():
    plt.savefig()
    pass


def preloading_data():
    codes = get_codes()
    for code in codes:
        get_fina_main(code)


if __name__ == '__main__':
    # read_type_df()
    # print(code_to_name(int("00503")))
    main_2()
    pass
