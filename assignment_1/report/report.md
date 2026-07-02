# Assignment 1: LLM Code Generation Evaluation
## Fibonacci Sequence Generation with a Small Language Model

**Student ID:** 12349031  
**Course:** 700.390 Advanced Topics in Neurocomputing: Explainability, Neuro-Symbolic Computing, AI Agents, LLM, Quantum Computing, PINN  
**Date:** July 1, 2026

---

## 1. Introduction

This assignment evaluates how well a small language model can generate correct Python code for a simple algorithmic task. The task is to generate programs that compute and print all Fibonacci numbers less than 100. Two types of implementations were tested: iterative and recursive. The main focus was on how the temperature parameter affects the quality of the generated code.

---

## 2. Methodology

### Model

The model used is **Qwen/Qwen2.5-Coder-0.5B-Instruct**, a 0.5 billion parameter instruction-tuned model built for code generation. It was chosen because it is small enough to run without heavy hardware but still capable of following coding instructions.

### Setup

The model was run on Google Colab using an A100 GPU. For each experiment, the model received a prompt asking it to write a Python program implementing the Fibonacci sequence (either iterative or recursive) and print all values less than 100.

Expected correct output: `0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89`

### Tested Settings

| Parameter | Values |
|-----------|--------|
| Temperature | 0.0, 0.3, 0.5, 0.7 |
| Top-p | 0.95 |
| Top-k | 50 |
| Trials per config | 2 |
| Implementation types | Iterative, Recursive |
| Total experiments | 16 |

Temperature controls how random the model's token selection is. At 0.0 the model always picks the most likely next token (greedy). Higher values introduce more randomness. Each generated program was automatically executed and its output was compared to the expected Fibonacci sequence.

---

## 3. Results and Observations

### Overall Results

| Metric | Overall | Iterative | Recursive |
|--------|---------|-----------|-----------|
| Executable | 100% | 100% | 100% |
| Correct | 25% | 50% | 0% |
| Exact Match | 25% | 50% | 0% |

### Effect of Temperature

| Temperature | Correct / Total | Correctness Rate |
|-------------|-----------------|------------------|
| 0.0 | 0 / 4 | 0% |
| 0.3 | 1 / 4 | 25% |
| 0.5 | 1 / 4 | 25% |
| 0.7 | 2 / 4 | 50% |

### Key Observations

- All 16 generated programs were syntactically valid and ran without errors. The model clearly understands Python syntax.
- The iterative approach worked well at higher temperatures. At T=0.7, both trials produced correct output.
- Greedy decoding (T=0.0) performed worst. The model produced code that ran but gave wrong output for both implementation types.
- Recursive implementations failed in all 8 trials. The model understood how to define a recursive Fibonacci function but got the output logic wrong — it typically computed Fibonacci up to index 100 and printed the full list, including large values well above 100.
- A small amount of randomness (T=0.7) helped the iterative implementation find the correct solution more reliably.

---

## 4. Conclusions

From these experiments, a few things became clear. First, the model is good at writing code that runs, but getting the logic exactly right is harder, especially for recursive tasks. Second, temperature 0.0 was not the best setting. Some randomness at T=0.7 improved results for iterative code. Third, the iterative approach was more reliable than recursive for this model and task.

The best configuration found was: **iterative implementation at T=0.7, top-p=0.95**, which produced correct output in both trials.

Overall, the model (0.5B parameters) shows reasonable code generation ability for simple iterative tasks, but struggles with tasks that require reasoning about output filtering in recursive contexts.

---

## Appendix: Sample Generated Code

### A. Correct Iterative Output (T=0.3)

```python
def fibonacci_sequence():
    a, b = 0, 1
    while a < 100:
        print(a)
        a, b = b, a + b

fibonacci_sequence()
```

Output: `0 1 1 2 3 5 8 13 21 34 55 89` ✓

### B. Incorrect Recursive Output (T=0.7)

The function logic is correct, but the output filtering is wrong — it prints a full list up to index 100 instead of stopping when the value exceeds 100.

```python
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

fib_sequence = [0, 1]
for i in range(2, 100):
    fib_sequence.append(fibonacci(i))

print("Fibonacci numbers less than 100:", fib_sequence)
```

---

## References

1. Qwen Team. *Qwen2.5-Coder Technical Report*. Alibaba Group, 2024. https://huggingface.co/Qwen/Qwen2.5-Coder-0.5B-Instruct
2. Thomas Wolf et al. *Transformers: State-of-the-Art Natural Language Processing*. Proceedings of EMNLP 2020.
