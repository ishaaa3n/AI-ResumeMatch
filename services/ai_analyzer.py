"""AI-powered resume analysis using Ollama"""
import json
from langchain_community.llms import Ollama

class ResumeAnalyzer:
    def __init__(self, model="llama3", temperature=0.3):
        self.llm = Ollama(model=model, temperature=temperature)
        
    def analyze_resume(self, resume_text, max_length=1500):
        """
        Analyze resume text and extract structured information
        
        Args:
            resume_text (str): Full resume text
            max_length (int): Maximum text length to analyze
            
        Returns:
            dict: Extracted information (name, title, skills, etc.)
        """
        # Truncate if too long
        resume_snippet = resume_text[:max_length] if len(resume_text) > max_length else resume_text
        
        extraction_prompt = """You are a resume parser. Extract info from this resume and return ONLY a JSON object (no markdown, no explanations).

Resume text:
{resume_text}

Return this exact JSON structure:
{{"full_name": "name here", "job_title": "title here", "years_experience": number, "top_skills": ["skill1", "skill2", "skill3"], "preferred_location": "Pune"}}

JSON only:"""
        
        try:
            # Get AI response
            raw_response = self.llm.invoke(
                extraction_prompt.format(resume_text=resume_snippet)
            )
            
            # Clean and parse response
            parsed_info = self._clean_and_parse(raw_response)
            return parsed_info
            
        except Exception as e:
            raise Exception(f"AI analysis failed: {str(e)}")
    
    def _clean_and_parse(self, raw_response):
        """Clean AI response and parse JSON"""
        cleaned = (raw_response or "").strip()
        
        if not cleaned:
            raise ValueError("Empty response from AI")
        
        # Remove markdown code blocks
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[1].split("```")[0].strip()
        
        # Extract JSON object
        if "{" in cleaned:
            cleaned = cleaned[cleaned.index("{"):]
        if "}" in cleaned:
            cleaned = cleaned[:cleaned.rindex("}") + 1]
        
        # Parse JSON
        return json.loads(cleaned)