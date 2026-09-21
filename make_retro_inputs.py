import pandas as pd
from rdkit import Chem

tabersonine_smiles = r"CC[C@@]25(\C=C/C[NH+]4(CC[C@@]1(C3(/C=C\C=C/C(/NC\1=C(C2)/C(=O)OC)=3))[C@@H]45))"

hydroxy16_smiles = r"CC[C@@]25(\C=C/C[NH+]4(CC[C@@]1(C3(/C=C\C(\O)=C/C(/NC\1=C(C2)/C(=O)OC)=3))[C@@H]45))"

tab_mol = Chem.MolFromSmiles(tabersonine_smiles)
hydroxy_mol = Chem.MolFromSmiles(hydroxy16_smiles)

tab_inchi = Chem.MolToInchi(tab_mol)
hydroxy_inchi = Chem.MolToInchi(hydroxy_mol)

print("TABERSONINE:")
print(tab_inchi)

print("\n16-HYDROXYTABERSONINE:")
print(hydroxy_inchi)

pd.DataFrame([{
    "Name": "16-hydroxytabersonine",
    "InChI": hydroxy_inchi
}]).to_csv("source.csv", index=False)

pd.DataFrame([{
    "Name": "tabersonine",
    "InChI": tab_inchi
}]).to_csv("sink.csv", index=False)

print("\nClean source.csv and sink.csv written.")