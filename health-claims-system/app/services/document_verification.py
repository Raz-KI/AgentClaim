

class DocumentVerificationService:
    def __init__(self,policy_repo):
        self.policy_repo = policy_repo
        
    def verify_documents(self,treatment_type, documents):
        required_documents = self.policy_repo.get_doc_req(treatment_type)
        print("Required Documents:", required_documents["required"])
        print("Uploaded Documents:", documents)
        missing_docs = set(required_documents["required"]) - set(documents)
        if missing_docs:
            return {
                "valid": False,
                "missing_documents": list(missing_docs),
                "message": "Required documents are missing"
            }
        else:
            return {
    "valid": True,
    "message": "All required documents uploaded"
}