# ─── ICONS NEEDED ────────────────────────────────────────────────────────────
# Download these PNGs into the icons/ folder before running:
#   icons/database.png   → https://www.flaticon.com (search: database)
#   icons/cpu.png        → https://www.flaticon.com (search: cpu)
#   icons/sliders.png    → https://www.flaticon.com (search: sliders)
#   icons/activity.png   → https://www.flaticon.com (search: activity)
#   icons/search.png     → https://www.flaticon.com (search: search)
#   icons/plus-circle.png → https://www.flaticon.com (search: plus circle)
#   icons/check-circle.png → https://www.flaticon.com (search: check circle)
#   icons/alert-circle.png → https://www.flaticon.com (search: alert circle)
# ─────────────────────────────────────────────────────────────────────────────

from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom

# Graph attributes for hackathon-quality output
graph_attr = {
    "splines": "ortho",
    "nodesep": "1.0",
    "ranksep": "1.4",
    "fontsize": "16",
    "fontname": "Helvetica Neue",
    "bgcolor": "white",
    "pad": "0.8",
    "compound": "true",
}

CLUSTER_COLOURS = [
    "#E3F2FD",  # ice blue
    "#F3E5F5",  # soft purple
    "#FFF3E0",  # warm orange
    "#E8F5E9",  # mint green
    "#FCE4EC",  # rose
    "#E8F4F8",  # azure
    "#F9FBE7",  # lime
    "#FFFDE7",  # yellow
]

def cluster_attr(colour: str) -> dict:
    return {
        "fontsize": "13",
        "fontname": "Helvetica Neue Bold",
        "bgcolor": colour,
        "style": "rounded",
        "margin": "20",
    }

with Diagram(
    "Hybrid Classifier + OpenSense",
    filename="diagrams/aria_diagram",
    outformat=["png", "dot"],
    show=False,
    direction="TB",
    graph_attr=graph_attr,
):
    embedding = Custom("Traffic Embedding (z)", "home/pramit/Diagram-creator/icons/database.png")
    with Cluster("Hybrid Classifier", graph_attr=cluster_attr(CLUSTER_COLOURS[0])):
        similarity = Custom("Similarity (Memory Bank)", "home/pramit/Diagram-creator/icons/cpu.png")
        ml = Custom("ML Confidence", "home/pramit/Diagram-creator/icons/cpu.png")
        ood = Custom("OOD Detection", "home/pramit/Diagram-creator/icons/cpu.png")
    embedding >> similarity
    embedding >> ml
    embedding >> ood
    known = Custom("Known Traffic", "home/pramit/Diagram-creator/icons/check-circle.png")
    unknown = Custom("Unknown Traffic", "home/pramit/Diagram-creator/icons/alert-circle.png")
    similarity >> Edge(label="high similarity", color="#2196F3", fontsize="11") >> known
    ml >> Edge(label="high confidence", color="#2196F3", fontsize="11") >> known
    ood >> Edge(label="low confidence / OOD", color="#2196F3", fontsize="11") >> unknown
    qos = Custom("Apply QoS", "home/pramit/Diagram-creator/icons/sliders.png")
    known >> qos
    provisional_qos = Custom("Provisional QoS", "home/pramit/Diagram-creator/icons/activity.png")
    with Cluster("OpenSense", graph_attr=cluster_attr(CLUSTER_COLOURS[1])):
        cluster = Custom("Cluster unknowns (HDBSCAN)", "home/pramit/Diagram-creator/icons/search.png")
        validate = Custom("Stable cluster?", "home/pramit/Diagram-creator/icons/search.png")
    unknown >> cluster
    cluster >> validate
    new_class = Custom("New Class + Policy", "home/pramit/Diagram-creator/icons/plus-circle.png")
    validate >> Edge(label="YES", color="#2196F3", fontsize="11") >> new_class
    validate >> Edge(label="NO", color="#607D8B", style="dashed", fontsize="11") >> cluster
    new_class >> qos

import subprocess
try:
    subprocess.run(
        ["dot", "-Tsvg", "diagrams/aria_diagram.dot", "-o", "diagrams/aria_diagram.drawio"],
        check=True,
    )
    print("✓ draw.io → diagrams/aria_diagram.drawio")
except FileNotFoundError:
    print("✗ dot not found — ensure Graphviz is installed and in PATH")
