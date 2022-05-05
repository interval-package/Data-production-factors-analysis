

from bs4 import BeautifulSoup
import requests


if __name__ == '__main__':

    req = requests.get("https://zhuanlan.zhihu.com/p/38107460")
    soup = BeautifulSoup(req.content, features="html.parser")
    print(soup.get_text())
    print(soup.contents)
    pass
