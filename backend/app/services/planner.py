from datetime import date

from app.schemas.platform import Program, Recommendation, RecommendationRequest, SimulationRequest, StudentProfile

PROGRAMS = [
    Program(id="tum-ds", university="Technical University of Munich", country="Germany", city="Munich", name="MSc Data Engineering and Analytics", field="Data Science", duration_months=24, intake="Winter", deadline=date(2027, 5, 31), tuition_inr=0, living_inr=2700000, application_fee_inr=7500, min_cgpa=7.5, ielts=6.5, gre=None, prerequisites=["Mathematics", "Programming", "Statistics"], official_url="https://www.tum.de/en/studies/degree-programs/detail/data-engineering-and-analytics-master-of-science-msc", source_url="https://www.tum.de/en/studies/degree-programs", last_verified=date(2026, 8, 19)),
    Program(id="rwth-ds", university="RWTH Aachen University", country="Germany", city="Aachen", name="MSc Data Science", field="Data Science", duration_months=24, intake="Winter", deadline=date(2027, 3, 1), tuition_inr=0, living_inr=2200000, application_fee_inr=0, min_cgpa=7.0, ielts=6.5, gre=None, prerequisites=["Mathematics", "Programming", "Machine Learning"], official_url="https://www.rwth-aachen.de", source_url="https://www.rwth-aachen.de", last_verified=date(2026, 8, 19)),
    Program(id="saar-cs", university="Saarland University", country="Germany", city="Saarbrücken", name="MSc Computer Science", field="Computer Science", duration_months=24, intake="Winter", deadline=date(2027, 5, 15), tuition_inr=0, living_inr=2100000, application_fee_inr=0, min_cgpa=6.8, ielts=6.5, gre=None, prerequisites=["Programming", "Algorithms", "Mathematics"], official_url="https://www.uni-saarland.de", source_url="https://www.uni-saarland.de", last_verified=date(2026, 8, 19)),
    Program(id="melb-ds", university="The University of Melbourne", country="Australia", city="Melbourne", name="Master of Data Science", field="Data Science", duration_months=24, intake="February", deadline=date(2026, 10, 31), tuition_inr=5400000, living_inr=3400000, application_fee_inr=8500, min_cgpa=7.0, ielts=6.5, gre=None, prerequisites=["Mathematics", "Programming", "Statistics"], official_url="https://study.unimelb.edu.au", source_url="https://study.unimelb.edu.au", last_verified=date(2026, 8, 19)),
    Program(id="unsw-ai", university="UNSW Sydney", country="Australia", city="Sydney", name="Master of Information Technology (AI)", field="Artificial Intelligence", duration_months=24, intake="February", deadline=date(2026, 11, 30), tuition_inr=5100000, living_inr=3600000, application_fee_inr=9000, min_cgpa=6.5, ielts=6.5, gre=None, prerequisites=["Programming", "Mathematics"], official_url="https://www.unsw.edu.au", source_url="https://www.unsw.edu.au", last_verified=date(2026, 8, 19)),
    Program(id="monash-it", university="Monash University", country="Australia", city="Melbourne", name="Master of Data Science", field="Data Science", duration_months=24, intake="February", deadline=date(2026, 11, 15), tuition_inr=4900000, living_inr=3300000, application_fee_inr=7500, min_cgpa=6.5, ielts=6.5, gre=None, prerequisites=["Programming", "Statistics"], official_url="https://www.monash.edu", source_url="https://www.monash.edu", last_verified=date(2026, 8, 19)),
]


def assess(profile: StudentProfile, program: Program) -> Recommendation:
    normalized_cgpa = profile.cgpa / profile.cgpa_scale * 10
    academic = min(100, round(normalized_cgpa / (program.min_cgpa or 7) * 85))
    program_fit = 100 if any(program.field.lower() in field.lower() or field.lower() in program.field.lower() for field in profile.target_fields) else 68
    known_requirements = [program.min_cgpa, program.ielts]
    met = int(normalized_cgpa >= (program.min_cgpa or 0)) + (int(profile.tests.ielts >= program.ielts) if profile.tests.ielts is not None and program.ielts else 0)
    eligibility_fit = round(met / len(known_requirements) * 100)
    total = sum(v for v in [program.tuition_inr, program.living_inr, program.application_fee_inr] if v is not None)
    budget_fit = min(100, round(profile.total_budget_inr / total * 100)) if total else 50
    missing = []
    if normalized_cgpa < (program.min_cgpa or 0): missing.append("CGPA is below the published minimum")
    if program.ielts and profile.tests.ielts is None: missing.append("IELTS score is not available")
    elif program.ielts and profile.tests.ielts < program.ielts: missing.append("IELTS score is below the published minimum")
    if missing and normalized_cgpa < (program.min_cgpa or 0): eligibility = "NOT_ELIGIBLE"
    elif missing: eligibility = "MISSING_REQUIREMENTS"
    else: eligibility = "ELIGIBLE"
    budget_status = "WITHIN_BUDGET" if total <= profile.total_budget_inr else "SLIGHTLY_ABOVE" if total <= profile.total_budget_inr * 1.15 else "SIGNIFICANTLY_ABOVE"
    match = round(academic * .30 + program_fit * .25 + eligibility_fit * .20 + budget_fit * .10 + 80 * .10 + 85 * .05)
    category = "BEST_MATCH" if match >= 86 else "TARGET" if match >= 72 else "REACH"
    if budget_status == "WITHIN_BUDGET" and program.country == "Germany": category = "BUDGET_FRIENDLY"
    why = ["Your academic background aligns with the programme field", f"CGPA {'meets' if normalized_cgpa >= (program.min_cgpa or 0) else 'does not meet'} the published minimum"]
    if profile.tests.ielts is not None and program.ielts and profile.tests.ielts >= program.ielts: why.append("Your IELTS score meets the published minimum")
    actions = ["Verify prerequisites and credit compatibility on the official programme page"]
    if profile.tests.ielts is None: actions.insert(0, "Complete or add your IELTS score")
    return Recommendation(program=program, profile_match=match, eligibility=eligibility, category=category, total_cost_inr=total, budget_status=budget_status, score_breakdown={"academic_fit": academic, "program_fit": program_fit, "eligibility": eligibility_fit, "budget_fit": budget_fit}, why_match=why, potential_issues=missing or ["Prerequisite equivalence needs transcript verification"], next_actions=actions)


def recommendations(request: RecommendationRequest) -> list[Recommendation]:
    programmes = PROGRAMS
    countries = request.countries or request.profile.target_countries
    programmes = [p for p in programmes if p.country in countries]
    if request.field: programmes = [p for p in programmes if request.field.lower() in p.field.lower()]
    results = [assess(request.profile, p) for p in programmes]
    return sorted(results, key=lambda r: r.profile_match, reverse=True)


def simulate(request: SimulationRequest) -> dict:
    before = recommendations(RecommendationRequest(profile=request.profile))
    profile = request.profile.model_copy(deep=True)
    if request.simulated_cgpa is not None: profile.cgpa = request.simulated_cgpa
    if request.simulated_ielts is not None: profile.tests.ielts = request.simulated_ielts
    if request.simulated_budget_inr is not None: profile.total_budget_inr = request.simulated_budget_inr
    after = recommendations(RecommendationRequest(profile=profile, countries=request.countries))
    return {"before_count": len([r for r in before if r.eligibility == "ELIGIBLE"]), "after_count": len([r for r in after if r.eligibility == "ELIGIBLE"]), "recommendations": after[:10], "notice": "Simulation only — your saved profile has not changed."}
