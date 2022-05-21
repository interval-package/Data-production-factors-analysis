import pandas as pd
import os

dir_main_prof = os.path.join("..", "data", "main_prof")


def read_csv_data(code, file_dir=dir_main_prof):
    """
    :car tar_path: the file path containing the data
    :return return a list of dataframe
    """
    path = os.path.join(file_dir, "{}.csv".format(code))
    print(path)
    res = pd.read_csv(path)
    return res
