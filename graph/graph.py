from langgraph.graph import StateGraph,START,END
from state.state import CandidateState
import pandas as pd


from nodes.nodes import (load_batch,
                         initialize_candidate,
                         preprocess,
                         feature_extraction,
                         technical_match,
                         seniority_match,
                         culture_match,
                         aggregate_score,
                         recruiter_summary,
                         self_review,
                         save_result,
                         next_candidate,export_csv,
                         next_candidate_router)


builder = StateGraph(CandidateState)
builder.add_node("load_batch", load_batch)

builder.add_node("initialize_candidate", initialize_candidate)

builder.add_node("preprocess", preprocess)
builder.add_node("feature_extraction",feature_extraction)
builder.add_node("technical_match", technical_match)

builder.add_node("seniority_match", seniority_match)

builder.add_node("culture_match", culture_match)

builder.add_node("aggregate_score", aggregate_score)

builder.add_node("recruiter_summary", recruiter_summary)

builder.add_node("self_review", self_review)

builder.add_node("save_result", save_result)

builder.add_node("next_candidate", next_candidate)

builder.add_node("export_csv", export_csv)


builder.add_edge(
    START,
    "load_batch"
)


builder.add_edge(
    "load_batch",
    "initialize_candidate"
)

builder.add_edge(
    "initialize_candidate",
    "preprocess"
)

builder.add_edge(
    "preprocess",
    "feature_extraction"
)

builder.add_edge(
    "feature_extraction",
    "technical_match"
)

builder.add_edge(
    "technical_match",
    "seniority_match"
)

builder.add_edge(
    "seniority_match",
    "culture_match"
)

builder.add_edge(
    "culture_match",
    "aggregate_score"
)

builder.add_edge(
    "aggregate_score",
    "recruiter_summary"
)

builder.add_edge(
    "recruiter_summary",
    "self_review"
)

builder.add_edge(
    "self_review",
    "save_result"
)


builder.add_conditional_edges(
    "save_result",
    next_candidate_router,
    {
        "next": "next_candidate",
        "export": "export_csv"
    }
)

builder.add_edge(
    "next_candidate",
    "initialize_candidate"
)


builder.add_edge(
    "export_csv",
    END
)

graph = builder.compile()

graph.get_graph().draw_mermaid_png(
    output_file_path="candidate_screening_intern_graph.png"
)
