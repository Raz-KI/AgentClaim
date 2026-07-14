import json

class PolicyRepo:
    def __init__(self,file_path="app/policies/policy.json"):
        self.file_path = file_path
        self.policy = self._load_policy()

    def _load_policy(self):
        try:
            with open(self.file_path, 'r') as file:
                policies = json.load(file)
                return policies
        except FileNotFoundError:
            print("File not found")
    
    def get_doc_req(self, treatment_type):
        if self.policy:
            docs_required = self.policy[treatment_type]
            return docs_required