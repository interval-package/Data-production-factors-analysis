from Mining.Plumber_Mining import *

if __name__ == '__main__':
    for pdf in get_pdf_name():
        print(pdf)
        obj = PdfPlumberMiner(pdf,
                              "./res.xlsx")
        obj.bf_mining(obj.analyze)
    pass
