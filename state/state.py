from typing import TypedDict


class CandidateState(TypedDict):

    candidates: list

    current_index: int

    candidate: dict

    features: dict

    technical_score: int

    seniority_score: int

    culture_score: int

    overall_score: float

    verdict:str

    confidence: float

    summary: str

    top_signal: str

    top_gap: str

    approved: bool

    results: list