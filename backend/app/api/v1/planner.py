import re
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.dependencies.auth import get_current_email
from app.schemas.platform import RecommendationRequest, SimulationRequest, StudentProfile
from app.services.planner import PROGRAMS, recommendations, simulate

router = APIRouter(tags=["planning"])
profiles: dict[str, StudentProfile] = {}
shortlists: dict[str, set[str]] = {}
documents: dict[str, list[dict]] = {}
applications: dict[str, list[dict]] = {}
CurrentUser = Annotated[str, Depends(get_current_email)]


@router.get("/programs")
def list_programs(country: str | None = None, field: str | None = None):
    results = PROGRAMS
    if country: results = [p for p in results if p.country.lower() == country.lower()]
    if field: results = [p for p in results if field.lower() in p.field.lower() or field.lower() in p.name.lower()]
    return results


@router.get("/programs/{program_id}")
def get_program(program_id: str):
    program = next((p for p in PROGRAMS if p.id == program_id), None)
    if not program: raise HTTPException(404, "Program not found")
    return program


@router.get("/profile")
def get_profile(user: CurrentUser):
    if user not in profiles: raise HTTPException(404, "No profile saved yet")
    return profiles[user]


@router.put("/profile")
def save_profile(profile: StudentProfile, user: CurrentUser):
    profiles[user] = profile
    return profile


@router.post("/recommendations")
def create_recommendations(request: RecommendationRequest, _: CurrentUser):
    return recommendations(request)[:10]


@router.get("/recommendations/top10")
def top_ten(user: CurrentUser):
    if user not in profiles: raise HTTPException(400, "Save a student profile first")
    return recommendations(RecommendationRequest(profile=profiles[user]))[:10]


@router.post("/simulation")
def run_simulation(request: SimulationRequest, _: CurrentUser): return simulate(request)


@router.post("/shortlist/{program_id}")
def shortlist(program_id: str, user: CurrentUser):
    if not any(p.id == program_id for p in PROGRAMS): raise HTTPException(404, "Program not found")
    shortlists.setdefault(user, set()).add(program_id)
    return {"shortlisted": list(shortlists[user])}


@router.get("/shortlist")
def get_shortlist(user: CurrentUser): return [p for p in PROGRAMS if p.id in shortlists.get(user, set())]


@router.post("/documents/resume")
async def upload_resume(user: CurrentUser, file: UploadFile = File(...)):
    if file.content_type not in {"application/pdf", "text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}:
        raise HTTPException(415, "Upload a PDF, DOCX, or TXT resume")
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")
    extracted = {"email": (re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text) or [None])[0], "cgpa": (re.search(r"(?:CGPA|GPA)\s*[:=-]?\s*(\d(?:\.\d+)?)", text, re.I) or [None, None])[1], "skills": re.findall(r"(?:Python|Java|SQL|Machine Learning|Data Science|React|C\+\+)", text, re.I)[:8]}
    document = {"id": f"resume-{len(documents.get(user, [])) + 1}", "name": file.filename, "type": "RESUME", "uploaded_at": str(date.today()), "status": "AI_EXTRACTED_REVIEW_REQUIRED", "extracted": extracted}
    documents.setdefault(user, []).append(document)
    return {"document": document, "notice": "Resume extraction is a draft. Please review before saving your profile."}


@router.get("/documents")
def list_documents(user: CurrentUser): return documents.get(user, [])


@router.post("/applications/{program_id}")
def add_application(program_id: str, user: CurrentUser):
    program = next((p for p in PROGRAMS if p.id == program_id), None)
    if not program: raise HTTPException(404, "Program not found")
    record = {"id": f"app-{len(applications.get(user, [])) + 1}", "program_id": program_id, "university": program.university, "program": program.name, "status": "SHORTLISTED", "updated_at": str(date.today())}
    applications.setdefault(user, []).append(record)
    return record


@router.get("/applications")
def list_applications(user: CurrentUser): return applications.get(user, [])


@router.post("/ai/advisor")
def advisor(profile: StudentProfile, _: CurrentUser):
    results = recommendations(RecommendationRequest(profile=profile)); actions = []
    if profile.tests.ielts is None: actions.append({"priority": 1, "action": "Book IELTS", "reason": "Several matching programmes publish an IELTS minimum."})
    actions += [{"priority": len(actions) + 1, "action": "Upload and map your transcript", "reason": "Prerequisite equivalence needs manual verification."}, {"priority": len(actions) + 2, "action": "Shortlist programmes before deadlines", "reason": f"{len(results)} demo programmes match your profile."}]
    return {"actions": actions, "disclaimer": "Planning guidance only. Verify requirements on official programme pages."}
