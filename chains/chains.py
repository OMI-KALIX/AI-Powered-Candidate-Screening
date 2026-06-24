from prompts.prompts import (feature_prompt,
                             technical_prompt,
                             seniority_prompt,
                             culture_prompt,
                             summary_prompt,
                             review_prompt)

from model.model import llm
from schemas.schema import (CandidateFeatures,
                            TechnicalAssessment,
                            SeniorityAssessment,
                            CultureAssessment,
                            RecruiterSummary,
                            ReviewAssessment)

feature_chain = (

    feature_prompt

    |

    llm.with_structured_output(

        CandidateFeatures

    )

)

technical_chain = (
    technical_prompt
    |
    llm.with_structured_output(
        TechnicalAssessment
    )
)

seniority_chain = (
    seniority_prompt
    |
    llm.with_structured_output(
        SeniorityAssessment
    )
)

culture_chain = (
    culture_prompt
    |
    llm.with_structured_output(
        CultureAssessment
    )
)

summary_chain = (
    summary_prompt
    |
    llm.with_structured_output(
        RecruiterSummary
    )
)

review_chain = (
    review_prompt
    |
    llm.with_structured_output(
        ReviewAssessment
    )
)