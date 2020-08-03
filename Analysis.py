import pandas as pd
import numpy as np

expression_df = pd.read_csv("./data/ExpressionGenes.txt", header = 0, sep = "\t")
expression_df


muscle_genes = pd.read_csv("./data/Muscle differentiation genes.csv", header = 0, sep = ",")
muscle_genes = muscle_genes["Gene symbol"].tolist()
muscle_genes = [gene.upper() for gene in muscle_genes]
muscle_genes


muscle_expression = expression_df.filter(like = "Muscle")
muscle_expression = muscle_expression.assign(Gene = expression_df["ApprovedSymbol"])
muscle_expression = muscle_expression[muscle_expression["Gene"].isin(muscle_genes)]

muscle_expression
