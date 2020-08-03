import pandas as pd
import numpy as np

expression_df = pd.read_csv("./data/ExpressionGenes.txt", header = 0, sep = "\t")
expression_df

muscle_genes = (pd.read_csv("./Muscle differentiation genes - Genes.csv", header = 0, sep = ",")
                  ["Gene symbol"].tolist()
               )
muscle_genes = [gene.upper() for gene in muscle_genes]
muscle_genes

muscle_expression = (expression_df.filter(like = "Muscle")
                                  .assign(Gene = expression_df["ApprovedSymbol"])
                    )
muscle_expression = muscle_expression[muscle_expression["Gene"].isin(muscle_genes)]
muscle_expression
