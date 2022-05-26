import pandas as pd

from DataBase.Load_csv_Data import *
from Process_Site.main_prof.MainBzReTag import MainBzReTag


class DetailData:
    def __init__(self):
        self.data = preloading_detail_factor()
        pass

    @staticmethod
    def load_csv_data(code):
        res = pd.read_csv("../data/detail_res/{}.csv".format(code))
        return res

    def init_process(self):
        pass
