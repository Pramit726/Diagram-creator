# Agent Instructions: Eraser.io → Hackathon Architecture Diagram

## Overview
This workspace converts **eraser.io diagram code** into visually rich, hackathon-ready architecture diagrams.

The user will paste their eraser.io diagram code into `sample_inputs/my_diagram.eraser`.  
Your job as the agent is to:
1. **Read** `sample_inputs/my_diagram.eraser`
2. **Generate** a Python script (e.g. `my_diagram.py`) using the `diagrams` library that visually represents the architecture with icons, colours, and clusters
3. **Tell the user** to run it

The eraser.io format is plain-text and line-based — no icons, no colours, no visual styling. You must make it visually appealing by mapping components to the correct icons and adding cluster colours.

---

## Environment Setup

### Python Environment
- **Location**: `E:\Learnings\Extras\3_sem\Hackathon\Diagram-creator\venv`
- **Python Version**: 3.x
- **Activation**: `.\venv\Scripts\Activate.ps1` (PowerShell)

### Installed Packages
```
diagrams==0.24.4
graphviz==0.20.3
pygraphviz==1.14
graphviz2drawio==1.1.0
puremagic==1.30
svg.path==7.0
```

### GraphViz Installation
- **Location**: `C:\Program Files\Graphviz\bin`
- **Critical**: Must add to PATH before running any diagram script
  ```powershell
  $env:PATH += ";C:\Program Files\Graphviz\bin"
  ```

### VS Code Extensions
- **Draw.io**: `hediet.vscode-drawio` — for viewing/editing `.drawio` files

---

## File Structure

```
Diagram-creator/
├── venv/                        # Python virtual environment
├── requirements.txt             # Python dependencies
├── agent.md                     # THIS FILE — Copilot instructions
├── sample_inputs/
│   └── my_diagram.eraser        # ← User pastes their eraser.io code here
├── diagrams/                    # Output directory (auto-created)
│   ├── *.png
│   ├── *.dot
│   └── *.drawio
└── *.py                         # Generated diagram scripts (one per diagram)
```

---

## Your Workflow as the Agent

### Step 1 — Read the eraser.io file

Open `sample_inputs/my_diagram.eraser` and parse:
- **Title** (if present): `title: My Architecture`
- **Groups / clusters**: blocks wrapped in `{ }` — these become `Cluster()` in diagrams
- **Nodes**: component names listed inside groups or standalone
- **Edges**: lines like `A -> B: label`, `A -- B`, `A <-> B`

Eraser DSL reference:
```
// comment
title: My System

GroupName {
    NodeA
    NodeB [label: "Custom Label"]
    
    NestedGroup {
        NodeC
    }
}

NodeA -> NodeB: HTTP
NodeA -- NodeB        // undirected → use dashed edge style
NodeA <-> NodeB: sync // bidirectional → draw both directions
```

---

### Step 2 — Generate the Python script

Create a `.py` file named after the diagram (e.g. `my_diagram.py`) using the template below.

#### Graph Attributes (always use these for hackathon-quality output)
```python
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
```

#### Cluster Colour Palette (assign one per top-level group)
```python
# Use these in rotation for top-level clusters
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
```

#### Edge Styling
```python
from diagrams import Edge

# Directed  →  solid blue
Edge(label="HTTP", color="#2196F3", fontsize="11")

# Undirected  —  dashed grey
Edge(label="", color="#607D8B", style="dashed", fontsize="11")

# Bidirectional  ↔  bold purple (draw both directions)
Edge(label="sync", color="#9C27B0", style="bold", fontsize="11")
```

#### Output Format (always generate both)
```python
with Diagram(
    "My Architecture",
    filename="diagrams/my_diagram",
    outformat=["png", "dot"],
    show=False,
    direction="TB",
    graph_attr=graph_attr,
):
```

#### draw.io Export (always append at end of script)
```python
import subprocess

try:
    subprocess.run(
        ["graphviz2drawio", "diagrams/my_diagram.dot", "-o", "diagrams/my_diagram.drawio"],
        check=True,
    )
    print("✓ draw.io → diagrams/my_diagram.drawio")
except FileNotFoundError:
    print("✗ graphviz2drawio not found — pip install graphviz2drawio")
```

---

### Step 3 — Icon Mapping Rules

⚠️ **CRITICAL**: Only use icons from the verified lists below. These are the EXACT class names confirmed working on this installation. Never guess or invent names.

#### Users / Clients
```python
from diagrams.onprem.client import Users, User, Client
# Keywords: user, users, client, browser, customer, mobile, app
```

#### Generic Compute / Servers
```python
from diagrams.onprem.compute import Server, Nomad
# Keywords: server, compute, worker, node
```

#### Flowchart / Generic shapes
```python
from diagrams.programming.flowchart import (
    Action, Collate, Database, Decision, Delay, Display, Document,
    InputOutput, Inspection, InternalStorage, LoopLimit, ManualInput,
    ManualLoop, Merge, MultipleDocuments, Or, PredefinedProcess,
    Preparation, Sort, StartEnd, StoredData, SummingJunction
)
# ✅ Use PredefinedProcess (NOT Process — Process does NOT exist)
# ✅ Use StartEnd (NOT Start or End)
# ✅ Use Decision for conditions/checks
# ✅ Use Database for generic DB nodes
# Keywords: process/step/task → PredefinedProcess
#           start/end/begin/finish → StartEnd
#           decision/if/condition → Decision
#           database/db (generic) → Database
#           document/report/file → Document
#           input/output/form → InputOutput
```

#### AWS Compute
```python
from diagrams.aws.compute import EC2, Lambda, ECS, EKS, Fargate, ElasticBeanstalk, Batch
# Keywords: lambda/function/serverless → Lambda
#           ec2/vm/instance/server → EC2
#           ecs/container service → ECS
#           eks/kubernetes/k8s → EKS
#           fargate → Fargate
```

#### AWS Database
```python
from diagrams.aws.database import RDS, Dynamodb, ElastiCache, Aurora, Redshift, DocumentDB, Neptune
# Keywords: rds/sql/relational → RDS
#           dynamodb/dynamo/nosql → Dynamodb
#           elasticache/redis/cache/memcached → ElastiCache
#           aurora → Aurora
#           redshift/warehouse → Redshift
#           documentdb/mongodb compatible → DocumentDB
```

#### AWS Network
```python
from diagrams.aws.network import (
    ELB, ALB, NLB, APIGateway, CloudFront, Route53, VPC,
    InternetGateway, NATGateway, TransitGateway, GlobalAccelerator
)
# Keywords: elb/load balancer/alb → ELB or ALB
#           api gateway/gateway → APIGateway
#           cloudfront/cdn → CloudFront
#           route53/dns → Route53
#           vpc/virtual network → VPC
#           internet gateway → InternetGateway
```

#### AWS Storage
```python
from diagrams.aws.storage import S3, EBS, EFS, Backup, StorageGateway
# Keywords: s3/bucket/blob/object storage → S3
#           ebs/block storage/volume → EBS
#           efs/file storage → EFS
```

#### AWS Security
```python
from diagrams.aws.security import IAM, Cognito, KMS, SecretsManager, WAF, Shield, SecurityHub
# Keywords: iam/role/permission → IAM
#           cognito/auth/authentication/login/identity → Cognito
#           kms/encryption/key → KMS
#           secrets manager/secret → SecretsManager
#           waf → WAF
```

#### AWS Integration / Messaging
```python
from diagrams.aws.integration import SQS, SNS, Eventbridge, MQ, StepFunctions
# Keywords: sqs/queue → SQS
#           sns/notification/topic → SNS
#           eventbridge/events → Eventbridge
#           step functions/workflow → StepFunctions
```

#### AWS Management / Monitoring
```python
from diagrams.aws.management import Cloudwatch, Cloudtrail, Cloudformation, Config, SSM
# Keywords: cloudwatch/monitoring/metrics/logs → Cloudwatch
#           cloudtrail/audit → Cloudtrail
#           cloudformation/iac → Cloudformation
```

#### Azure
```python
from diagrams.azure.compute import AppServices, FunctionApps, VM
from diagrams.azure.database import SQLDatabases, CosmosDb
from diagrams.azure.network import VirtualNetworks, ApplicationGateway, FrontDoors, LoadBalancers
from diagrams.azure.storage import StorageAccounts, BlobStorage
from diagrams.azure.security import KeyVaults
from diagrams.azure.integration import ServiceBus
from diagrams.azure.identity import ManagedIdentities
# Keywords: app service/webapp → AppServices
#           function app/azure function → FunctionApps
#           azure vm → VM
#           sql db/azure sql → SQLDatabases
#           cosmosdb/cosmos → CosmosDb
#           key vault/secret → KeyVaults
#           service bus → ServiceBus
```

#### Networking / Infrastructure
```python
from diagrams.onprem.network import (
    Nginx, Apache, Haproxy, Internet, Traefik, Istio, Kong,
    Envoy, Consul, Etcd, Zookeeper, Gunicorn
)
# Keywords: nginx/reverse proxy → Nginx
#           apache → Apache
#           haproxy → Haproxy
#           traefik → Traefik
#           internet/www/web → Internet
#           istio/service mesh → Istio
#           kong/api gateway (onprem) → Kong
```

#### Queues / Messaging
```python
from diagrams.onprem.queue import Kafka, RabbitMQ, Celery, ActiveMQ, Nats, ZeroMQ
# ✅ Use RabbitMQ (not Rabbitmq — both exist but RabbitMQ is preferred)
# Keywords: kafka/event hub/streaming → Kafka
#           rabbitmq → RabbitMQ
#           celery/worker → Celery
#           activemq → ActiveMQ
```

#### Databases (on-prem)
```python
from diagrams.onprem.database import (
    PostgreSQL, MySQL, MongoDB, Cassandra, Redis,
    MSSQL, MariaDB, CockroachDB, ClickHouse, Neo4J,
    Oracle, Qdrant, Scylla
)
# ✅ Use PostgreSQL (not Postgresql — both exist, PostgreSQL preferred)
# ✅ Use MySQL (not Mysql)
# ✅ Use MongoDB (not Mongodb)
# Keywords: postgres/postgresql → PostgreSQL
#           mysql → MySQL
#           mongodb/mongo → MongoDB
#           cassandra → Cassandra
#           redis → Redis (from onprem.database)
#           mssql/sql server → MSSQL
#           neo4j/graph db → Neo4J
#           vector db/qdrant → Qdrant
```

#### Containers
```python
from diagrams.onprem.container import Docker
# Keywords: docker, container
```

#### Monitoring
```python
from diagrams.onprem.monitoring import (
    Grafana, Prometheus, Datadog, Sentry, Newrelic,
    Splunk, Dynatrace, Zabbix, Nagios
)
# Keywords: grafana → Grafana
#           prometheus → Prometheus
#           datadog → Datadog
#           sentry → Sentry
```

#### Analytics (on-prem)
```python
from diagrams.onprem.analytics import (
    Spark, Kafka, Hadoop, Hive, Flink, Databricks,
    Tableau, PowerBI, Superset, Metabase, Presto, Trino
)
# ✅ NO Activity, Model, or Test — these do NOT exist
# Keywords: spark → Spark
#           hadoop → Hadoop
#           flink → Flink
#           databricks → Databricks
#           tableau → Tableau
#           powerbi → PowerBI
#           superset/metabase → Superset or Metabase
```

#### Version Control
```python
from diagrams.onprem.vcs import Github, Git, Gitlab, Gitea
# Keywords: git/github/repo/vcs → Github
```

#### MLOps
```python
from diagrams.onprem.mlops import Mlflow, Polyaxon
# ✅ Only Mlflow and Polyaxon exist — nothing else
# Keywords: mlflow/experiment tracking → Mlflow
#           ml training/polyaxon → Polyaxon
# For generic ML model nodes use PredefinedProcess from flowchart
```

**Fallback**: If no keyword matches, use:
```python
from diagrams.programming.flowchart import PredefinedProcess
# ✅ PredefinedProcess is the correct fallback (NOT Process)
```

---

#### Custom Icons (for domain-specific nodes)

When a node concept doesn't match any library icon (e.g. "ShadowGuard", "Classify", "Sense", "QoS"), use the `Custom` class with a PNG file from the `icons/` folder:

```python
from diagrams.custom import Custom

# Syntax: Custom("Label", "./icons/filename.png")
sense      = Custom("Sense", "./icons/sensor.png")
classify   = Custom("Classify", "./icons/ml.png")
shadowguard = Custom("ShadowGuard", "./icons/shield.png")
promote    = Custom("Promote", "./icons/deploy.png")
```

**Icon file rules:**
- All icons go in the `icons/` folder at project root
- Must be PNG format, ideally 64x64 or 128x128 px
- Filename must match exactly what's used in the script

**Icon assignment guide — tell the user to download these:**

| Node concept | Icon to download | Search term on flaticon.com |
|---|---|---|
| Security / Guard / Shield | shield.png | "shield security" |
| ML Model / AI / Neural Net | ml.png | "neural network" |
| Sensor / Sense / Input | sensor.png | "sensor" |
| Classify / Decision / ML classify | classify.png | "classification" |
| QoS / Network quality | qos.png | "network quality" |
| Deploy / Promote / Release | deploy.png | "rocket deploy" |
| Drift / Detect / Monitor | detect.png | "radar detect" |
| Embed / Vector / Encode | embed.png | "vector embedding" |
| Validation / Test / Check | validate.png | "checkmark verify" |
| Policy / Rules / Governance | policy.png | "document rules" |

**When to use Custom vs library icons:**
- Cloud services (AWS/Azure/GCP) → always use library icons
- Generic concepts (server, database, queue) → use library icons
- Domain-specific / custom concepts → use `Custom` with PNG
- Any node that previously fell back to a plain pink box → replace with `Custom`

**Always tell the user which icons to download** at the top of the generated script as a comment:

```python
# ─── ICONS NEEDED ────────────────────────────────────────────────────────────
# Download these PNGs into the icons/ folder before running:
#   icons/shield.png   → https://www.flaticon.com (search: shield security)
#   icons/ml.png       → https://www.flaticon.com (search: neural network)
#   icons/sensor.png   → https://www.flaticon.com (search: sensor)
# ─────────────────────────────────────────────────────────────────────────────
```

---

### Step 4 — Tell the user to run it

After generating the script, instruct the user:

```powershell
# In PowerShell, from the project root:
.\venv\Scripts\Activate.ps1
$env:PATH += ";C:\Program Files\Graphviz\bin"
python my_diagram.py
```

Output files will appear in `diagrams/`:
- `my_diagram.png` — visual image
- `my_diagram.dot` — GraphViz source
- `my_diagram.drawio` — editable in draw.io

---

## Key Principles

1. **Read the eraser file first** — never generate a diagram from memory
2. **Every group becomes a Cluster** — preserve the hierarchy from eraser.io
3. **Every node gets an icon** — no plain text nodes; use Process as last resort
4. **Assign distinct colours** — rotate through CLUSTER_COLOURS for top-level groups
5. **Always export draw.io** — append the subprocess call at the end of every script
6. **Output format is always `["png", "dot"]`** — both are required

---

## Troubleshooting Reference

### GraphViz not found
```powershell
$env:PATH += ";C:\Program Files\Graphviz\bin"
```

### Wrong icon name (ImportError)
Check available names:
```python
from diagrams.aws import compute
print([x for x in dir(compute) if not x.startswith('_')])
```

### Cluttered layout
Increase spacing in `graph_attr`:
```python
"nodesep": "1.5",
"ranksep": "2.0",
```
Or switch direction: `direction="LR"`

### graphviz2drawio not found
```powershell
pip install graphviz2drawio
```
