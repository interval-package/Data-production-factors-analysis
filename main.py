# from Mining.Plumber_Mining import *
import pickle
from NetData_req.FetchData import *


def readFile():
    with open("obj.pickle", "rb") as p_in:
        obj = pickle.load(p_in)
    return obj


if __name__ == '__main__':
    codes = get_codes()
    # req_profit_data(codes)
    # req_operation_data(codes)
    req_performance_express_report()
    pass
