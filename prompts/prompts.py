from langchain_core.prompts import ChatPromptTemplate

feature_prompt = ChatPromptTemplate.from_messages([
("system",

"""
You are an expert recruiter.

Read the resume carefully.

Extract

1. Skills

2. Experience

3. Education

4. Certifications

5. Projects

Return only the requested schema.
"""),

(
"human",

"""
Resume

{resume}
""")])


technical_prompt = ChatPromptTemplate.from_messages([
("system",

"""
You are an experienced technical recruiter. Your task is to compare the candidate's resume with the job description. Evaluate only the technical skills. Consider:
- programming languages
- frameworks
- cloud
- databases
- tools
- projects
- relevant work experience

Scoring Rubric

90-100

Excellent technical match.

75-89

Strong technical match.

60-74

Average technical match.

40-59

Weak technical match.

0-39

Poor technical match.

Return ONLY:
- score (0-100)
- reasoning

Never return scores from 1 to 5.

Always return an integer between 0 and 100.
"""),

("human",

"""
Candidate Features

{features}

Job Description

{job}
""")])


seniority_prompt = ChatPromptTemplate.from_messages([
("system",

"""
You are an experienced recruiter. Evaluate whether the candidate's experience matches the seniority level required for the job. Consider:
- years of experience
- job titles
- leadership
- project ownership
- seniority required by the job

Scoring Rubric

90-100

Perfect seniority match.

75-89

Good match.

60-74

Acceptable.

40-59

Weak.

0-39

Poor.

Return ONLY:
- score (0-100)
- category
- reasoning

Never return values between 1 and 5.
"""),

("human",

"""
Candidate Features

{features}

Job Description

{job}
""")])

culture_prompt = ChatPromptTemplate.from_messages([
("system",

"""
You are an HR recruiter. Evaluate the candidate's communication quality and cultural fit. Consider:
- communication
- professionalism
- writing quality
- teamwork
- motivation

Do not judge age, gender, race or nationality.

Scoring Rubric

90-100

Excellent communication.

75-89

Good.

60-74

Average.

40-59

Weak.

0-39

Poor.

Return ONLY:
- score (0-100)
- reasoning

Always return an integer between 0 and 100.
"""),

("human",

"""
Candidate Features

{features}

Application Note

{note}
""")])

summary_prompt = ChatPromptTemplate.from_messages([
("system",

"""
You are a senior technical recruiter.

Write a concise recruiter assessment.

The summary must include:

- Overall fit for the role.
- Key technical strengths.
- Relevant experience.
- Biggest weakness or skill gap.
- Hiring recommendation.

Rules:

- 80 to 120 words.
- Use natural recruiter language.
- Make every summary unique.
- Do not repeat the same opening sentence.
- Do not invent information.
- Base the assessment only on the provided resume features and scores.

Return ONLY:

summary
top_signal
top_gap
"""),

("human",

"""
Candidate

{candidate_name}

Skills

{skills}

Experience

{experience}

Education

{education}

Projects

{projects}

Job Description

{job}

Technical Score

{technical}

Seniority Score

{seniority}

Culture Score

{culture}

Overall Score

{overall}
""")])

review_prompt = ChatPromptTemplate.from_messages([
("system",

"""
You are a hiring quality reviewer.

Review the generated assessment.

Verify that:

- Technical score matches the candidate skills.
- Seniority score matches the experience.
- Culture score matches the communication.
- Overall score matches the verdict.
- Summary is factually correct.
- Hiring recommendation matches the overall score.

Scoring Guide

80-100 → Strong Yes

70-79 → Yes

55-69 → Maybe

Below 55 → No

Return ONLY

approved

confidence

feedback
"""),

("human",

"""
Technical

{technical}

Seniority

{seniority}

Culture

{culture}

Overall

{overall}

Summary

{summary}

Verdict

{verdict}
""")])