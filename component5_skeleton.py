import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

edges = [
    ("GPP","Geraniol","GES"),
    ("Geraniol","8-Hydroxygeraniol","G8H"),
    ("8-Hydroxygeraniol","8-Oxogeranial","8HGO"),
    ("8-Oxogeranial","cis-trans-Nepetalactol","ISY"),
    ("cis-trans-Nepetalactol","7-Deoxyloganetic acid","IO"),
    ("7-Deoxyloganetic acid","7-Deoxyloganic acid","7DLGT"),
    ("7-Deoxyloganic acid","Loganic acid","7DLH"),
    ("Loganic acid","Loganin","LAMT"),
    ("Loganin","Secologanin","SLS"),

    ("L-Tryptophan","Tryptamine","TDC"),

    ("Secologanin","Strictosidine","STR"),
    ("Tryptamine","Strictosidine","STR"),

    ("Strictosidine","Strictosidine aglycone","SGD"),
    ("Strictosidine aglycone","Geissoschizine","GS"),
    ("Geissoschizine","Stemmadenine","GO-Redox1-Redox2"),
    ("Stemmadenine","Stemmadenine acetate","SAT"),
    ("Stemmadenine acetate","Precondylocarpine acetate","ASO"),
    ("Precondylocarpine acetate","Dehydrosecodine","DPAS"),

    ("Dehydrosecodine","Catharanthine","CS"),
    ("Dehydrosecodine","Tabersonine","TS"),

    ("Tabersonine","16-Hydroxytabersonine","T16H"),
    ("16-Hydroxytabersonine","16-Methoxytabersonine","16OMT"),
    ("16-Methoxytabersonine","3-Hydroxy-16-methoxy-2,3-dihydrotabersonine","T3O-T3R"),
    ("3-Hydroxy-16-methoxy-2,3-dihydrotabersonine","Deacetoxyvindoline","NMT"),
    ("Deacetoxyvindoline","17-O-Deacetylvindoline","D4H"),
    ("17-O-Deacetylvindoline","Vindoline","DAT"),

    ("Catharanthine","Anhydrovinblastine","PRX1"),
    ("Vindoline","Anhydrovinblastine","PRX1"),

    ("Vinblastine","Vincristine","Vincristine Formation")
]

for source, target, enzyme in edges:
    G.add_edge(source, target, enzyme=enzyme)

pos = {
    "GPP": (-2,16),
    "Geraniol": (-2,15),
    "8-Hydroxygeraniol": (-2,14),
    "8-Oxogeranial": (-2,13),
    "cis-trans-Nepetalactol": (-2,12),
    "7-Deoxyloganetic acid": (-2,11),
    "7-Deoxyloganic acid": (-2,10),
    "Loganic acid": (-2,9),
    "Loganin": (-2,8),
    "Secologanin": (-2,7),

    "L-Tryptophan": (2,9),
    "Tryptamine": (2,8),

    "Strictosidine": (0,6),
    "Strictosidine aglycone": (0,5),
    "Geissoschizine": (0,4),
    "Stemmadenine": (0,3),
    "Stemmadenine acetate": (0,2),
    "Precondylocarpine acetate": (0,1),
    "Dehydrosecodine": (0,0),

    "Catharanthine": (-2,-1),
    "Tabersonine": (2,-1),

    "16-Hydroxytabersonine": (2,-2),
    "16-Methoxytabersonine": (2,-3),
    "3-Hydroxy-16-methoxy-2,3-dihydrotabersonine": (2,-4),
    "Deacetoxyvindoline": (2,-5),
    "17-O-Deacetylvindoline": (2,-6),
    "Vindoline": (2,-7),

    "Anhydrovinblastine": (0,-8.5),
    "Vinblastine": (0,-10),
    "Vincristine": (0,-11.5)
}

plt.figure(figsize=(11,17))

nx.draw_networkx_nodes(
    G,
    pos,
    node_size=140
)

nx.draw_networkx_edges(
    G,
    pos,
    arrows=True,
    arrowsize=11,
    width=1.3,
    node_size=140
)

label_pos = {}

for node, (x, y) in pos.items():

    if x < 0:
        label_pos[node] = (x - 0.12, y)

    elif x > 0:
        label_pos[node] = (x + 0.12, y)

    else:
        label_pos[node] = (x + 0.12, y)

nx.draw_networkx_labels(
    G,
    label_pos,
    font_size=7,
    horizontalalignment="left"
)

edge_labels = {
    (source, target): data["enzyme"]
    for source, target, data in G.edges(data=True)
}

nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=edge_labels,
    font_size=6,
    label_pos=0.5,
    rotate=False,
    bbox=dict(
        alpha=0
    )
)

plt.xlim(-4,4)
plt.ylim(-12.5,17)
plt.axis("off")
plt.tight_layout()

plt.savefig(
    "component5_skeleton.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()