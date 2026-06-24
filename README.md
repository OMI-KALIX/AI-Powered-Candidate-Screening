# AI Candidate Screening System using LangGraph

An AI-powered candidate screening workflow built with LangGraph. The system processes a batch of resumes, evaluates each candidate across multiple dimensions, generates recruiter-friendly summaries, performs self-review for quality assurance, and exports the final results.

---

# Running the Project

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

## 2. Start Ollama

Make sure Ollama is installed, then start the Ollama server:

```bash
ollama serve
```

In a separate terminal, pull the required model (if you haven't already):

```bash
ollama pull qwen2.5:7b
```

> Replace `qwen2.5:7b` with the model your project uses if it's different.

## 3. Run the application

```bash
python app.py
```

---

# Project Workflow

```
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

This node is separated because batch loading happens only once before processing individual candidates.

---

## 2. initialize_candidate

Selects the next candidate from the batch and initializes the workflow state for that candidate.

Keeping this as a separate node makes it easy to iterate over multiple candidates without restarting the graph.

---

## 3. preprocess

Cleans and standardizes resume data before evaluation.

Responsibilities include:

- Normalizing text
- Removing unnecessary whitespace
- Preparing structured input for downstream evaluation

Separating preprocessing ensures every evaluator receives consistent input.

---

## 4. feature_extraction

Extracts relevant information from the resume.

Examples:

- Skills
- Experience
- Education
- Projects
- Certifications

This node isolates information extraction from scoring logic.

---

## 5. technical_match

Evaluates the candidate's technical skills against the required job skills.

Produces:

- Technical feedback
- Technical score

Keeping technical evaluation independent makes it reusable for different roles.

---

## 6. seniority_match

Determines whether the candidate's experience level matches the job requirements.

Evaluates:

- Years of experience
- Role progression
- Leadership experience

Produces:

- Seniority feedback
- Seniority score

---

## 7. culture_match

Evaluates non-technical qualities such as:

- Communication
- Teamwork
- Adaptability
- Learning mindset

Produces:

- Culture feedback
- Culture score

Keeping this separate prevents mixing technical and behavioral evaluation.

---

## 8. aggregate_score

Combines all evaluation scores into a final candidate score.

Calculates:

- Overall score
- Overall recommendation

This node acts as the central scoring component.

---

## 9. recruiter_summary

Generates a recruiter-friendly summary describing:

- Overall fit
- Key strengths
- Major weaknesses
- Hiring recommendation

This separates evaluation from presentation.

---

## 10. self_review

Reviews the generated summary before saving the result.

Checks include:

- Missing information
- Contradictory statements
- Hallucinated information
- Score consistency
- Recommendation consistency
- Formatting quality

If an issue is detected, the node regenerates or corrects the summary before continuing.

This improves reliability without affecting earlier evaluation nodes.

---

## 11. save_result

Stores the evaluated candidate into the final results list.

Keeping persistence separate makes exporting easier.

---

## 12. next_candidate

Determines whether more candidates remain in the batch.

If candidates remain:

Returns to

```
initialize_candidate
```

Otherwise proceeds to export.

---

## 13. export_csv

Exports all processed candidates into a CSV file.

This node executes only once after every candidate has been processed.

---

# Conditional Edges

The workflow contains two conditional branches.

## Candidate Loop

After saving a candidate:

If additional candidates exist

```
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

```
save_result
        │
        ▼
export_csv
```

---

## Self Review

The self-review node validates the generated recruiter summary.

If the summary passes all validation checks

```
Self Review
      │
      ▼
Save Result
```

If problems are detected

- Missing information
- Contradictions
- Unsupported claims
- Inconsistent recommendation

The summary is regenerated before continuing.

---

# Self Evaluation

The self-evaluation stage acts as a quality control layer.

It verifies:

- Summary matches evaluation scores
- No fabricated information
- Recommendation aligns with scores
- Output is complete
- Output is readable
- No contradictory statements

Only validated summaries are saved.

---

# Tradeoffs

Several design tradeoffs were made during development.

- Multiple specialized nodes were preferred over a single large evaluation node to improve modularity and maintainability.
- LLM evaluations provide richer reasoning but increase latency.
- Sequential evaluation improves interpretability at the expense of execution speed.
- Self-review adds additional model calls but significantly improves output quality.

---

# Future Improvements

With additional time, the following improvements would be implemented:

- Parallel execution of independent evaluation nodes
- Resume embedding and semantic retrieval
- Job description matching
- ATS compatibility scoring
- Human-in-the-loop review
- Multi-model evaluation
- Interactive dashboard
- Database integration
- REST API deployment
- Streamlit interface
- PDF report generation

---

## Author

© 2025 OMI-KALIX

---
