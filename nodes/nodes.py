
import pandas as pd

from state.state import CandidateState
from chains.chains import (feature_chain,
                           review_chain,
                           culture_chain,
                           seniority_chain,
                           technical_chain,
                           summary_chain)


def load_batch(state: CandidateState):

    df = pd.read_csv("candidates.csv")

    return {"candidates": df.to_dict("records"),

        "current_index": 0,

        "results": []}

def initialize_candidate(state: CandidateState):

    candidate = state["candidates"][state["current_index"]]

    return {"candidate": candidate}

def preprocess(state: CandidateState):

    candidate = state["candidate"]

    resume = candidate["resume"].strip()

    note = candidate.get("application_note", "").strip()

    job = candidate["job_description"].strip()

    candidate["resume"] = resume

    candidate["application_note"] = note

    candidate["job_description"] = job

    return {"candidate": candidate}

def feature_extraction(state: CandidateState):

    candidate = state["candidate"]

    response = feature_chain.invoke({"resume": candidate["resume"]})

    return {"features": response.model_dump()}

def technical_match(state: CandidateState):

    candidate = state["candidate"]

    response = technical_chain.invoke({

        "features": state["features"],

        "job": candidate["job_description"]})

    return {"technical_score": response.score}

def seniority_match(state: CandidateState):

    candidate = state["candidate"]

    response = seniority_chain.invoke({

        "features": state["features"],

        "job": candidate["job_description"]})

    return {"seniority_score": response.score}


def culture_match(state: CandidateState):

    candidate = state["candidate"]

    response = culture_chain.invoke({

        "features": state["features"],

        "note": candidate["application_note"]})

    return {"culture_score": response.score}


def aggregate_score(state: CandidateState):

    technical = state["technical_score"]
    seniority = state["seniority_score"]
    culture = state["culture_score"]

    overall = round((technical + seniority + culture) / 3, 1)

    if overall >= 85:
        verdict = "Strong Yes"
    elif overall >= 70:
        verdict = "Yes"
    elif overall >= 55:
        verdict = "Maybe"
    else:
        verdict = "No"

    if overall >= 90:
        confidence = 98
    elif overall >= 80:
        confidence = 92
    elif overall >= 70:
        confidence = 85
    elif overall >= 60:
        confidence = 75
    elif overall >= 50:
        confidence = 65
    else:
        confidence = 50

    return {
        "overall_score": overall,
        "verdict": verdict,
        "confidence": confidence
    }

def recruiter_summary(state: CandidateState):

    candidate = state["candidate"]

    response = summary_chain.invoke({
            "candidate_name": candidate["candidate_name"],

            "skills": ", ".join(state["features"]["skills"]),

            "experience": state["features"]["experience"],

            "education": state["features"]["education"],

            "projects": ", ".join(state["features"]["projects"]),

            "technical": state["technical_score"],

            "seniority": state["seniority_score"],

            "culture": state["culture_score"],

            "overall": state["overall_score"],

            "job": candidate["job_description"]})

    return {"summary": response.summary,

            "top_signal": response.top_signal,

            "top_gap": response.top_gap
        }

def self_review(state: CandidateState):

    response = review_chain.invoke({

            "technical": state["technical_score"],

            "seniority": state["seniority_score"],

            "culture": state["culture_score"],

            "summary": state["summary"],

            "verdict": state["verdict"],

            "confidence": state["confidence"],

            "overall": state["overall_score"]
            })

    return {"approved": response.approved,

            "confidence": response.confidence}

def save_result(state: CandidateState):

    result = {

        "Candidate": state["candidate"]["candidate_name"],

        "Technical Score": state["technical_score"],

        "Seniority Score": state["seniority_score"],

        "Culture Score": state["culture_score"],

        "Overall Score": state["overall_score"],

        "Verdict": state["verdict"],

        "Confidence": state["confidence"],

        "Summary": state["summary"],

        "Top Signal": state["top_signal"],

        "Top Gap": state["top_gap"]

    }

    results = state["results"]

    results.append(result)

    return {"results": results}

def next_candidate_router(state: CandidateState):

    if state["current_index"] < len(state["candidates"]) - 1:

        return "next"

    return "export"


def next_candidate(state: CandidateState):

    return {"current_index": state["current_index"] + 1}

def export_csv(state: CandidateState):

    df = pd.DataFrame(state["results"])

    df.to_csv("candidate_results.csv",index=False)

    print(df)

    print("\nCSV Exported Successfully.")

    return state