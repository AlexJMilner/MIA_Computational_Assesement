# MIA Pathway Intermediates
# Source: Miettinen et al. 2014 Nature Communications

intermediates = {
    "geraniol": "OC/C=C(/CCC=C(C)C)C",  # SMILES
    "10-hydroxygeraniol": "OCC(=CCO)CCC=C(C)C",
    "secologanin": "O=C(OC)C1=COC(OC2OC(CO)C(O)C(O)C2O)C1CC=C",
    "tryptamine": "NCCc1c[nH]c2ccccc12",
    "strictosidine": "O=C(OC)[C@@H]1[C@H](CC=C)C=COC1OC1OC(CO)C(O)C(O)C1O",
    "catharanthine": "O=C(OC)[C@]12CC[C@@H](CC=C)[C@H]1N1CCc3c1c2[nH]c2ccccc32",
    "tabersonine": "O=C(OC)[C@]12CC[C@@H](CC=C)[C@H]1N1CCc3c1c2[nH]c2ccccc32",
    "vindoline": "O=C(OC)[C@]12CC[C@@H](CC)[C@H]1N1c3[nH]c4ccccc4c3CC1C2OC(=O)C",
    "vinblastine": "O=C(OC)C1(O)CC(CC=C)CN2CCc3c2[nH]c2ccccc32"
}

print(f"Loaded {len(intermediates)} MIA pathway intermediates")
for name, smiles in intermediates.items():
    print(f"  {name}: {smiles}")