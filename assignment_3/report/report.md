# Assignment 3: RAG Chat System
## Build a Simple Retrieval-Augmented Generation Pipeline

**Student ID:** 12349031  
**Course:** 700.390 Advanced Topics in Neurocomputing: Explainability, Neuro-Symbolic Computing, AI Agents, LLM, Quantum Computing, PINN

---

## 1. Overview

This assignment builds a simple Retrieval-Augmented Generation (RAG) chat system. The system reads uploaded PDF files, splits the text into overlapping chunks, indexes them using FAISS, and answers questions by retrieving relevant chunks and passing them to a language model. The model is instructed to answer only from the retrieved content. If the answer is not found in the documents, the system returns "Insufficient evidence."

---

## 2. System Pipeline

The pipeline has six steps:

1. **Upload:** The user uploads PDF files via Google Colab. Three documents were used: `course_policy.pdf`, `lab_guide.pdf`, and `faq.pdf`.
2. **Parse:** Text is extracted from each PDF using the `pypdf` library. The original file name is kept as metadata for each document.
3. **Chunk:** Each document is split into overlapping chunks of 500 characters with an overlap of 100 characters. Each chunk stores the source file name.
4. **Embed and Index:** Chunks are embedded using `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions) and indexed with a FAISS flat L2 index.
5. **Retrieve:** For each query, the top-3 most similar chunks are retrieved by embedding the query and searching the FAISS index.
6. **Answer:** The retrieved chunks and the question are passed to `Qwen/Qwen3.5-0.8B`. The model is instructed to answer only from the context. Sources are cited by file name.

---

## 3. Results

The system was evaluated on 10 test questions: 8 with answers present in the documents, and 2 with no answer available (abstention cases).

| # | Question (short) | Answer (short) | Source | Grounded | Time |
|---|------------------|----------------|--------|----------|------|
| 1 | Late submission penalty? | 10% penalty | course_policy.pdf | Yes | 0.79s |
| 2 | How is final grade calculated? | 60% assignments, 40% exam | course_policy.pdf | Yes | 7.22s |
| 3 | When are office hours? | Mon 2–4pm, Wed 10am–12pm | course_policy.pdf | Yes | 1.74s |
| 4 | How many assignments? | 4 assignments | course_policy.pdf | Yes | 1.29s |
| 5 | Packages to install? | transformers, torch, faiss... | lab_guide.pdf | Yes | 1.86s |
| 6 | Recommended GPU? | A100 or T4 on Colab | lab_guide.pdf | Yes | 1.02s |
| 7 | Submit in groups? | No, individually | faq.pdf | Yes | 1.93s |
| 8 | Use pre-trained models? | Yes, cite them | faq.pdf | Yes | 1.97s |
| 9 | Capital of Germany? | "Berlin" (should abstain) | — | — | 0.65s |
| 10 | How does BERT work? | Insufficient evidence. | — | N/A | 0.80s |

### Evaluation Metrics Summary

| Metric | Result | Notes |
|--------|--------|-------|
| Retrieval quality | 8/8 | Correct source retrieved for all answerable questions |
| Grounding / faithfulness | 8/8 | All answers supported by retrieved chunks |
| Source correctness | 8/8 | File names cited correctly |
| Latency | 1.93s average | Range: 0.65s – 7.22s |
| Abstention | 1/2 | Q10 returned "Insufficient evidence.", Q9 did not |

---

## 4. Discussion

The system performed well on all eight answerable questions. Answers were accurate, grounded in the retrieved chunks, and sources were cited correctly by file name.

**Q9 failure (Capital of Germany):** The model answered "Berlin" even though the answer was not in any of the uploaded documents. This is a known limitation of small instruction-tuned models — they use their training-time knowledge when the context does not contain an obvious answer. A stronger grounding mechanism, such as stricter prompt constraints or output filtering, would be needed to prevent this.

**Q10 success (BERT self-attention):** Handled correctly. The model returned "Insufficient evidence." because the documents contain no information about BERT.

---

## 5. Conclusion

The RAG pipeline was implemented end-to-end and ran successfully on Google Colab. The system correctly parses uploaded PDFs, retrieves relevant chunks, cites sources by file name, and answers only from the retrieved content in most cases.

The main limitation is that small models can still leak training-time knowledge when they confidently know an answer, even if it is not supported by the context.

---

## References

1. Qwen Team. *Qwen3.5 Technical Report*. Hugging Face, 2025.
2. N. Reimers and I. Gurevych. *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*. EMNLP 2019.
3. J. Johnson, M. Douze, and H. Jegou. *Billion-scale similarity search with GPUs*. IEEE Transactions on Big Data, 7(3):535–547, 2021.
