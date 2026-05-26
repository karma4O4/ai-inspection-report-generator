import os
import openai
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class WhisperService:
    @staticmethod
    def _get_client():
        if OPENAI_API_KEY and not OPENAI_API_KEY.startswith("sk-proj-your"):
            return openai.OpenAI(api_key=OPENAI_API_KEY)
        return None

    @classmethod
    def transcribe_audio(cls, file_bytes: bytes, filename: str) -> str:
        """
        Transcribes the given audio bytes using OpenAI Whisper API.
        Falls back to a simulated transcript if OpenAI is not configured or fails.
        """
        client = cls._get_client()
        if client:
            try:
                # Call Whisper API
                # Pass file-like object using tuple: (filename, bytes)
                transcript_response = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=(filename, file_bytes),
                    response_format="text"
                )
                if isinstance(transcript_response, str):
                    return transcript_response.strip()
                return transcript_response.text.strip()
            except Exception as e:
                print(f"OpenAI Whisper transcription failed: {e}. Falling back to simulation.")

        # Simulation fallback based on the filename/request
        return "Simulated voice note: Inspector observed minor hair-line cracks along the lower foundation wall and recommended structural injection sealing."
