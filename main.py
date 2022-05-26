# from Mining.Plumber_Mining import *
import matplotlib.pyplot as plt

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
            res = analysis(code, is_save=True)

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
    # obj.process_factor_encode_type_overall()
    obj.plot_k_means_res_invest()
    pass


def disp_res():

    plt.savefig()
    pass


def preloading_data():
    codes = get_codes()
    for code in codes:
        get_fina_main(code)


if __name__ == '__main__':

    main_3()
    pass
