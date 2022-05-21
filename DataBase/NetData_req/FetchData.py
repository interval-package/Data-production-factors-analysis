import baostock as bs
import pandas as pd
import xlrd
import os.path as path

# from DataBase.DataBaseReader import *

# output = DataBaseReader()

func_dict_data = {
    "profit_data": bs.query_profit_data,
    "operation_data": bs.query_operation_data,
}

func_dict_report = {
    "performance_express_report": bs.query_performance_express_report,
}


def get_codes():
    workBook = xlrd.open_workbook(path.join(".", "DataBase", "NetData_req", "data.xls"))
    sheet1_content1 = workBook.sheets()[0]
    cols = sheet1_content1.col_values(0)
    return cols[1:]


tar_years = [i for i in range(2017, 2021)]


def req_profit_data(codes: list):
    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    col = bs.query_profit_data(code="sz.000503", year=2017, quarter=2)

    # 查询季频估值指标盈利能力
    profit_list = []
    for code in codes:
        for year in tar_years:
            for quarter in range(1, 4):
                print("now is " + code + " in " + str(year) + " of " + str(quarter))
                rs_profit = bs.query_profit_data(code="sz." + code, year=year, quarter=quarter)
                while (rs_profit.error_code == '0') & rs_profit.next():
                    profit_list.append(rs_profit.get_row_data())
    result_profit = pd.DataFrame(profit_list, columns=col.fields)
    # 打印输出
    print(result_profit)
    # 结果集输出到csv文件
    result_profit.to_csv("./data/profit_data.csv", encoding="gbk", index=False)

    # 登出系统
    bs.logout()


def req_operation_data(codes: list):
    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    col = bs.query_operation_data(code="sz.000503", year=2017, quarter=2)

    # 查询季频估值指标盈利能力
    profit_list = []
    for code in codes:
        for year in tar_years:
            for quarter in range(1, 4):
                print("now is " + code + " in " + str(year) + " of " + str(quarter))
                rs_profit = bs.query_operation_data(code="sz." + code, year=year, quarter=quarter)
                while (rs_profit.error_code == '0') & rs_profit.next():
                    profit_list.append(rs_profit.get_row_data())
    result_profit = pd.DataFrame(profit_list, columns=col.fields)
    # 打印输出
    print(result_profit)
    # 结果集输出到csv文件
    result_profit.to_csv("./data/operation_data.csv", encoding="gbk", index=False)
    # 登出系统
    bs.logout()


def req_data_base(codes: list, data_type):
    func = func_dict_data[data_type]
    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    col = func(code="sz.000503", year=2017, quarter=2)

    # 查询季频估值指标盈利能力
    data_list = []
    for code in codes:
        for year in tar_years:
            for quarter in range(1, 4):
                print("now is " + code + " in " + str(year) + " of " + str(quarter))
                res = func(code="sz." + code, year=year, quarter=quarter)
                while (res.error_code == '0') & res.next():
                    data_list.append(res.get_row_data())
    result_data = pd.DataFrame(data_list, columns=col.fields)
    # 打印输出
    print(result_data)
    # 结果集输出到csv文件
    result_data.to_csv("./data/{}.csv".format(data_type), encoding="gbk", index=False)
    # 登出系统
    bs.logout()

    return


def req_performance_express_report():
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    #### 获取公司业绩快报 ####
    rs = bs.query_performance_express_report("sh.600000", start_date="2015-01-01", end_date="2021-12-31")
    print('query_performance_express_report respond error_code:' + rs.error_code)
    print('query_performance_express_report respond  error_msg:' + rs.error_msg)

    result_list = []
    while (rs.error_code == '0') & rs.next():
        result_list.append(rs.get_row_data())
        # 获取一条记录，将记录合并在一起
    result = pd.DataFrame(result_list, columns=rs.fields)
    #### 结果集输出到csv文件 ####
    result.to_csv("./performance_express_report.csv", encoding="gbk", index=False)
    print(result)
