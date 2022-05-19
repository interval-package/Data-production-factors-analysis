import tushare as ts

pro = ts.pro_api("2bdcac3df7abe5a51cec2461d8ccb4d05c208f9374b1b33c332a6585")

df = pro.fina_mainbz(ts_code='000627.SZ', type='P')

print(df)

