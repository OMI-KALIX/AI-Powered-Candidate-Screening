from typing import Literal
from pydantic import BaseModel,Field

class CandidateFeatures(BaseModel):

    skills: list[str]

    experience: str

    education: str

    certifications: list[str]

    projects: list[str]


class TechnicalAssessment(BaseModel):

    score: int = Field(ge=0, le=100)

    reasoning: str


class SeniorityAssessment(BaseModel):

    score: int = Field(ge=0, le=100)

    category: Literal[
        "Underqualified",
        "Good Match",
        "Overqualified"
    ]

    reasoning: str


class CultureAssessment(BaseModel):

    score: int = Field(ge=0, le=100)

    reasoning: str


class RecruiterSummary(BaseModel):

    summary: str

    top_signal: str

    top_gap: str


class ReviewAssessment(BaseModel):

    feedback: str

    approved: bool

    confidence: float