from Process_Site.main_prof.proess_factors import *
from DataBase.NetData_req.tushare_home import *


class MainBzReTag:
    def __init__(self):
        pass

    @staticmethod
    def preloading():
        codes = get_codes()
        for code in get_codes():
            res = get_main_bz_by_year(code)
        pass

    key_words = ["信息", "数据"]

    def is_fit_keys(self, tar: str):
        for key in self.key_words:
            if key in tar:
                return True
        return False
