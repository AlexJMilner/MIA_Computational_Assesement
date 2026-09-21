import pandas as pd
from Bio import Entrez, SeqIO
from io import StringIO
import time

Entrez.email = "alexjmilner12@gmail.com"

base = r"C:\Users\alexj\OneDrive\MIA_Project"
df = pd.read_csv(base + r"\BLAST_no_Catharanthus.csv")

enzymes = {
    "DAT": "Q9ZTK5",
    "SAT": "A0A2P1GIW7",
    "SGD": "Q9M7N7",
    "D4H": "O04847",
    "T16H": "U5HKE8",
    "T3R": "A0A161CAI1",
    "T3O": "I1TEM1",
}

def fetch_fasta(accession):
    for attempt in range(5):
        try:
            h = Entrez.efetch(
                db="protein",
                id=accession,
                rettype="fasta",
                retmode="text"
            )
            return SeqIO.read(StringIO(h.read()), "fasta")
        except Exception:
            print("retrying:", accession)
            time.sleep(5)
    return None

for enzyme, query_acc in enzymes.items():
    print("\n" + enzyme)

    hits = (
        df[df["qseqid"].str.contains(query_acc, na=False)]
        .sort_values("bitscore", ascending=False)
        .drop_duplicates("sseqid")
        .head(5)["sseqid"]
        .tolist()
    )

    ids = [query_acc] + hits
    records = []

    for accession in ids:
        print("downloading:", accession)
        record = fetch_fasta(accession)

        if record:
            records.append(record)

    output = base + fr"\{enzyme}_MSA_input.fasta"
    SeqIO.write(records, output, "fasta")

    print("saved:", enzyme + "_MSA_input.fasta")
    print("sequences:", len(records))

print("\nDONE")