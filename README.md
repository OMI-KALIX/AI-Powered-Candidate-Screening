# AI Candidate Screening System using LangGraph

An AI-powered candidate screening workflow built with **LangGraph**. The system processes a batch of resumes, evaluates each candidate across multiple dimensions, generates recruiter-friendly summaries, performs self-review for quality assurance, and exports the final results.

---

# Running the Project

## Option 1: Run Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Ollama

```bash
ollama serve
```

Pull the required model:

```bash
ollama pull qwen2.5:7b
#any model you want.
```

> Replace `qwen2.5:7b` if your project uses another model.

### 3. Run the application

```bash
python app.py
```

---

## Option 2: Run with Docker

### 1. Pull the Docker image

```bash
docker pull omikalix/ai-candidate-screening
```

### 2. Start Ollama

```bash
ollama serve
```

### 3. Pull the model

```bash
ollama pull qwen2.5:7b

#any model you want.
```

### 4. Run the container

```bash
docker run -p 8501:8501 omikalix/ai-candidate-screening
```

> **Note:** Keep the Ollama server running on your host machine before starting the Docker container.

---

# Tech Stack

* LangGraph
* LangChain
* Ollama
* Qwen2.5
* Python
* Pandas
* Docker

# Project Workflow

```text
Start
   │
   ▼
Load Batch
   │
   ▼
Initialize Candidate
   │
   ▼
Preprocess Resume
   │
   ▼
Feature Extraction
   │
   ▼
Technical Match
   │
   ▼
Seniority Match
   │
   ▼
Culture Match
   │
   ▼
Aggregate Score
   │
   ▼
Recruiter Summary
   │
   ▼
Self Review
   │
   ▼
Save Result
   │
   ├──────────────► Export CSV
   │                     │
   │                     ▼
   │                    End
   │
   └──────────────► Next Candidate
                         │
                         ▼
               Initialize Candidate
```

---

# LangGraph Nodes

## 1. load_batch

Loads the complete candidate dataset from the CSV file.

This node runs only once before processing individual candidates.

---

## 2. initialize_candidate

Initializes the workflow state for the next candidate.

Separating this node makes batch processing simple and scalable.

---

## 3. preprocess

Prepares the resume for evaluation.

Responsibilities:

* Normalize text
* Remove unnecessary whitespace
* Standardize input

---

## 4. feature_extraction

Extracts structured candidate information.

Examples:

* Skills
* Experience
* Education
* Projects
* Certifications

---

## 5. technical_match

Evaluates technical skills against job requirements.

Produces:

* Technical score
* Technical feedback

---

## 6. seniority_match

Evaluates:

* Years of experience
* Career progression
* Leadership experience

Produces:

* Seniority score
* Seniority feedback

---

## 7. culture_match

Evaluates:

* Communication
* Teamwork
* Adaptability
* Learning mindset

Produces:

* Culture score
* Culture feedback

---

## 8. aggregate_score

Combines all evaluation scores.

Produces:

* Final score
* Overall recommendation

---

## 9. recruiter_summary

Generates a recruiter-friendly summary including:

* Overall fit
* Strengths
* Weaknesses
* Hiring recommendation

---

## 10. self_review

Acts as the quality assurance layer.

Checks:

* Missing information
* Hallucinated claims
* Contradictions
* Score consistency
* Recommendation consistency
* Formatting quality

If any issue is detected, the summary is regenerated before continuing.

---

## 11. save_result

Stores the evaluated candidate.

---

## 12. next_candidate

Checks whether additional candidates remain.

If yes:

```text
initialize_candidate
```

Otherwise:

```text
export_csv
```

---

## 13. export_csv

Exports all evaluated candidates into a CSV file.

Runs only once after the entire batch has been processed.

---

# Conditional Edges

## Candidate Loop

```text
save_result
      │
      ▼
next_candidate
      │
      ├── More Candidates
      │
      ▼
initialize_candidate
```

Otherwise

```text
save_result
      │
      ▼
export_csv
```

---

## Self Review

If validation succeeds:

```text
Self Review
      │
      ▼
Save Result
```

Otherwise:

* Missing information
* Unsupported claims
* Contradictions
* Recommendation mismatch

The summary is regenerated before saving.

---

# Self Evaluation

The Self-Review stage verifies:

* Summary matches evaluation scores
* Recommendation aligns with scores
* No fabricated information
* No contradictions
* Complete output
* Readable recruiter summary

Only validated summaries are saved.

---

# Tradeoffs

Design decisions made during development:

* Modular nodes instead of one large LLM prompt for maintainability.
* Sequential execution improves explainability but increases latency.
* LLM reasoning provides richer evaluations than rule-based scoring.
* Self-review adds one additional model call but significantly improves reliability.

---

# Future Improvements

* Parallel execution of independent nodes
* Resume embeddings with semantic retrieval
* Job description matching
* ATS compatibility scoring
* Human-in-the-loop review
* Multi-model evaluation
* Interactive dashboard
* Database integration
* REST API deployment
* Streamlit interface
* PDF report generation

---

## Author

**OMI-KALIX**

© 2025
