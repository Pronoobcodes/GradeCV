import uuid
from typing import Optional
from app.repositories.grading_repository import GradingRepository
from app.schemas.grading import GradingCreate
from app.services.ai_service import AIService
from app.services.ats_service import ATSService
from app.models.cv import CV

class GradingService:
    def __init__(self, grading_repo: GradingRepository):
        self.grading_repo = grading_repo
        self.ai_service = AIService()
        self.ats_service = ATSService()

    async def grade_cv(self, cv: CV, user_id: uuid.UUID):
        # 1. Calculate ATS Score locally
        ats_score = self.ats_service.calculate_ats_score(cv.extracted_text)
        
        # 2. Get AI Evaluation
        ai_eval = await self.ai_service.evaluate_cv(cv.extracted_text)
        
        # 3. Create Grading Record
        grading_create = GradingCreate(
            cv_id=cv.id,
            user_id=user_id,
            overall_score=ai_eval.get("overall_score", 0),
            ats_score=ats_score,
            grammar_score=ai_eval.get("grammar_score", 0),
            formatting_score=ai_eval.get("formatting_score", 0),
            readability_score=ai_eval.get("readability_score", 0),
            experience_score=ai_eval.get("experience_score", 0),
            skills_score=ai_eval.get("skills_score", 0),
            education_score=ai_eval.get("education_score", 0),
            strengths=ai_eval.get("strengths", []),
            weaknesses=ai_eval.get("weaknesses", []),
            missing_keywords=ai_eval.get("missing_keywords", []),
            recommendations=ai_eval.get("recommendations", []),
            ai_feedback="Analysis completed successfully." if ai_eval.get("overall_score", 0) > 0 else "Analysis failed."
        )
        
        grading_record = await self.grading_repo.create(grading_create)
        return grading_record
