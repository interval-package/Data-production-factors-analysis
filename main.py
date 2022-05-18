from Mining.Plumber_Mining import *
import pickle


def readFile():
    with open("obj.pickle", "rb") as p_in:
        obj = pickle.load(p_in)
    return obj


if __name__ == '__main__':
    for pdf in get_pdf_name():
        print(pdf)
        obj = PdfPlumberMiner(pdf, "./res.xlsx")
        obj.bf_mining(obj.deep_analyze)
        obj.disp_self_res()
        with open("obj.pickle", "wb") as out:
            pickle.dump(obj, out)
        input()
    pass
