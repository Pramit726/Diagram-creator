# Eraser.io → Hackathon Architecture Diagram (Copilot Agent)

Converts your eraser.io diagram code into a visually rich architecture diagram with icons, colours, and draw.io export — powered by **GitHub Copilot** reading `agent.md`.

---

## How It Works

```
You paste eraser.io code → Copilot reads agent.md → Copilot writes diagram.py → You run it → PNG + draw.io
```

Copilot acts as the intelligence layer — it reads your eraser file, understands the architecture, maps every component to the right icon, and generates the Python script.

---

## Setup (one-time)

### 1. Install GraphViz
Download from https://graphviz.org/download/ — tick **"Add to PATH"** during install.

Verify:
```powershell
dot -V
```

### 2. Python environment
```powershell
cd "E:\Learnings\Extras\3_sem\Hackathon\Diagram-creator"
python -m venv venv
.\venv\Scripts\Activate.ps1
$env:PATH += ";C:\Program Files\Graphviz\bin"

# pygraphviz (Windows needs compiler flags)
pip install --config-settings="--global-option=build_ext" `
    --config-settings="--global-option=-IC:\Program Files\Graphviz\include" `
    --config-settings="--global-option=-LC:\Program Files\Graphviz\lib" `
    pygraphviz

pip install -r requirements.txt
```

### 3. VS Code extension
Install `hediet.vscode-drawio` to preview `.drawio` files inside VS Code.

---

## Usage

### Step 1 — Paste your eraser.io code
Open `sample_inputs/my_diagram.eraser` and replace its contents with your eraser.io diagram code.

### Step 2 — Ask Copilot
Open `agent.md` in VS Code so Copilot has context, then in Copilot Chat:

> "Read sample_inputs/my_diagram.eraser and generate a hackathon-ready architecture diagram Python script following agent.md instructions."

Copilot will create a `.py` file (e.g. `my_diagram.py`).

### Step 3 — Run the generated script
```powershell
.\venv\Scripts\Activate.ps1
$env:PATH += ";C:\Program Files\Graphviz\bin"
python my_diagram.py
```

### Step 4 — View outputs
All files land in `diagrams/`:
| File | How to open |
|---|---|
| `*.png` | Any image viewer |
| `*.drawio` | draw.io desktop or https://app.diagrams.net |
| `*.dot` | Version control / Graphviz Playground |

---

## File Structure

```
Diagram-creator/
├── agent.md                     ← Copilot reads this (do not delete)
├── requirements.txt
├── README.md
├── sample_inputs/
│   └── my_diagram.eraser        ← paste your eraser.io code here
├── diagrams/                    ← generated outputs land here
│   ├── *.png
│   ├── *.dot
│   └── *.drawio
└── my_diagram.py                ← Copilot generates this
```

---

## For Each New Diagram

Just replace the contents of `my_diagram.eraser` with your new eraser.io code and ask Copilot again. Give the output a new name so previous diagrams aren't overwritten.
