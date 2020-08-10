from pathlib import Path
import requests
import urllib.request
from bs4 import BeautifulSoup


URL = "https://fantom.gsc.riken.jp/5/suppl/Ramilowski_et_al_2015/data"
GEN_PATH = Path.cwd()
DATA_PATH = Path(GEN_PATH / "data")

#Download datasets from Ramilowski et al. 2015
def download_ramilowski(url: str, file_name: str or None = None) -> None:
    """
    Download datasets from Ramilowski et al. 2015

       args:
          url(str) - general data url containing all .txt datasets as hyperlinks
          file_name(str or None) - single file to be downloaded from data url
                                 - name + ".txt"
                                 - if None -> parses and downloads all
       returns:
          None
    """

    if DATA_PATH.exists() is False:
        DATA_PATH.mkdir()

    if file_name is None:
        content = requests.get(url)
        soup = BeautifulSoup(content.text, "html.parser")
        hyperlinks = soup.find_all("a")
        link_names = {link.text for link in hyperlinks if ".txt" in str(link)}
        for link in link_names:
            download_url = url + "/" + link
            if Path(DATA_PATH / link).exists():
                continue
            else:
                urllib.request.urlretrieve(url + "/" + link, DATA_PATH / link)
    else:
        if Path(DATA_PATH / file_name).exists():
            raise ValueError(file_name + " already downloaded")
        else:
            urllib.request.urlretrieve(url + "/" + file_name, DATA_PATH / filename)



if __name__ == "__main__":
    download_ramilowski(URL)

    import pandas as pd
    expression_genes = pd.read_csv("./data/ExpressionGenes.txt", header = 0, sep = "\t")
    expression_genes
