import pandas as pd


def extract_header(df, header_1, header_2) -> list:
    res = []
    for info_1, info_2 in zip(df[header_1], df[header_2]):
        res.append(str(info_1) + "+" + str(info_2))
    return res
