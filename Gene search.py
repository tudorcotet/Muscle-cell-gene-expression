from pathlib import Path
import pandas as pd
import numpy as np
import string
from fuzzywuzzy import fuzz


DATA_PATH = Path.cwd() / "data"

meat_df = pd.read_csv(DATA_PATH / "Cell-based meat genes.csv", header = 2)
meat_df
meat_genes = meat_df["Gene / Protein Name"].to_list()
meat_genes


expression_df = pd.read_csv(Path(DATA_PATH / "ExpressionGenes.txt"), header = 0, sep = "\t")
expression_df
gene_list = expression_df["ApprovedSymbol"].to_list()
gene_list



class GenePreprocessing(object):
    def __init__(self):
        self.cleaned_genes = []

    def to_upper(self, genes):
        text_upper = text.upper()
        return text_upper

    def remove_punct(self, text):
        text_cleaned = text.translate(None, string.punctuation)
        return text_cleaned

##De terminat


class GeneSearch(object):
    def __init__(self):
        self.found_genes = []
        self.remaining_names = []

    def initial_search(self, names, gene_list):
        found_genes = [name for name in names if name in gene_list]
        self.found_genes = found_genes
        remaining_names = [name for name in names if name not in self.found_genes]
        self.remaining_names = remaining_names
        return found_genes, remaining_names

    def fuzzy_search(self, names, gene_list, fuzzy_method = fuzz.token_set_ratio, similarity_index = 50):
        if not self.found_genes:
            self.initial_search(names, gene_list)

        remaining_gene_list = [gene for gene in gene_list if gene not in self.found_genes]
        test_dict = {}
        for name in self.remaining_names:
            similarities = [fuzzy_method(name, gene) for gene in remaining_gene_list]
            found_gene = remaining_gene_list[np.argmax(similarities)]

            if max(similarities) > similarity_index:
                self.found_genes.append(found_gene)
                self.remaining_names.remove(name)

            test_dict.update({name:[found_gene, max(similarities)]})

        return test_dict, self.remaining_names


names = meat_genes
genes = gene_list
found_genes, rem_names1 = GeneSearch().initial_search(names, genes)
len(found_genes)
len(rem_names)
dict, rem_names1 = GeneSearch().fuzzy_search(names, genes)
len(dict)
len(rem_names1)
###????????????####
