import logging
import os
from typing import Optional
import cv2
import numpy as np
from tenacity import retry, stop_after_attempt, wait_random_exponential
from google import genai
from google.genai import types

from app.schemas.claim import ExtractedDocument

logger = logging.getLogger("GeminiVisionExtraction")


class Preprocessor:
    @staticmethod
    def optimize_for_vlm(image_bytes: bytes, max_dim: int = 2048) -> bytes:
        """
        Resizes images exceeding maximum dimensions while retaining full RGB color.
        """
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Invalid image file or unreadable byte stream.")

        h, w = img.shape[:2]
        if max(h, w) > max_dim:
            scale = max_dim / float(max(h, w))
            img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

        _, buffer = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        return buffer.tobytes()


class GeminiDocumentExtractionService:
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.5-flash"):
        # key = api_key or os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6JZN7vNZI3FLtU5id9NFsEt_0ymX3Q0kvaUz1J6hlOCHA")
        # if not key:
        #     raise ValueError("GEMINI_API_KEY must be provided or set in environment variables.")
        
        # self.client = genai.Client(api_key=key)
        self.model_name = model_name
        self.client = genai.Client(enterprise=True, project="agentclaims-1234", location="us-central1"
)
        self.model_name = model_name

    @retry(
        wait=wait_random_exponential(min=1, max=10),
        stop=stop_after_attempt(3),
        reraise=True
    )
    def extract_from_bytes(self, image_bytes: bytes, document_type: str) -> ExtractedDocument:
        """
        Extracts structured data from image bytes dynamically using the specified document type.
        """
        logger.info(f"Executing Gemini VLM Extraction for document_type: {document_type}")

        # Preprocess image
        clean_bytes = Preprocessor.optimize_for_vlm(image_bytes)

        system_instruction = (
            "You are an AI document extraction engine for a health insurance claims processing system.\n"
            "Your task is to analyze a medical document and extract structured information with maximum accuracy.\n"
            "Requirements:\n"
            "- Read every visible field from the document.\n"
            "- Preserve numeric values exactly.\n"
            "- Do not invent or infer missing information.\n"
            "- If a value is unreadable or absent, set value to null.\n"
            "- Return confidence scores for extracted fields.\n"
            "- Preserve dates exactly as written; normalize to YYYY-MM-DD where possible.\n"
            "- Summarize the document in one concise sentence.\n"
            "- Return ONLY valid JSON matching the requested schema."
        )

        # Dynamic prompt using runtime document_type
        prompt = (
            f"Document Type: {document_type.upper()}\n"
            "Extract all relevant information required for insurance claim processing.\n"
            "Important fields to extract if present:\n"
            "- patient_name, hospital_name, doctor_name, invoice_number\n"
            "- bill_date, admission_date, discharge_date, diagnosis\n"
            "- procedures, medicines, total_amount, taxes, payment_status\n\n"
            "Extract any additional relevant fields present on the document.\n"
            "Return JSON matching the schema."
        )

        image_part = types.Part.from_bytes(
            data=clean_bytes,
            mime_type="image/jpeg"
        )

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.0,
            response_mime_type="application/json",
            response_schema=ExtractedDocument,
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[image_part, prompt],
            config=config,
        )
        # print("Gemini VLM response:", response.text)
        return ExtractedDocument.model_validate_json(response.text)