# 700.390 Advanced Topics in Neurocomputing — Assignments

**Student:** Lanre Olusegun AKINOLA | **ID:** 12349031

Course assignments covering LLM code generation, intent classification, retrieval-augmented generation (RAG), and agentic AI with tool use.

---

## Repository Structure

```
├── assignment_1/          # LLM Code Generation (Fibonacci with Qwen2.5-Coder)
│   ├── fibonacci_colab.ipynb
│   ├── results/
│   └── report/
├── assignment_2/          # Email Intent Extraction (Qwen2.5-1.5B)
│   ├── email_intent_colab.ipynb
│   ├── results/
│   └── report/
├── assignment_3/          # RAG Chat System (FAISS + Qwen)
│   ├── rag_chat_colab.ipynb
│   ├── results/
│   └── report/
├── assignment_4/          # Agentic AI with Tool Use (ReAct pattern)
│   ├── agent.py           # Main runnable script
│   ├── agentic_ai.ipynb   # Notebook version
│   ├── README.md          # How to run Assignment 4
│   ├── results/
│   └── report/
├── labs/                  # Lab exercises
├── requirements.txt
└── .gitignore
```

---

## Assignment Summaries

### Assignment 1 — LLM Code Generation
Evaluated `Qwen2.5-Coder-0.5B` on generating iterative and recursive Fibonacci implementations. Tested across different temperature and generation settings to measure correctness and consistency.

📄 [View Report](assignment_1/report/report.md) | [Download PDF](assignment_1/report/Report_Assignment1.pdf)

### Assignment 2 — Email Intent Extraction
Used `Qwen2.5-1.5B` to classify intent from raw email text (e.g., complaint, inquiry, request). Compared zero-shot vs. few-shot prompting strategies.

📄 [View Report](assignment_2/report/report.md) | [Download PDF](assignment_2/report/Report_Assignment2.pdf)

### Assignment 3 — Retrieval-Augmented Generation (RAG)
Built a RAG chat system using FAISS for vector retrieval and a local Qwen model for generation. Evaluated retrieval accuracy and answer quality on course-related documents.

📄 [View Report](assignment_3/report/report.md) | [Download PDF](assignment_3/report/Report_Assignment3.pdf)

### Assignment 4 — Agentic AI with Tool Use
Implemented a ReAct-style agent in pure Python with three tools:
- **`search_web`** — DuckDuckGo search via `ddgs`
- **`convert_currency`** — Live exchange rates via Frankfurter API
- **`calculate`** — Safe math expression evaluator

The agent routes questions to the appropriate tool using keyword-based selection and logs a full QUESTION → TOOL → OBSERVE → ANSWER → TIME trace for each query.

📄 [View Report](assignment_4/report/report.md) | [Download PDF](assignment_4/report/Report_Assignment4.pdf)

```bash
# Run the agent
cd assignment_4
python agent.py
```

---

## Setup

**Requirements:** Python 3.8+, no GPU needed for Assignment 4.

```bash
git clone https://github.com/<your-username>/agentic-ai-assignments.git
cd agentic-ai-assignments
pip install -r requirements.txt
```

Assignments 1–3 were run on Google Colab (GPU recommended for LLM inference).  
Assignment 4 runs fully locally with no GPU required.

## Dependencies

Key libraries used in this project:
- `transformers` - Hugging Face transformers library
- `torch` - PyTorch for model inference
- `numpy` - Numerical computations
- `pandas` - Data manipulation and analysis
- `matplotlib` - Visualization
- `seaborn` - Statistical visualizations

## Author

Akino

## License

This project is for educational purposes.
