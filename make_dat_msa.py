import pandas as pd
from Bio import Entrez, SeqIO
from io import StringIO
import time

Entrez.email = "alexjmilner12@gmail.com"

base = r"C:\Users\alexj\OneDrive\MIA_Project"

df = pd.read_csv(base + r"\BLAST_no_Catharanthus.csv")

# DAT results only
dat = df[df["qseqid"].str.contains("Q9ZTK5")]

# Best 5 homologues
hits = dat.sort_values("bitscore", ascending=False)["sseqid"].head(5).tolist()

print("Top DAT hits:")
print(hits)

records = []

# Original DAT sequence from NCBI
ids = ["Q9ZTK5"] + hits

for x in ids:
    print("Downloading:", x)

    for attempt in range(5):
        try:
            h = Entrez.efetch(
                db="protein",
                id=x,
                rettype="fasta",
                retmode="text"
            )

            record = SeqIO.read(StringIO(h.read()), "fasta")
            records.append(record)
            break

        except Exception:
            print("Retrying...")
            time.sleep(5)

SeqIO.write(
    records,
    base + r"\DAT_MSA_input.fasta",
    "fasta"
)

print("\nDONE")
print("Sequences:", len(records))
print("Saved: DAT_MSA_input.fasta")