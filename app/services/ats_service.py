import re

class ATSService:
    @staticmethod
    def calculate_ats_score(cv_text: str) -> int:
        """
        Calculates a heuristic ATS score based on common CV elements.
        Returns a score out of 100.
        """
        score = 0
        text_lower = cv_text.lower()
        
        # Check for contact info (basic heuristics)
        if re.search(r'[\w\.-]+@[\w\.-]+', text_lower):
            score += 10 # Has email
            
        if re.search(r'(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}', text_lower) or \
           re.search(r'\d{10}', text_lower):
            score += 10 # Has phone number
            
        # Check for standard sections
        sections = {
            "experience": ["experience", "employment", "work history"],
            "education": ["education", "academic background"],
            "skills": ["skills", "core competencies", "technologies"],
            "summary": ["summary", "profile", "objective"]
        }
        
        section_score = 0
        for section, keywords in sections.items():
            if any(keyword in text_lower for keyword in keywords):
                section_score += 15
        
        score += min(section_score, 60) # Max 60 points for sections
        
        # Length check (not too short, not too long)
        word_count = len(cv_text.split())
        if 300 <= word_count <= 1000:
            score += 20
        elif 150 <= word_count < 300 or 1000 < word_count <= 1500:
            score += 10
            
        return min(score, 100)
