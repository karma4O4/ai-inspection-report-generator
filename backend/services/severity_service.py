import os
import openai
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class SeverityService:
    @staticmethod
    def _get_client():
        if OPENAI_API_KEY and not OPENAI_API_KEY.startswith("sk-proj-your"):
            return openai.OpenAI(api_key=OPENAI_API_KEY)
        return None

    @classmethod
    def analyze_severity(cls, description: str) -> str:
        """
        Uses OpenAI GPT-4o to analyze a defect description and return a severity level:
        Critical, High, Medium, or Low.
        Falls back to rule-based classification if OpenAI is not configured or fails.
        """
        client = cls._get_client()
        if client and description:
            try:
                prompt = f"""You are a professional building inspector. Analyze the following defect description from an inspection report and assign a single severity level.
The severity level MUST be exactly one of: Critical, High, Medium, Low.

Defect Description:
{description}

Respond with only the single word representing the severity level (Critical, High, Medium, Low) and nothing else."""

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=10,
                    temperature=0.0
                )
                
                result = response.choices[0].message.content.strip().title()
                # Normalize result
                for option in ["Critical", "High", "Medium", "Low"]:
                    if option in result:
                        return option
            except Exception as e:
                print(f"OpenAI severity analysis failed: {e}. Falling back to rule-based model.")

        # Rule-based fallback model
        desc_lower = description.lower()
        
        # Critical: Structural collapse, immediate safety hazards, exposed live wires, active major water flooding
        critical_keywords = ["critical", "hazard", "exposed wire", "shock", "fire hazard", "structural failure", "collapse", "severe structural", "load-bearing"]
        if any(kw in desc_lower for kw in critical_keywords):
            return "Critical"
            
        # High: Active water leaks, major roof defects, failing systems
        high_keywords = ["severe", "active leak", "water penetration", "blistering", "warped", "rot", "mold", "crack", "blockage"]
        if any(kw in desc_lower for kw in high_keywords):
            return "High"
            
        # Medium: Moderate weathering, sag, wear, but no active leakage or immediate safety risk
        medium_keywords = ["moderate", "sag", "rust", "corrosion", "damaged", "peeling", "cracked"]
        if any(kw in desc_lower for kw in medium_keywords):
            return "Medium"
            
        # Low: General maintenance, minor weathering, cosmetic issues
        return "Low"
