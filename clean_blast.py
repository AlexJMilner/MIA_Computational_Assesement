import pandas as pd

base = r"C:\Users\alexj\OneDrive\MIA_Project"

raw = base + r"\A4V8FS7U014-Alignment-HitTable.csv"
cache = base + r"\organisms.csv"

cols = [
    "qseqid","sseqid","pident","length","mismatch","gapopen",
    "qstart","qend","sstart","send","evalue","bitscore","qcovs"
]

df = pd.read_csv(raw, header=None, names=cols)

org = dict(pd.read_csv(cache).values)

df["organism"] = df["sseqid"].map(org).fillna("Unknown")

clean = df[
    ~df["organism"].str.startswith("Catharanthus", na=False)
]

clean.to_csv(
    base + r"\BLAST_no_Catharanthus.csv",
    index=False
)

print("Original rows:", len(df))
print("Clean rows:", len(clean))
print("Queries:", clean["qseqid"].nunique())
print("Unknown:", (clean["organism"] == "Unknown").sum())