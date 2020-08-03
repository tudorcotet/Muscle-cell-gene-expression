import requests
import urllib.request
from bs4 import BeautifulSoup
from typing import List
from pathlib import Path

GEN_PATH = Path()



def download_ramilowski(url = "https://fantom.gsc.riken.jp/5/suppl/Ramilowski_et_al_2015/data", file_name = ""):
    if os.path.exists("data") is False:
        os.makedirs(os.getcwd() + "/data")

    if file_name is not "":
        if os.path.exists("data/" + file_name):
            raise ValueError(file_name + " already downloaded")
        else:
            urllib.request.urlretrieve(url + "/" + file_name, "./data/" + file_name)

    else:
        content = requests.get(url)
        soup = BeautifulSoup(content.text, "html.parser")
        hyperlinks = soup.find_all("a")
        link_names = {link.text for link in hyperlinks if ".txt" in str(link)}

        for link in link_names:
            download_url = url + "/" + link
            if os.path.exists("data/"  + link):
                continue

            else:
                urllib.request.urlretrieve(url + "/" + link, "./data/" + link)


download_ramilowski()

expression_genes = pd.read_csv("./data/ExpressionGenes.txt", header = 0, sep = "\t")
expression_genes
