# Services are reusable business logic code
# It will mostly have normal python functions

import json
import uuid
from pathlib import Path
import shutil

from app.repositories.policy_repo import PolicyRepo
from app.services.document_verification import DocumentVerificationService

from app.schemas.claim import ClaimCreate
import os
import uuid
import logging
from typing import List
from fastapi import UploadFile

from app.schemas.claim import ClaimCreate, ClaimResponse
from app.schemas.claim import ExtractedDocument
from app.services.document_processing_service import DocumentProcessingService

class ClaimService:
    def __init__(self):
        self.policy_repo = PolicyRepo()
        self.document_verification_service = DocumentVerificationService(self.policy_repo)
        self.document_processing_service = DocumentProcessingService()

    def submit_claim(self, claim: ClaimCreate, docs):
        claim_id = self._generate_claim_id()

        verification = self.document_verification_service.verify_documents(claim.treatment_type, claim.docs_type)

        if verification["valid"] is False:
            return {
                "claim_id": claim_id,
                "status": "FAILED",
                "message": verification["message"],
                "missing_documents": verification["missing_documents"]
            }

        upload_folder = self._create_upload_folder(claim_id)
        saved_paths = self._save_uploaded_files(upload_folder, docs, claim.docs_type)
        self._save_claim_to_json(claim_id, claim)
        extractions: List[ExtractedDocument] = self.document_processing_service.process_documents(
            file_paths=saved_paths,
            docs_type=claim.docs_type
        )
        self._save_extracted_documents(claim_id, extractions)
        return {
            "claim_id": claim_id,
            "status": "SUBMITTED",
            "message": "Claim submitted successfully"
        }
    

    def _generate_claim_id(self):
        return str(uuid.uuid4())
    
    def _create_upload_folder(self,claim_id):
        folder = Path(f"app/claims_submitted/{claim_id}")
        folder.mkdir(parents=True, exist_ok=True)
        return folder
    
    def _save_uploaded_files(self, upload_folder, docs: list, docs_type: list):
        save_paths = []
        for file, docs_type in zip(docs, docs_type):
            extension = Path(file.filename).suffix
            new_filename = f"{docs_type}{extension}"

            file_path = upload_folder / new_filename

            with open(file_path, "wb") as destination:
                shutil.copyfileobj(file.file, destination)
            save_paths.append(file_path)

        return save_paths
    def _save_extracted_documents(self, claim_id, extractions: List[ExtractedDocument]):
        extracted_data = [extraction.model_dump() for extraction in extractions]
        json_file_path = Path(f"app/claims_submitted/{claim_id}/extracted_documents.json")

        with open(json_file_path, "w") as f:
            json.dump(extracted_data, f, indent=4)

    def _save_claim_to_json(self, claim_id, claim:ClaimCreate):
        claim_data = {
            "claim_id": claim_id,
            "member_id": claim.member_id,
            "claim_amount": claim.claim_amount,
            "treatment_type": claim.treatment_type
        }
                
        json_file_path = Path("app/claims_submitted/claims.json")

        # Read existing claims
        if json_file_path.exists() and json_file_path.stat().st_size > 0:

            
            with open(json_file_path, "r") as f:
                claims = json.load(f)
        else:
            claims = []

        # Add new claim
        claims.append(claim_data)

        # Save everything back
        with open(json_file_path, "w") as f:
            json.dump(claims, f, indent=4)