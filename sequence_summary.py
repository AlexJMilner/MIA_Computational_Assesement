import pandas as pd
from Bio import AlignIO

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

results = []

for enzyme, accession in enzymes.items():

    hits = (
        df[df["qseqid"].str.contains(accession, na=False)]
        .sort_values("bitscore", ascending=False)
        .drop_duplicates("sseqid")
        .head(5)
    )

    alignment = AlignIO.read(
        base + fr"\{enzyme}_MSA_aligned.fasta",
        "fasta"
    )

    conserved = 0

    for i in range(alignment.get_alignment_length()):
        column = alignment[:, i]
        residues = [aa for aa in column if aa != "-"]

        if len(residues) == len(alignment) and len(set(residues)) == 1:
            conserved += 1

    results.append({
        "Enzyme": enzyme,
        "Mean_identity": hits["pident"].mean(),
        "Mean_query_coverage": hits["qcovs"].mean(),
        "Conserved_positions": conserved
    })

summary = pd.DataFrame(results)

print(summary)

summary.to_csv(
    base + r"\sequence_conservation_summary.csv",
    index=False
)