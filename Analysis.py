import pandas as pd
import numpy as np
from Ramilowski import download_ramilowski
from pathlib import Path

#Data wrangling - import the ExpressionGenes.txt file from Ramilowski et al. 2015, filter genes based on `Muscle differentiation genes`.csv
#As putea sa mut intr-o functie in Ramilowski.py
URL = "https://fantom.gsc.riken.jp/5/suppl/Ramilowski_et_al_2015/data"
download_ramilowski(URL)
DATA_PATH = Path.cwd() / "data"

expression_df = pd.read_csv(Path(DATA_PATH / "ExpressionGenes.txt"), header = 0, sep = "\t")
expression_df.dtypes


muscle_genes = (pd.read_csv(DATA_PATH / "Muscle differentiation genes.csv", header = 0, sep = ",")
                  ["Gene symbol"].tolist()
               )
muscle_genes = [gene.upper() for gene in muscle_genes]
muscle_genes

df = (pd.DataFrame(expression_df[expression_df["ApprovedSymbol"].isin(muscle_genes)])
                     .transpose()
                     .reset_index()
                  )

df.columns = df.iloc[0,0:]
df = df.drop(0)
df.rename(columns = {"ApprovedSymbol":"Cell type"}, inplace = True)
df["Muscle cells"] = np.where(df['Cell type'].str.contains("Muscle") , "Yes", np.where(~df["Cell type"].str.contains("Muscle"), "No", "Error"))
df = df.set_index("Cell type")
df[df.columns.difference(["Muscle cells"])] = df[df.columns.difference(["Muscle cells"])].astype("float")
df["Muscle cells"] = df["Muscle cells"].astype("category")
#df.assign(Muscle cell = "")
#df.loc[df["Cell type"].str.contains("Muscle"), "Muscle cells"] = "Yes"
#df.loc[~df["Cell type"].str.contains("Muscle"), "Muscle cells"] = "No"
df.to_csv(Path(Path.cwd() / "data" / "WrangledDf.csv"), index = True)


mean_table = df.groupby("Muscle cells", as_index = False).mean().melt(id_vars = "Muscle cells")
mean_table.rename(columns = {0: "Genes", "value": "Expression"}, inplace = True)
mean_table["Genes"] = mean_table["Genes"].astype("category")
mean_table["Expression"] = mean_table["Expression"].astype("float")
#(mean_table.groupby(["Genes"])
         # .max()
          #.assign(Min = mean_table.groupby(["Genes"]).min()))
mean_table_wrangled = mean_table.drop(mean_table[mean_table["Expression"] < 2].index)
mean_table_wrangled


import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline


fig = plt.figure(figsize=(15, 8))
sns.barplot(x="Expression", y="Genes", hue = "Muscle cells", data = mean_table_wrangled)
fig.savefig("ExpressionBarplot.png")

muscle_df = df[df["Muscle cells"] == "Yes"]
sns.kdeplot(muscle_df["MYOG"], bw = 0.1)
cells_df = df[df["Muscle cells"] == "No"]
sns.kdeplot(cells_df["MYOG"], bw = 0.1)
