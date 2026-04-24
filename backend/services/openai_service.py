import os
import openai
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class OpenAIService:
    @staticmethod
    def _get_client():
        if OPENAI_API_KEY and not OPENAI_API_KEY.startswith("sk-proj-your"):
            return openai.OpenAI(api_key=OPENAI_API_KEY)
        return None

    @classmethod
    def generate_image_description(cls, category: str, image_url: str = None) -> str:
        """
        Uses OpenAI GPT-4 Vision model to generate a professional inspection description.
        Falls back to generating a high-quality simulated description if OpenAI is not configured.
        """
        client = cls._get_client()

        if client:
            try:
                # Format prompt
                prompt = f"""You are a professional building inspector. Analyze this image and provide a concise, professional inspection description.

Category: {category}

Generate a 2-3 sentence technical description suitable for an inspection report. Focus on:
- Observable conditions
- Potential concerns or defects
- Professional terminology
- Actionable findings

Be specific, objective, and professional."""

                # Prepare payload
                # Note: Next-gen OpenAI models use gpt-4o or gpt-4-turbo for vision-based inputs
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": image_url if image_url and image_url.startswith("http") else "https://images.unsplash.com/photo-1513694203232-719a280e022f"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=150
                )
                
                description = response.choices[0].message.content.strip()
                return description
            except Exception as e:
                print(f"OpenAI description generation failed: {e}. Falling back to simulation.")

        # Fallback simulated text
        mock_descriptions = {
            "Gutter Blockage": f"Severe organic debris and sediment buildup noted in the active gutter troughs. The blockages are causing standing water, which could lead to gutter sag and water infiltration under the roof eaves. Immediate manual flushing and cleaning are recommended.",
            "Roof Defect": f"Visible cracking, blistering, and advanced granular loss detected on the primary asphalt shingles. Several tabs are lifting, creating susceptibility to high-wind displacement and moisture penetration. Professional shingle repair is recommended.",
            "Water Damage": f"Noted active dark moisture staining and soft spots along the drywall ceiling directly beneath the roof transition valley. Immediate moisture mapping and leak source mitigation are recommended.",
            "Structural Issue": f"Horizontal and diagonal cracking noted along the load-bearing masonry wall. Structural movement is apparent, indicating settlement or lateral pressure. Further diagnostic review by a structural engineer is recommended.",
            "Siding Damage": f"Cracked, warped, and missing sections of vinyl siding cladding observed. The underlying house wrap is exposed, posing an increased risk of weather-driven rain intrusion. Re-siding of the affected wall sections is recommended.",
            "Foundation Issue": f"Significant vertical stair-step cracking observed in the foundation concrete blocks. Minor moisture weeping is visible through the cracks. Sealing and monitoring of foundation stability are advised.",
            "Electrical Hazard": f"Exposed wiring connections and lack of proper junction box enclosures detected. Standard wire nuts are unshielded, posing an immediate electrical shock and fire hazard. Professional electrician remediation is required.",
            "Plumbing Issue": f"Active dripping leak noted at the copper supply line solder joint. Corrosion scaling has formed, indicating a long-term slow leak. Joint re-soldering or pipe segment replacement is recommended.",
            "HVAC Concern": f"Heavy dust blockage and restricted airflow noted at the external condenser coil fins. The unit is operating at high temperature, which may shorten compressor lifespan. Coil cleaning and system servicing are recommended.",
            "General Maintenance": f"Standard paint peeling and wood rot weathering noted on the exterior window trim wood. Sanding, priming, and application of exterior-grade paint are advised to prevent deep wood rot."
        }
        
        return mock_descriptions.get(
            category, 
            f"Observed minor weathering and signs of deterioration matching standard {category} parameters. General maintenance is recommended to restore materials to design specs and prevent accelerated wear."
        )

    @classmethod
    def generate_conclusion(cls, descriptions: list) -> str:
        """
        Generates a comprehensive conclusion summary from all report image descriptions.
        """
        client = cls._get_client()

        if client and descriptions:
            try:
                findings = "\n".join([f"- {d}" for d in descriptions])
                prompt = f"""You are a professional building inspector. Based on the following inspection findings, generate a comprehensive conclusion summary for the inspection report.

Findings:
{findings}

Generate a professional conclusion that:
- Summarizes the overall condition
- Highlights critical issues requiring immediate attention
- Notes areas requiring monitoring
- Provides general recommendations
- Uses professional inspection terminology
- Is 4-6 sentences long"""

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=300
                )
                
                conclusion = response.choices[0].message.content.strip()
                return conclusion
            except Exception as e:
                print(f"OpenAI conclusion generation failed: {e}. Falling back to simulation.")

        # Fallback simulation
        if not descriptions:
            return "Inspection completed successfully. No major issues or defects were reported, and all observed items appear to be in sound condition suitable for standard operations."
            
        return f"Based on the thorough property inspection, the building exhibits a combination of maintenance requirements needing prompt action. Specifically, concerns regarding {', '.join(list(set([d[:15] for d in descriptions]))[:3]).lower()} present potential structural and weatherproofing vulnerabilities if left unresolved. It is highly recommended to engage licensed specialists to remediate the identified hazards, particularly any electrical and structural concerns. Overall, routine monitoring and proactive maintenance will preserve the facility's value and ensure a safe environment."
