import json
from openai import AsyncOpenAI
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def evaluate_cv(self, cv_text: str) -> dict:
        prompt = f"""
        You are an expert HR professional and Resume/CV evaluator. Evaluate the following CV text and provide a structured JSON response.
        Do NOT wrap the response in markdown blocks like ```json ... ```, just output the raw JSON object.
        
        The JSON must contain EXACTLY the following keys:
        - "overall_score": (integer 0-100)
        - "grammar_score": (integer 0-100)
        - "formatting_score": (integer 0-100)
        - "readability_score": (integer 0-100)
        - "experience_score": (integer 0-100)
        - "skills_score": (integer 0-100)
        - "education_score": (integer 0-100)
        - "professionalism": (integer 0-100)
        - "strengths": (list of strings)
        - "weaknesses": (list of strings)
        - "missing_keywords": (list of strings)
        - "missing_sections": (list of strings)
        - "recommendations": (list of strings)
        
        CV Text:
        {cv_text}
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a CV evaluation assistant that outputs raw JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Simple check if there are markdown json wrappers and strip them
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
                
            return json.loads(result_text.strip())
            
        except Exception as e:
            logger.error(f"Error evaluating CV with AI: {e}")
            # Fallback data if AI fails
            return {
                "overall_score": 0,
                "grammar_score": 0,
                "formatting_score": 0,
                "readability_score": 0,
                "experience_score": 0,
                "skills_score": 0,
                "education_score": 0,
                "professionalism": 0,
                "strengths": ["Failed to analyze"],
                "weaknesses": ["Failed to analyze"],
                "missing_keywords": [],
                "missing_sections": [],
                "recommendations": ["Please try again later"]
            }
