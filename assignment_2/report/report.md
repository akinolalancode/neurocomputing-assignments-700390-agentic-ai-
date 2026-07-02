# Assignment 2: Email Intent Extraction System
## Prompt Engineering for Structured Information Extraction

**Student ID:** 12349031  
**Course:** 700.390 Advanced Topics in Neurocomputing: Explainability, Neuro-Symbolic Computing, AI Agents, LLM, Quantum Computing, PINN

---

## 1. Introduction

This assignment builds an LLM-based system to extract structured information from student emails. The goal is to design a prompt that reliably reads an incoming email and outputs a valid JSON object with predefined fields. The prompt needs to handle different scenarios: clear requests, missing information, ambiguous intent, and emails with irrelevant content.

The core idea is to treat the prompt as an engineering artifact. Instead of writing a one-time message, the prompt is designed as a contract that specifies what the model should do, what constraints it must follow, and exactly what format the output should have.

---

## 2. System Design

### Model

The model used is `Qwen/Qwen2.5-1.5B-Instruct` — 1.5 billion parameters, instruction-tuned. Run on Google Colab using an A100 GPU. This model is larger than the one used in Assignment 1 and better suited for tasks that require following structured output formats.

### Prompt Contract

The prompt was designed as a system message with five parts:

- **Role:** Academic administration assistant
- **Task:** Extract student data and classify the intent of the email
- **Context:** Use only the email content, do not rely on outside knowledge
- **Constraints:** Do not invent or guess any missing information
- **Output:** Return valid JSON only, with no extra text

The required output format includes six fields: `student_name`, `student_id`, `email_intent`, `course_or_exam`, `confidence`, and `missing_information`.

**Full system prompt:**

```
You are an academic administration assistant.
Your task is to read a student email and extract information from it.

Extract exactly these fields:
- student_name: full name of the student, or null if not given
- student_id: student ID number as a string, or null if not given
- email_intent: one of "register", "deregister", or "unknown" if unclear
- course_or_exam: the course or exam mentioned, or null if not given
- confidence: "high" if intent is clear, "medium" if somewhat clear, "low" if ambiguous
- missing_information: list of field names that are missing, e.g. ["student_id"]

Rules:
- Use ONLY what is written in the email. Do not guess or invent anything.
- If intent is ambiguous or unclear, set email_intent to "unknown" and confidence to "low".
- Return ONLY valid JSON. No explanation, no markdown, no extra text.

Output format:
{"student_name": "...", "student_id": "...", "email_intent": "...",
 "course_or_exam": "...", "confidence": "...", "missing_information": []}
```

Temperature was set to **0.1** for consistent, deterministic extraction outputs.

---

## 3. Test Emails

| Email | Scenario | Description |
|-------|----------|-------------|
| 1 | Clear registration | Student provides full name, student ID, and course name. Intent is explicitly to register. |
| 2 | Clear deregistration | Student states they want to deregister from an exam. All fields present. |
| 3 | Missing student ID | Student wants to register but does not mention their student ID. |
| 4 | Ambiguous intent | Student says they registered before but is unsure whether to stay or withdraw. |
| 5 | Extra irrelevant info | Email includes unrelated sentences about weather and hiking, but a clear registration request is present. |

---

## 4. Results

All five emails produced valid JSON output.

| Email | Intent | Confidence | ID Found | Missing Field | Valid JSON |
|-------|--------|------------|----------|---------------|------------|
| 1 | register | high | yes | none | ✓ |
| 2 | deregister | high | yes | none | ✓ |
| 3 | register | high | null | *not reported* | ✓* |
| 4 | register | high | yes | none | ✓* |
| 5 | register | high | yes | none | ✓ |

*\* Valid JSON but contains incorrect field values (see Discussion)*

**Generation time per email:**

| Email | Scenario | Time (s) |
|-------|----------|----------|
| 1 | Clear registration | 3.12 |
| 2 | Clear deregistration | 1.86 |
| 3 | Missing student ID | 1.50 |
| 4 | Ambiguous intent | 1.76 |
| 5 | Extra irrelevant info | 1.64 |
| | **Average** | **1.98** |

### Individual Outputs

Emails 1 and 2 were fully correct. The model correctly identified the intent, extracted all fields, and returned them in the required format.

For email 3 (missing student ID), the model correctly set `student_id` to `null`, but the `missing_information` field was left as an empty list instead of `["student_id"]`.

For email 4 (ambiguous intent), the model returned `email_intent: "register"` with `confidence: "high"`, even though the student explicitly stated they were unsure whether to stay or withdraw.

For email 5, the model correctly ignored the unrelated sentences about weather and hiking and extracted the registration request correctly.

---

## 5. Discussion

### Email 3 — Missing student ID

The model correctly set `student_id` to `null`, which shows it understood that the ID was not present. However, it did not populate the `missing_information` array. This is likely because the prompt gave an example format with an empty list, and the model followed the example rather than reasoning about which fields were actually missing.

**Fix:** Rewrite the instruction for `missing_information` more explicitly, or remove the empty list from the output example.

### Email 4 — Ambiguous intent

The model failed to detect the ambiguity. The student said they "registered last semester" but were "not sure if I should stay or withdraw." The model interpreted "registered" as the current intent and returned `register` with high confidence. Small models often struggle with negation and uncertainty detection.

**Fix:** Include a few-shot example in the prompt that shows an ambiguous case and the expected `"unknown"` output.

### Email 5 — Extra irrelevant information

The model handled this well — it ignored the sentences about weather and hiking and focused on the relevant parts of the email.

---

## 6. Conclusion

This assignment shows that a small instruction-tuned model can reliably extract structured information from student emails and produce valid JSON when given a well-defined prompt. The system achieved a 5/5 valid JSON rate and was fully correct on 3 out of 5 emails.

The main weaknesses were in handling the `missing_information` field and detecting ambiguous intent. Both issues point to limitations in how small models follow multi-step conditional instructions. These could be addressed by revising the prompt with more explicit instructions and few-shot examples for the edge cases.

---

## Appendix: Full JSON Outputs

**Email 1 — Clear registration request**
```json
{
  "student_name": "John Smith",
  "student_id": "2045123",
  "email_intent": "register",
  "course_or_exam": "Advanced Topics in Neurocomputing",
  "confidence": "high",
  "missing_information": []
}
```

**Email 2 — Clear deregistration request**
```json
{
  "student_name": "Maria Garcia",
  "student_id": "2045456",
  "email_intent": "deregister",
  "course_or_exam": "Advanced Topics in Neurocomputing",
  "confidence": "high",
  "missing_information": []
}
```

**Email 3 — Missing student ID**
```json
{
  "student_name": "Ahmed Hassan",
  "student_id": null,
  "email_intent": "register",
  "course_or_exam": "Quantum Computing module",
  "confidence": "high",
  "missing_information": []
}
```

**Email 4 — Ambiguous intent**
```json
{
  "student_name": "Lisa Chen",
  "student_id": "2045789",
  "email_intent": "register",
  "course_or_exam": "Advanced Topics in Neurocomputing",
  "confidence": "high",
  "missing_information": []
}
```

**Email 5 — Extra irrelevant information**
```json
{
  "student_name": "Tom Brown",
  "student_id": "2045321",
  "email_intent": "register",
  "course_or_exam": "AI Agents",
  "confidence": "high",
  "missing_information": []
}
```

---

## References

1. Qwen Team. *Qwen2.5 Technical Report*. arXiv:2412.15115, 2025.
2. T. Wolf et al. *Transformers: State-of-the-Art Natural Language Processing*. EMNLP 2020.
