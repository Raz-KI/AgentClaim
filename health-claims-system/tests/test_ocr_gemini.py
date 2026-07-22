import io
import logging
import os
from typing import List, Optional
import cv2
import numpy as np
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_random_exponential

from google import genai
from google.genai import types

# Load API key safely from environment variable (or hardcode for quick local testing)
GEMINI_API_KEY = "AQ.Ab8RN6JZN7vNZI3FLtU5id9NFsEt_0ymX3Q0kvaUz1J6hlOCHA"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Gemini-OCR-Pipeline")


# ==========================================
# 1. STRUCTURED SCHEMAS
# ==========================================
class ExtractedField(BaseModel):
    value: str | int | float | list | None
    confidence: float


class DocumentExtraction(BaseModel):
    document_type: str
    summary: str

    fields: dict[str, ExtractedField]

    missing_fields: list[str]

    confidence: float

    extraction_notes: str | None = None


# ==========================================
# 2. VLM-OPTIMIZED PREPROCESSOR (RGB-Safe)
# ==========================================
class Preprocessor:
    @staticmethod
    def optimize_for_vlm(image_bytes: bytes, max_dim: int = 2048) -> bytes:
        """
        Optimizes resolution while maintaining original RGB colors
        to preserve visual signals for the VLM attention mechanism.
        """
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Invalid image file or unreadable byte stream.")

        # Downscale ONLY if resolution exceeds token limits
        h, w = img.shape[:2]
        if max(h, w) > max_dim:
            scale = max_dim / float(max(h, w))
            img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

        # Re-encode clean RGB image as JPEG
        _, buffer = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        return buffer.tobytes()


# ==========================================
# 3. OCR SERVICE
# ==========================================
class GeminiOCRService:
    def __init__(self, api_key: str, model_name: str = "gemini-3.1-flash-lite"):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    @retry(
        wait=wait_random_exponential(min=1, max=10),
        stop=stop_after_attempt(3),
        reraise=True
    )
    def process_image(self, image_bytes: bytes) -> DocumentExtraction:
        logger.info("Executing Gemini VLM request...")

        system_instruction = ('''
            You are an AI document extraction engine for a health insurance claims processing system.

            Your task is to analyze a medical document and extract structured information with maximum accuracy.

            Requirements:

            - Read every visible field from the document.
            - Preserve numeric values exactly.
            - Do not invent or infer missing information.
            - If a value is unreadable or absent, return null.
            - Return confidence scores for extracted fields.
            - Preserve dates exactly as written; if possible normalize to YYYY-MM-DD.
            - Ignore logos, decorative graphics, and watermarks unless they contain useful information.
            - Summarize the document in one sentence.
            - Return ONLY valid JSON that matches the provided schema.'''
        )

        prompt = '''Document Type:
        HOSPITAL_BILL

        Extract all relevant information required for insurance claim processing.

        Examples of important fields include:

        - patient name
        - hospital name
        - doctor name
        - invoice number
        - bill date
        - admission date
        - discharge date
        - diagnosis
        - procedures
        - medicines
        - total amount
        - taxes
        - payment status

        Extract any additional useful fields you find.

        Return only JSON following the provided schema.'''

        # Pass raw image bytes directly via GenAI Part object
        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type="image/jpeg"
        )

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.0,  # Fully deterministic outputs
            response_mime_type="application/json", # What type of output we expect
            response_schema=DocumentExtraction,     # how we want the output structured
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[image_part, prompt],
            config=config,
        )

        # Parse and validate with Pydantic
        return DocumentExtraction.model_validate_json(response.text)


# ==========================================
# 4. RUNNER
# ==========================================
if __name__ == "__main__":
    image_path = "invoice.png"

    try:
        with open(image_path, "rb") as f:
            raw_bytes = f.read()

        logger.info("Preprocessing image for VLM...")
        clean_bytes = Preprocessor.optimize_for_vlm(raw_bytes)

        logger.info("Initializing OCR Service...")
        ocr_engine = GeminiOCRService(api_key=GEMINI_API_KEY, model_name="gemini-3.1-flash-lite")
        
        result: DocumentExtraction = ocr_engine.process_image(clean_bytes)

        print("\n--- OCR EXTRACTION COMPLETE ---")
        print(f"Vendor: {result.vendor_name}")
        print(f"Total:  {result.currency} {result.total_amount}")
        print("\nValidated Output:")
        print(result.model_dump_json(indent=2))

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")