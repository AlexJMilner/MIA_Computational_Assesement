import os, ast, shutil, subprocess
import pandas as pd
from rdkit import Chem

BASE = r"C:\Users\alexj\OneDrive\MIA_Project"
MAIN = os.path.join(BASE, "run_mia_retropath.py")
EXE = os.path.join(BASE, "RetroPath.Cli.exe")
RULES = os.path.join(BASE, "retrorules_parsed.csv")

# Load mol + steps from main script without running it
tree = ast.parse(open(MAIN, encoding="utf-8").read())
for node in tree.body:
    if isinstance(node, ast.Assign):
        if any(getattr(x, "id", "") == "mol" for x in node.targets):
            mol = ast.literal_eval(node.value)
        if any(getattr(x, "id", "") == "steps" for x in node.targets):
            steps = ast.literal_eval(node.value)

bad = {"ISY","IO","7DLGT","7DLH","LAMT","SLS","STR"}

def inc(smiles):
    return Chem.MolToInchi(Chem.MolFromSmiles(smiles))

dummy = inc("CCO")   # ethanol: unrelated sink

def run_test(target, parents, use_dummy):
    pd.DataFrame(
        [[target, inc(mol[target])]],
        columns=["Name","InChI"]
    ).to_csv(os.path.join(BASE,"source.csv"), index=False)

    sinks = [["dummy",dummy]] if use_dummy else [
        [p,inc(mol[p])] for p in parents
    ]

    pd.DataFrame(sinks,columns=["Name","InChI"]).to_csv(
        os.path.join(BASE,"sink.csv"),index=False
    )

    rdir = os.path.join(BASE,"results")
    if os.path.exists(rdir):
        shutil.rmtree(rdir)

    r = subprocess.run(
        [EXE,RULES,
         os.path.join(BASE,"source.csv"),
         os.path.join(BASE,"sink.csv"),"1"],
        cwd=BASE,
        capture_output=True,
        text=True
    )

    text = r.stdout + r.stderr

    if "Sequence contains more than one element" in text:
        return "CRASH: duplicate/matching"
    if r.returncode != 0:
        return "CRASH: other"
    if not os.path.exists(os.path.join(rdir,"results.csv")):
        return "NO RESULTS"
    return "OK"

print("\nDIAGNOSTIC\n")

for batch,branch,name,parent,target in steps:
    if name not in bad:
        continue

    parents = parent if isinstance(parent,list) else [parent]

    real = run_test(target,parents,False)
    dummy_result = run_test(target,parents,True)

    print(f"{name:6} | real sink: {real:25} | dummy sink: {dummy_result}")