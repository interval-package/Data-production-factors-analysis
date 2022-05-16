

import pdfplumber
import pandas as pd


def read_pdf(read_path, save_path):
    pdf_2020 = pdfplumber.open(read_path)
    result_df = pd.DataFrame()
    for page in pdf_2020.pages:
        table = page.extract_table()
        if table is not None:
            df_detail = pd.DataFrame(table[1:], columns=table[0])
            print(df_detail)
            # result_df = pd.concat([df_detail, result_df], ignore_index=True)



if __name__ == '__main__':
    read_pdf("D:\coding\PythonProjects\data\pdfs\\000503 国新健康 2021.PDF",
             "D:\coding\PythonProjects\data\pdfs\\000503 国新健康 2021.csv")
    pass
