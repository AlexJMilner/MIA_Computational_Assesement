import pandas as pd

file = r"C:\Users\alexj\OneDrive\MIA_Project\BLAST_summary.csv"

df = pd.read_csv(file)

outliers = df[
    (df["pident"] < 70) |
    (df["qcovs"] < 80) |
    (df["strong_homologues"] < 10)
]

print(outliers.to_string(index=False))