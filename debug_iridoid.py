import os, shutil, subprocess, pandas as pd
from rdkit import Chem

BASE = r"C:\Users\alexj\OneDrive\MIA_Project"
EXE = os.path.join(BASE, "RetroPath.Cli.exe")
RULES = os.path.join(BASE, "retrorules_parsed.csv")

mol = {
    "8-oxogeranial": r"C/C(=C\C=O)/CC/C=C(\C)/C=O",
    "cis-trans-nepetalactol": "C[C@@H]1CC[C@@H]2[C@H]1[C@@H](OC=C2C)O",
    "7-deoxyloganetic acid": "C[C@H]1CC[C@H]2[C@@H]1[C@@H](OC=C2C(=O)O)O",
    "7-deoxyloganic acid": "C[C@H]1CC[C@H]2[C@@H]1[C@@H](OC=C2C(=O)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O",
    "loganic acid": "C[C@H]1[C@H](C[C@H]2[C@@H]1[C@@H](OC=C2C(=O)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O)O",
    "loganin": "C[C@H]1[C@H](C[C@H]2[C@@H]1[C@@H](OC=C2C(=O)OC)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O)O",
    "secologanin": "COC(=O)C1=CO[C@H]([C@@H]([C@@H]1CC=O)C=C)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O)O)O"
}

steps = [
    ("ISY", "8-oxogeranial", "cis-trans-nepetalactol"),
    ("IO", "cis-trans-nepetalactol", "7-deoxyloganetic acid"),
    ("7DLGT", "7-deoxyloganetic acid", "7-deoxyloganic acid"),
    ("7DLH", "7-deoxyloganic acid", "loganic acid"),
    ("LAMT", "loganic acid", "loganin"),
    ("SLS", "loganin", "secologanin"),
]

def inchi(name):
    m = Chem.MolFromSmiles(mol[name])
    if m is None:
        raise ValueError("BAD SMILES: " + name)
    return Chem.MolToInchi(m)

for name, parent, target in steps:
    print("\n" + "="*60)
    print(name, ":", target, "->", parent)

    try:
        source = inchi(target)
        sink = inchi(parent)
        print("RDKit inputs: OK")
    except Exception as e:
        print(e)
        continue

    pd.DataFrame([[target, source]], columns=["Name","InChI"]).to_csv(BASE+r"\source.csv", index=False)
    pd.DataFrame([[parent, sink]], columns=["Name","InChI"]).to_csv(BASE+r"\sink.csv", index=False)

    rdir = BASE+r"\results"
    if os.path.exists(rdir):
        shutil.rmtree(rdir)

    run = subprocess.run(
        [EXE, RULES, BASE+r"\source.csv", BASE+r"\sink.csv", "1"],
        cwd=BASE
    )

    result = rdir+r"\results.csv"

    if run.returncode != 0:
        print("RESULT: RetroPath crashed")
    elif not os.path.exists(result):
        print("RESULT: no results.csv")
    else:
        df = pd.read_csv(result)
        hits = (df["In Sink"].astype(str) == "1").sum()
        print("RESULT: completed")
        print("Candidates:", len(df))
        print("Sink hits:", hits)