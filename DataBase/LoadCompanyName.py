import os

source_data_path = "D:\\coding\\PythonProjects\\data\\pdfs"


def get_pdf_name(file_dir=source_data_path):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.PDF':
                L.append(os.path.join(root, file))
    return L


# def get_pdf_name(data_path=source_data_path):
#     res = os.walk(data_path)
#     return


if __name__ == '__main__':
    pass
