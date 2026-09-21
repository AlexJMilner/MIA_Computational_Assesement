import os, shutil, subprocess

import pandas as pd

from rdkit import Chem

BASE = r"C:\Users\alexj\OneDrive\MIA_Project"

EXE = os.path.join(BASE, "RetroPath.Cli.exe")

RULES = os.path.join(BASE, "retrorules_parsed.csv")

mol = {

    "GPP": "CC(=CCC/C(=C/COP(=O)(O)OP(=O)(O)O)/C)C",

    "geraniol": "CC(=CCC/C(=C/CO)/C)C",

    "8-hydroxygeraniol": r"C/C(=C\CO)/CC/C=C(\C)/CO",

    "8-oxogeranial": r"C/C(=C\C=O)/CC/C=C(\C)/C=O",

    "cis-trans-nepetalactol": "C[C@@H]1CC[C@@H]2[C@H]1[C@@H](OC=C2C)O",

    "7-deoxyloganetic acid": "C[C@H]1CC[C@H]2[C@@H]1[C@@H](OC=C2C(=O)O)O",

    "7-deoxyloganic acid": "C[C@H]1CC[C@H]2[C@@H]1[C@@H](OC=C2C(=O)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O",

    "loganic acid": "C[C@H]1[C@H](C[C@H]2[C@@H]1[C@@H](OC=C2C(=O)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O)O",

    "loganin": "C[C@H]1[C@H](C[C@H]2[C@@H]1[C@@H](OC=C2C(=O)OC)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O)O",

    "secologanin": "COC(=O)C1=CO[C@H]([C@@H]([C@@H]1CC=O)C=C)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O)O)O",

    "L-tryptophan": "N[C@@H](Cc1c[nH]c2ccccc12)C(=O)O",

    "tryptamine": "NCCc1c[nH]c2ccccc12",

    "strictosidine": "COC(=O)C1=CO[C@H]([C@@H]([C@@H]1C[C@H]2C3=C(CCN2)C4=CC=CC=C4N3)C=C)O[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O)O)O",

    "strictosidine aglycone": "COC(=O)C1=CO[C@H]([C@@H]([C@@H]1C[C@H]2C3=C(CCN2)C4=CC=CC=C4N3)C=C)O",

    "geissoschizine": r"C/C=C\1/CN2CCC3=C([C@@H]2C[C@@H]1C(C=O)C(=O)OC)NC4=CC=CC=C34",

    "stemmadenine": r"C/C=C4([C@@H]1(CC[NH+](CCC2(C3(/C=C\C=C/C(/NC(/[C@](C(OC)=O)(CO)1)=2)=3)))C4))",

    "stemmadenine acetate": r"C/C=C4([C@@H]1(CC[NH+](CCC2(C3(/C=C\C=C/C(/NC(/[C@](C(=O)OC)(COC(C)=O)1)=2)=3)))C4))",

    "precondylocarpine acetate": r"C/C=C\1/C=[N+]2CC[C@@H]1[C@](C3=C(CC2)C4=CC=CC=C4N3)(COC(=O)C)C(=O)OC",

    "dehydrosecodine": "CCC1=CN(CC=C1)CCC2=C(NC3=CC=CC=C32)C(=C)C(=O)OC",

    "catharanthine": "CCC1=C[C@H]2C[C@]3([C@@H]1N(C2)CCC4=C3NC5=CC=CC=C45)C(=O)OC",

    "tabersonine": r"CC[C@@]25(\C=C/C[NH+]4(CC[C@@]1(C3(/C=C\C=C/C(/NC\1=C(C2)/C(=O)OC)=3))[C@@H]45))",

    "16-hydroxytabersonine": r"CC[C@@]25(\C=C/C[NH+]4(CC[C@@]1(C3(/C=C\C(O)=C/C(/NC\1=C(C2)/C(=O)OC)=3))[C@@H]45))",

    "16-methoxytabersonine": r"CC[C@@]25(\C=C/C[NH+]4(CC[C@@]1(C3(/C=C\C(OC)=C/C(/NC\1=C(C2)/C(=O)OC)=3))[C@@H]45))",

    "(3R)-3-hydroxy-16-methoxy-2,3-dihydrotabersonine": r"CC[C@@]25(\C=C/C[NH+]4(CC[C@@]1(C3(/C=C\C(OC)=C/C(/N[C@H]1[C@](C(OC)=O)(O)C2)=3))[C@@H]45))",

    "deacetoxyvindoline": r"CC[C@@]25(\C=C/C[NH+]4(CC[C@@]1(C3(/C=C\C(OC)=C/C(/N(C)[C@H]1[C@](C(OC)=O)(O)C2)=3))[C@@H]45))",

    "17-O-deacetylvindoline": r"CC[C@@]25(\C=C/C[NH+]4(CC[C@@]1(C3(/C=C\C(OC)=C/C(/N(C)[C@H]1[C@](C(OC)=O)(O)[C@H](O)2)=3))[C@@H]45))",

    "vindoline": r"CC[C@@]25(\C=C/C[NH+]4(CC[C@@]1(C3(/C=C\C(OC)=C/C(/N(C)[C@H]1[C@](C(OC)=O)(O)[C@H](OC(=O)C)2)=3))[C@@H]45))",

    "vinblastine": r"CC[C@]7(O)(C[C@@H]6(C[C@](C(=O)OC)(C3(\C(OC)=C/C4(/N(C)[C@H]5([C@](C(OC)=O)(O)[C@H](OC(=O)C)[C@]2(CC)(\C=C/C[NH+]1(CC[C@]([C@@H]12)(C(/C=3)=4)5))))))C8(NC9(C(/C(\CC[NH+](C6)C7)=8)=C/C=C\C=9))))",

    "vincristine": r"CC[C@]7(O)(C[C@@H]6(C[C@](C(=O)OC)(C3(\C(OC)=C/C4(/N(C=O)[C@H]5([C@](C(OC)=O)(O)[C@H](OC(=O)C)[C@]2(CC)(\C=C/[NH+]1(CC[C@]([C@@H]12)(C(/C=3)=4)5))))))C8(NC9(C(/C(\CC[NH+](C6)C7)=8)=C/C=C\C=9))))",

    "anhydrovinblastine": r"CCC1=C[C@@H]2C[C@@](C3=C(CCN(C2)C1)C4=CC=CC=C4N3)(C5=C(C=C6C(=C5)[C@]78CCN9[C@H]7[C@@](C=CC9)([C@H]([C@@]([C@@H]8N6C)(C(=O)OC)O)OC(=O)C)CC)OC)C(=O)OC",

}

steps = [

    ("A","Iridoid","GES","GPP","geraniol"),

    ("A","Iridoid","G8H","geraniol","8-hydroxygeraniol"),

    ("A","Iridoid","8HGO","8-hydroxygeraniol","8-oxogeranial"),

    ("A","Iridoid","ISY","8-oxogeranial","cis-trans-nepetalactol"),

    ("A","Iridoid","IO","cis-trans-nepetalactol","7-deoxyloganetic acid"),

    ("A","Iridoid","7DLGT","7-deoxyloganetic acid","7-deoxyloganic acid"),

    ("A","Iridoid","7DLH","7-deoxyloganic acid","loganic acid"),

    ("A","Iridoid","LAMT","loganic acid","loganin"),

    ("A","Iridoid","SLS","loganin","secologanin"),

    ("A","Indole","TDC","L-tryptophan","tryptamine"),

    ("A","Central","SGD","strictosidine","strictosidine aglycone"),

    ("A","Central","GS","strictosidine aglycone","geissoschizine"),

    ("A","Central","GO-Redox1-Redox2","geissoschizine","stemmadenine"),

    ("A","Central","SAT","stemmadenine","stemmadenine acetate"),

    ("A","Central","ASO","stemmadenine acetate","precondylocarpine acetate"),

    ("A","Central","DPAS","precondylocarpine acetate","dehydrosecodine"),

    ("A","Catharanthine","CS","dehydrosecodine","catharanthine"),

    ("A","Vindoline","TS","dehydrosecodine","tabersonine"),

    ("A","Vindoline","T16H","tabersonine","16-hydroxytabersonine"),

    ("A","Vindoline","16OMT","16-hydroxytabersonine","16-methoxytabersonine"),

    ("A","Vindoline","T3O-T3R","16-methoxytabersonine","(3R)-3-hydroxy-16-methoxy-2,3-dihydrotabersonine"),

    ("A","Vindoline","NMT","(3R)-3-hydroxy-16-methoxy-2,3-dihydrotabersonine","deacetoxyvindoline"),

    ("A","Vindoline","D4H","deacetoxyvindoline","17-O-deacetylvindoline"),

    ("A","Vindoline","DAT","17-O-deacetylvindoline","vindoline"),

    ("A","Late","Vincristine Formation","vinblastine","vincristine"),

    ("A","Late","Vinblastine Formation","anhydrovinblastine","vinblastine"),

    ("B","Central","STR",["tryptamine","secologanin"],"strictosidine"),

    ("B","Dimer","Catharanthine-Vindoline coupling",
     ["catharanthine","vindoline"],"anhydrovinblastine")

]

def inc(name):

    m = Chem.MolFromSmiles(mol[name])

    if m is None:

        raise ValueError("Bad SMILES: " + name)

    return Chem.MolToInchi(m)

out = []

for batch, branch, name, parent, target in steps:

    parents = parent if isinstance(parent, list) else [parent]

    pd.DataFrame(

        [[target, inc(target)]],

        columns=["Name", "InChI"]

    ).to_csv(os.path.join(BASE, "source.csv"), index=False)

    pd.DataFrame(

        [[p, inc(p)] for p in parents],

        columns=["Name", "InChI"]

    ).to_csv(os.path.join(BASE, "sink.csv"), index=False)

    rdir = os.path.join(BASE, "results")

    if os.path.exists(rdir):

        shutil.rmtree(rdir)

    run = subprocess.run(

        [EXE, RULES,

         os.path.join(BASE, "source.csv"),

         os.path.join(BASE, "sink.csv"),

         "1"],

        cwd=BASE

    )

    file = os.path.join(rdir, "results.csv")

    if run.returncode != 0 or not os.path.exists(file):

        out.append([batch, branch, name, 0, 0, "ERROR"])

        continue

    df = pd.read_csv(file)

    df["Score"] = pd.to_numeric(df["Score"], errors="coerce")

    unique = (

        df.sort_values("Score", ascending=False)

        .drop_duplicates("Product InChI")

        .reset_index(drop=True)

    )

    hits = unique[unique["In Sink"].astype(str) == "1"]

    needed = len(parents)

    recovered = len(hits) >= needed

    out.append([

        batch,

        branch,

        name,

        len(unique),

        len(hits),

        "Recovered" if recovered else "Not recovered"

    ])

summary = pd.DataFrame(out, columns=[

    "Batch", "Branch", "Step",

    "Unique Products", "Sink Hits", "Result"

])

summary.to_csv(

    os.path.join(BASE, "mia_retropath_summary.csv"),

    index=False

)

print("\nFINAL SUMMARY\n")

print(summary.to_string(index=False))

for batch in ["A", "B"]:

    valid = summary[

        (summary["Batch"] == batch) &

        (summary["Result"] != "ERROR")

    ]

    if len(valid):

        n = (valid["Result"] == "Recovered").sum()

        print(f"\nBatch {batch}: {n}/{len(valid)} = {100*n/len(valid):.1f}%")