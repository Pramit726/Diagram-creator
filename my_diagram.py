from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom

# Graph attributes
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

CLUSTER_COLOURS = [
    "#E3F2FD",
    "#F3E5F5",
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

    # ---------------- SYSTEM 1 ----------------
    with Cluster(
        "System 1: Fast Path (<45 ms)", graph_attr=cluster_attr(CLUSTER_COLOURS[0])
    ):

        sense = Custom("Sense", "/home/pramit/Diagram-creator/icons/sense.png")
        embed = Custom("Embed", "/home/pramit/Diagram-creator/icons/embed.png")
        classify = Custom("Classify", "/home/pramit/Diagram-creator/icons/classify.png")
        act = Custom("Act (QoS)", "/home/pramit/Diagram-creator/icons/act.png")

        # 🔥 FIX 5: Add "No SLA drop" messaging
        provisional = Custom(
            "Provisional QoS\n(Safe fallback — No SLA drop)",
            "/home/pramit/Diagram-creator/icons/provisional.png",
        )

        # Main flow
        sense >> Edge(color="#2196F3") >> embed >> Edge(color="#2196F3") >> classify

        classify >> Edge(label="Known", color="#2196F3") >> act

        (
            classify
            >> Edge(
                label="Unknown",
                color="#607D8B",
                style="dashed",
            )
            >> provisional
        )

    # ---------------- SHADOWGUARD ----------------
    # 🔥 FIX 3: Make role explicit
    shadowguard = Custom(
        "ShadowGuard\n(Tests before deployment\n2% traffic • promote only if better)",
        "/home/pramit/Diagram-creator/icons/shadowguard.png",
    )

    # ---------------- SYSTEM 2 ----------------
    with Cluster(
        "System 2: Slow Path (Learning Loop)",
        graph_attr=cluster_attr(CLUSTER_COLOURS[1]),
    ):

        detect = Custom("Detect Drift", "/home/pramit/Diagram-creator/icons/detect.png")
        improve = Custom(
            "Improve Model", "/home/pramit/Diagram-creator/icons/train.png"
        )
        test = Custom("Test Policy", "/home/pramit/Diagram-creator/icons/test.png")
        promote = Custom("Promote", "/home/pramit/Diagram-creator/icons/promote.png")

        # Forward learning flow
        (
            detect
            >> Edge(color="#9C27B0")
            >> improve
            >> Edge(color="#9C27B0")
            >> test
            >> Edge(color="#9C27B0")
            >> promote
        )

        # 🔥 FIX 4: Add cyclic loop
        (
            promote
            >> Edge(
                label="Continuous monitoring",
                color="#9C27B0",
                style="dashed",
            )
            >> detect
        )

    # ---------------- CROSS LOOP ----------------

    # 🔥 FIX 1: Strong UNKNOWN trigger
    (
        provisional
        >> Edge(
            label="Trigger learning loop",
            color="#FF9800",
            penwidth="2",
        )
        >> detect
    )

    # 🔥 FIX 2: KPI → Reward signal (VERY IMPORTANT)
    (
        act
        >> Edge(
            label="Real-world reward\n(RTT, latency, QoS KPIs)",
            color="#4CAF50",
            penwidth="2",
        )
        >> shadowguard
    )

    # Safety gate
    promote >> Edge(color="#2196F3") >> shadowguard

    (
        shadowguard
        >> Edge(
            label="Update model & policy",
            style="dashed",
            color="#607D8B",
        )
        >> classify
    )

    # Feedback into learning
    (
        shadowguard
        >> Edge(
            style="dashed",
            color="#607D8B",
        )
        >> detect
    )


# Optional: draw.io export
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
