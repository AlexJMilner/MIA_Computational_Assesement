import pandas as pd

base = r"C:\Users\alexj\OneDrive\MIA_Project"
file = base + r"\BLAST_no_Catharanthus.csv"

df = pd.read_csv(file)

strong = df[
    (df["pident"] >= 40) &
    (df["qcovs"] >= 70) &
    (df["evalue"] <= 1e-5)
]

best = (
    df.sort_values(["qseqid", "bitscore"], ascending=[True, False])
      .groupby("qseqid")
      .first()
      .reset_index()
)

counts = (
    strong.groupby("qseqid")
          .size()
          .reset_index(name="strong_homologues")
)

summary = best[
    ["qseqid", "sseqid", "organism", "pident", "qcovs", "evalue", "bitscore"]
].merge(counts, on="qseqid", how="left")

summary["strong_homologues"] = (
    summary["strong_homologues"].fillna(0).astype(int)
)

summary.to_csv(
    base + r"\BLAST_summary.csv",
    index=False
)

print(summary.to_string(index=False))
print("\nSaved: BLAST_summary.csv")