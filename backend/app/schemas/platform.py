from datetime import date
from typing import Literal

from pydantic import BaseModel, EmailStr, Field

Eligibility = Literal["ELIGIBLE", "POTENTIALLY_ELIGIBLE", "MISSING_REQUIREMENTS", "NOT_ELIGIBLE", "UNKNOWN"]


class TestScores(BaseModel):
    ielts: float | None = Field(default=None, ge=0, le=9)
    toefl: int | None = Field(default=None, ge=0, le=120)
    gre: int | None = Field(default=None, ge=260, le=340)


class StudentProfile(BaseModel):
    name: str = "Future student"
    email: EmailStr
    college: str
    degree: str
    major: str
    cgpa: float = Field(ge=0, le=10)
    cgpa_scale: float = Field(default=10, gt=0)
    graduation_year: int = Field(ge=2020, le=2035)
    target_countries: list[Literal["Germany", "Australia"]] = ["Germany", "Australia"]
    target_fields: list[str] = ["Data Science"]
    preferred_intake: str = "Winter 2027"
    total_budget_inr: int = Field(ge=0)
    budget_flexibility: Literal["STRICT", "MODERATE", "FLEXIBLE"] = "MODERATE"
    tests: TestScores = TestScores()


class Program(BaseModel):
    id: str
    university: str
    country: Literal["Germany", "Australia"]
    city: str
    name: str
    field: str
    duration_months: int
    intake: str
    deadline: date
    tuition_inr: int | None
    living_inr: int | None
    application_fee_inr: int | None
    min_cgpa: float | None
    ielts: float | None
    gre: int | None
    prerequisites: list[str]
    official_url: str
    source_url: str
    last_verified: date
    source_label: str = "SEED / DEMO DATA — verify on official website"


class Recommendation(BaseModel):
    program: Program
    profile_match: int
    eligibility: Eligibility
    category: Literal["BEST_MATCH", "SAFE", "TARGET", "REACH", "BUDGET_FRIENDLY"]
    total_cost_inr: int | None
    budget_status: Literal["WITHIN_BUDGET", "SLIGHTLY_ABOVE", "SIGNIFICANTLY_ABOVE", "UNKNOWN"]
    score_breakdown: dict[str, int]
    why_match: list[str]
    potential_issues: list[str]
    next_actions: list[str]


class RecommendationRequest(BaseModel):
    profile: StudentProfile
    countries: list[Literal["Germany", "Australia"]] | None = None
    field: str | None = None
    max_budget_inr: int | None = None


class SimulationRequest(BaseModel):
    profile: StudentProfile
    simulated_cgpa: float | None = Field(default=None, ge=0, le=10)
    simulated_ielts: float | None = Field(default=None, ge=0, le=9)
    simulated_budget_inr: int | None = Field(default=None, ge=0)
    countries: list[Literal["Germany", "Australia"]] | None = None

