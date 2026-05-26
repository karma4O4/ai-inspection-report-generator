import os
import openai
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class CostEstimationService:
    @staticmethod
    def _get_client():
        if OPENAI_API_KEY and not OPENAI_API_KEY.startswith("sk-proj-your"):
            return openai.OpenAI(api_key=OPENAI_API_KEY)
        return None

    @classmethod
    def estimate_repair_cost(cls, category: str, severity: str) -> str:
        """
        Uses OpenAI GPT-4o to generate a rough repair cost estimate based on the defect category and severity.
        Falls back to a standard lookup matrix if OpenAI is not configured or fails.
        """
        client = cls._get_client()
        if client:
            try:
                prompt = f"""You are a professional building estimator and contractor.
Generate a rough, realistic repair cost estimate range (in USD) for the following defect:

Category: {category}
Severity Level: {severity}

Provide a concise response containing ONLY the cost range (e.g., "$500 - $1,200" or "$3,000 - $5,000") and a 5-word explanation (e.g., "$3,000 - $5,000 (requires full replacement)"). Do not write long paragraphs."""

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=30,
                    temperature=0.3
                )
                
                estimate = response.choices[0].message.content.strip()
                if estimate:
                    return estimate
            except Exception as e:
                print(f"OpenAI cost estimation failed: {e}. Falling back to matrix.")

        # Fallback matrix based on Category and Severity
        matrix = {
            "Gutter Blockage": {
                "Critical": "$300 - $600 (repair gutter sagging)",
                "High": "$200 - $400 (heavy professional flush)",
                "Medium": "$150 - $250 (standard gutter cleaning)",
                "Low": "$100 - $150 (minor debris removal)"
            },
            "Roof Defect": {
                "Critical": "$5,000 - $12,000 (complete roof replacement)",
                "High": "$1,500 - $3,500 (major shingle / valley repair)",
                "Medium": "$500 - $1,200 (minor shingle replacement)",
                "Low": "$200 - $500 (patch minor leak/sealant)"
            },
            "Water Damage": {
                "Critical": "$4,000 - $10,000 (mold remediation & drywall)",
                "High": "$1,500 - $4,000 (ceiling drywall & painting)",
                "Medium": "$600 - $1,500 (patch plaster & dry out)",
                "Low": "$200 - $600 (stain sealer & painting)"
            },
            "Structural Issue": {
                "Critical": "$10,000 - $25,000 (foundation underpinning)",
                "High": "$4,000 - $10,000 (structural wall reinforcement)",
                "Medium": "$1,500 - $4,000 (lintel/masonry stabilization)",
                "Low": "$500 - $1,500 (minor crack epoxy injection)"
            },
            "Siding Damage": {
                "Critical": "$3,000 - $7,000 (full wall siding replacement)",
                "High": "$1,200 - $3,000 (partial siding panel swap)",
                "Medium": "$500 - $1,200 (minor siding patch)",
                "Low": "$150 - $500 (re-secure loose panels)"
            },
            "Foundation Issue": {
                "Critical": "$8,000 - $20,000 (foundation stabilization)",
                "High": "$3,000 - $8,000 (major crack underpinning)",
                "Medium": "$1,000 - $3,000 (epoxy injection & sealing)",
                "Low": "$300 - $1,000 (minor surface crack patch)"
            },
            "Electrical Hazard": {
                "Critical": "$2,000 - $5,000 (full electrical panel upgrade)",
                "High": "$800 - $2,000 (rewire hazard circuits)",
                "Medium": "$300 - $800 (install subpanels/outlets)",
                "Low": "$150 - $300 (replace broken switches/nuts)"
            },
            "Plumbing Issue": {
                "Critical": "$3,000 - $8,000 (main sewer line replacement)",
                "High": "$1,000 - $3,000 (re-pipe damaged area)",
                "Medium": "$400 - $1,000 (repair copper pipe leaks)",
                "Low": "$150 - $400 (replace standard fixtures/valves)"
            },
            "HVAC Concern": {
                "Critical": "$4,000 - $9,000 (full HVAC system replacement)",
                "High": "$1,500 - $3,500 (compressor/evaporator repair)",
                "Medium": "$500 - $1,500 (duct repair or fan replacement)",
                "Low": "$150 - $500 (coil cleaning & system tuneup)"
            },
            "General Maintenance": {
                "Critical": "$1,000 - $3,000 (major carpentry repairs)",
                "High": "$500 - $1,500 (trim replacement & paint)",
                "Medium": "$250 - $600 (touch-up paint & caulk)",
                "Low": "$100 - $250 (basic cleanup & minor fix)"
            }
        }

        # Resolve values from matrix
        cat_estimates = matrix.get(category, matrix["General Maintenance"])
        return cat_estimates.get(severity, cat_estimates.get("Medium"))
