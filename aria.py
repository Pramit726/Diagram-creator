# ─── ICONS NEEDED ────────────────────────────────────────────────────────────
# Download these PNGs into the icons/ folder before running:
#   /home/pramit/Diagram-creator/icons/telemetry.png   → Network Telemetry
#   /home/pramit/Diagram-creator/icons/features.png    → Feature Engineering
#   /home/pramit/Diagram-creator/icons/encoder.png     → CMAFE Encoder
#   /home/pramit/Diagram-creator/icons/classifier.png  → Hybrid Classifier
#   /home/pramit/Diagram-creator/icons/actuator.png    → QoS Actuator
#   /home/pramit/Diagram-creator/icons/output.png      → QoS Output
#   /home/pramit/Diagram-creator/icons/opensense.png   → OpenSense
#   /home/pramit/Diagram-creator/icons/validation.png  → Validation Gate
#   /home/pramit/Diagram-creator/icons/promote.png     → Promote & Evolve
#   /home/pramit/Diagram-creator/icons/kpiloop.png     → KPI / Reward Loop
# ─────────────────────────────────────────────────────────────────────────────

from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL

# Graph and cluster attributes
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
    "ARIA Architecture: Zero-SLA Learning with Autonomous Evolution",
    filename="diagrams/my_diagram",
    outformat=["png", "dot"],
    show=False,
    direction="LR",
    graph_attr=graph_attr,
):
    # System 1 — FAST PATH
    with Cluster("System 1 FAST PATH", graph_attr=cluster_attr(CLUSTER_COLOURS[0])):
        input_node = Custom("Network Telemetry", "/home/pramit/Diagram-creator/icons/telemetry.png")
        features = Custom("Feature Engineering", "/home/pramit/Diagram-creator/icons/features.png")
        cmafe = Custom("CMAFE Encoder", "/home/pramit/Diagram-creator/icons/encoder.png")
        classifier = Custom("Hybrid Classifier", "/home/pramit/Diagram-creator/icons/classifier.png")
        actuator = Custom("QoS Actuator", "/home/pramit/Diagram-creator/icons/actuator.png")
        output = Custom("QoS Output", "/home/pramit/Diagram-creator/icons/output.png")
        network = Server("Network Environment")
        policy_store = PostgreSQL("Policy Store")

    # System 2 — SLOW PATH
    with Cluster("System 2 SLOW PATH", graph_attr=cluster_attr(CLUSTER_COLOURS[1])):
        opensense = Custom("OpenSense", "/home/pramit/Diagram-creator/icons/opensense.png")
        validation = Custom("Validation Gate", "/home/pramit/Diagram-creator/icons/validation.png")
        promote = Custom("Promote & Evolve", "/home/pramit/Diagram-creator/icons/promote.png")

    # Feedback Loop
    kpiloop = Custom("KPI / Reward Loop", "/home/pramit/Diagram-creator/icons/kpiloop.png")

    # --- Fast Path Flow ---
    input_node >> Edge(label="", color="#2196F3", fontsize="11") >> features
    features >> Edge(label="", color="#2196F3", fontsize="11") >> cmafe
    cmafe >> Edge(label="", color="#2196F3", fontsize="11") >> classifier
    classifier >> Edge(label="High confidence", color="#2196F3", fontsize="11") >> actuator
    actuator >> Edge(label="", color="#2196F3", fontsize="11") >> output
    output >> Edge(label="", color="#2196F3", fontsize="11") >> network
    policy_store >> Edge(label="QoS policies", color="#2196F3", fontsize="11") >> actuator

    # --- Trigger from System 1 ---
    classifier >> Edge(label="Low confidence / OOD", color="#607D8B", style="dashed", fontsize="11") >> opensense

    # --- Learning Flow ---
    opensense >> Edge(label="", color="#2196F3", fontsize="11") >> validation
    validation >> Edge(label="YES (stable + better KPI)", color="#9C27B0", style="bold", fontsize="11") >> promote
    validation >> Edge(label="NO (continue learning)", color="#607D8B", style="dashed", fontsize="11") >> opensense

    # --- Policy Update ---
    promote >> Edge(label="Update QoS rules", color="#2196F3", fontsize="11") >> policy_store

    # --- Feedback Loop ---
    network >> Edge(label="latency / throughput / loss", color="#607D8B", style="dashed", fontsize="11") >> kpiloop
    kpiloop >> Edge(label="reward signal", color="#607D8B", style="dashed", fontsize="11") >> policy_store

import subprocess
try:
    subprocess.run([
        "graphviz2drawio", "diagrams/my_diagram.dot", "-o", "diagrams/my_diagram.drawio"
    ], check=True)
    print("✓ draw.io → diagrams/my_diagram.drawio")
except FileNotFoundError:
    print("✗ graphviz2drawio not found — pip install graphviz2drawio")
