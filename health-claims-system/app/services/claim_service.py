# Services are reusable business logic code
# It will mostly have normal python functions

import json
import uuid
from pathlib import Path
import shutil

from app.schemas.claim import ClaimCreate

class ClaimService:
    def submit_claim(self, claim: ClaimCreate, docs):
        claim_id = self._generate_claim_id()
        upload_folder = self._create_upload_folder(claim_id)
        self._save_uploaded_files(upload_folder, docs)
        self._save_claim_to_json(claim_id, claim)
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
    
    def _save_uploaded_files(self,upload_folder, docs:list):
        for i in docs:
            file_path = Path(upload_folder) / i.filename
            with open(file_path, "wb") as f:
                shutil.copyfileobj(i.file, f)

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