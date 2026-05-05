# ─── ICONS NEEDED ────────────────────────────────────────────────────────────
# Download these PNGs into the icons/ folder before running:
#   /home/pramit/Diagram-creator/icons/temporal.png      → Temporal (Rhythm)
#   /home/pramit/Diagram-creator/icons/statistical.png   → Statistical (Volume)
#   /home/pramit/Diagram-creator/icons/context.png       → Context (Environment)
#   /home/pramit/Diagram-creator/icons/cnn_gru.png       → CNN + GRU
#   /home/pramit/Diagram-creator/icons/mlp_stats.png     → MLP (Stats)
#   /home/pramit/Diagram-creator/icons/mlp_context.png   → MLP (Context)
#   /home/pramit/Diagram-creator/icons/adaptive.png      → Adaptive Fusion
#   /home/pramit/Diagram-creator/icons/inputflow.png     → Encrypted Traffic Flow
#   /home/pramit/Diagram-creator/icons/embedding.png     → 128-dim Embedding (z)
# ─────────────────────────────────────────────────────────────────────────────

from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.programming.flowchart import Database

def cluster_attr(colour: str) -> dict:
    return {
        "fontsize": "13",
        "fontname": "Helvetica Neue Bold",
        "bgcolor": colour,
        "style": "rounded",
        "margin": "20",
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

with Diagram(
    "CMAFE Encoder: Multi-Aspect Fusion for Intent Representation",
    filename="diagrams/aria_diagram",
    outformat=["png", "dot"],
    show=False,
    direction="TB",
    graph_attr=graph_attr,
):
    # Input
    input_flow = Custom("Encrypted Traffic Flow", "/home/pramit/Diagram-creator/icons/inputflow.png")

    # Parallel Streams
    with Cluster("Temporal (Rhythm)", graph_attr=cluster_attr("#E3F2FD")):
        temporal_features = Custom("Timing patterns", "/home/pramit/Diagram-creator/icons/temporal.png")
        cnn_gru = Custom("CNN + GRU", "/home/pramit/Diagram-creator/icons/cnn_gru.png")
    with Cluster("Statistical (Volume)", graph_attr=cluster_attr("#F3E5F5")):
        statistical_features = Custom("Size / distribution", "/home/pramit/Diagram-creator/icons/statistical.png")
        mlp_stats = Custom("MLP", "/home/pramit/Diagram-creator/icons/mlp_stats.png")
    with Cluster("Context (Environment)", graph_attr=cluster_attr("#FFF3E0")):
        context_features = Custom("Network state", "/home/pramit/Diagram-creator/icons/context.png")
        mlp_context = Custom("MLP", "/home/pramit/Diagram-creator/icons/mlp_context.png")

    # Adaptive Fusion
    adaptive_fusion = Custom("Adaptive Fusion", "/home/pramit/Diagram-creator/icons/adaptive.png")

    # Output
    embedding = Custom("128-dim Embedding (z)", "/home/pramit/Diagram-creator/icons/embedding.png")

    # Flow into streams
    input_flow >> Edge(label="", color="#2196F3", fontsize="11") >> temporal_features
    input_flow >> Edge(label="", color="#2196F3", fontsize="11") >> statistical_features
    input_flow >> Edge(label="", color="#2196F3", fontsize="11") >> context_features

    temporal_features >> Edge(label="", color="#2196F3", fontsize="11") >> cnn_gru
    statistical_features >> Edge(label="", color="#2196F3", fontsize="11") >> mlp_stats
    context_features >> Edge(label="", color="#2196F3", fontsize="11") >> mlp_context

    # Streams to fusion
    cnn_gru >> Edge(label="", color="#2196F3", fontsize="11") >> adaptive_fusion
    mlp_stats >> Edge(label="", color="#2196F3", fontsize="11") >> adaptive_fusion
    mlp_context >> Edge(label="", color="#2196F3", fontsize="11") >> adaptive_fusion

    # Fusion to output
    adaptive_fusion >> Edge(label="", color="#2196F3", fontsize="11") >> embedding

import subprocess
try:
    subprocess.run([
        "dot", "-Tsvg", "diagrams/aria_diagram.dot", "-o", "diagrams/aria_diagram.drawio"
    ], check=True)
    print("✓ draw.io → diagrams/aria_diagram.drawio")
except FileNotFoundError:
    print("✗ dot not found — please install Graphviz")
