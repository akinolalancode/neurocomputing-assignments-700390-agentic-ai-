# Assignment 4: Agentic AI Application

**Student:** AKINOLA, Lanre Olusegun  
**Student ID:** 12349031  
**Course:** 700.390 Advanced Topics in Neurocomputing

## What this does

A simple agentic AI system that reads a user question, decides which tool to use, calls it, and returns a final answer. No hard-coded answers.

## Tools

| Tool | What it does | API |
|---|---|---|
| `search_web()` | Internet search | DuckDuckGo (ddgs) |
| `convert_currency()` | Single currency conversion | Frankfurter API |
| `get_multiple_rates()` | Compare several currencies | Frankfurter API |
| `calculate()` | Simple arithmetic | Python math module |

## How to run

**Requirements:** Python 3.8+

**Install packages:**
```
pip install ddgs requests
```

**Run the agent:**
```
python agent.py
```

This runs all 7 example questions and saves results to `results/agent_results.json`.

**Run the notebook:**
Open `agentic_ai.ipynb` in Jupyter or VS Code and run all cells.

```
pip install jupyter
jupyter notebook agentic_ai.ipynb
```

## Agent trace format

For every question the agent prints:

```
QUESTION : <the user's question>
TOOL     : <selected tool>
OBSERVE  : <what the tool returned>
ANSWER   : <final answer>
TIME     : <seconds>
```

## Files

```
assignment_4/
├── agent.py              main agent script (all tools + logic)
├── agentic_ai.ipynb      same code as a Jupyter notebook
├── README.md             this file
├── results/
│   └── agent_results.json   outputs from running all 7 questions
└── report/
    └── report.tex        LaTeX source for the scientific report
```
