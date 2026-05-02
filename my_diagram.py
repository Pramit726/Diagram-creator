from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.onprem.mlops import Mlflow

# Graph attributes for hackathon-quality output
graph_attr = {
    "splines": "ortho",
    "pad": "0.5",
    "nodesep": "0.7",
    "ranksep": "0.8",
    "fontsize": "16",
    "fontname": "Arial",
    "bgcolor": "#FAFAFA",
    "compound": "true",
}

# Cluster colour palette
CLUSTER_COLOURS = [
    "#E3F2FD",  # ice blue
    "#F3E5F5",  # lavender
    "#E8F5E9",  # mint
    "#FFFDE7",  # yellow
]


def cluster_attr(colour: str) -> dict:
    return {
        "style": "filled",
        "color": colour,
        "labeljust": "c",
        "fontsize": "15",
        "fontname": "Arial",
    }


with Diagram(
    "Dual Loop Intelligence Evolution",
    filename="diagrams/my_diagram",
    show=False,
    outformat=["png", "dot"],
    graph_attr=graph_attr,
):
    # SYSTEM 1: PRODUCTION (TOP TRACK)
    with Cluster("System 1: Fast Path", graph_attr=cluster_attr(CLUSTER_COLOURS[0])):
        sense = Custom(
            "Sense",
            "/home/pramit/Diagram-creator/icons/sense.png",
        )
        embed = Custom(
            "Embed",
            "/home/pramit/Diagram-creator/icons/embed.png",
        )
        classify = Custom(
            "Classify",
            "/home/pramit/Diagram-creator/icons/classify.png",
        )
        act = Custom(
            "Act (QoS)",
            "/home/pramit/Diagram-creator/icons/act.png",
        )
        provisional = Custom(
            "Provisional QoS",
            "/home/pramit/Diagram-creator/icons/provisional.png",
        )

        # Main path
        (
            sense
            >> Edge(color="#2196F3", fontsize="11")
            >> embed
            >> Edge(color="#2196F3", fontsize="11")
            >> classify
        )
        classify >> Edge(label="Known", color="#2196F3", fontsize="11") >> act
        (
            classify
            >> Edge(label="Unknown", color="#607D8B", style="dashed", fontsize="11")
            >> provisional
        )

    # INTERFACE: THE GATEKEEPER
    shadowguard = Custom(
        "ShadowGuard Validation",
        "/home/pramit/Diagram-creator/icons/shadowguard.png",
    )

    # SYSTEM 2: LEARNING (BOTTOM TRACK)
    with Cluster("System 2: Slow Path", graph_attr=cluster_attr(CLUSTER_COLOURS[1])):
        detect = Custom(
            "Detect Drift",
            "/home/pramit/Diagram-creator/icons/detect.png",
        )
        improve = Custom(
            "Improve Model",
            "/home/pramit/Diagram-creator/icons/train.png",
        )
        test = Custom(
            "Test Policy",
            "/home/pramit/Diagram-creator/icons/test.png",
        )
        promote = Custom(
            "Promote",
            "/home/pramit/Diagram-creator/icons/promote.png",
        )

        # Learning path
        (
            detect
            >> Edge(color="#2196F3", fontsize="11")
            >> improve
            >> Edge(color="#2196F3", fontsize="11")
            >> test
            >> Edge(color="#2196F3", fontsize="11")
            >> promote
        )

    # CROSS-LOOP LOGIC
    # Trigger learning from unknowns
    provisional >> Edge(label="Trigger", color="#2196F3", fontsize="11") >> detect

    # Safety Promotion Loop
    promote >> Edge(color="#2196F3", fontsize="11") >> shadowguard
    (
        shadowguard
        >> Edge(label="Update", color="#607D8B", style="dashed", fontsize="11")
        >> classify
    )

    # Feedback from Act to improve
    act >> Edge(label="KPIs", color="#2196F3", fontsize="11") >> shadowguard
    shadowguard >> Edge(color="#607D8B", style="dashed", fontsize="11") >> detect

# draw.io export
import subprocess

try:
    subprocess.run(
        [
            "python",
            "-m",
            "graphviz2drawio",
            "diagrams/my_diagram.dot",
            "-o",
            "diagrams/my_diagram.drawio",
        ],
        check=True,
    )
    print("✓ draw.io → diagrams/my_diagram.drawio")
except FileNotFoundError:
    print("✗ graphviz2drawio not found — pip install graphviz2drawio")
