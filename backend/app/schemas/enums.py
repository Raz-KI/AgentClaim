from enum import Enum


class ClaimType(str, Enum):
    OPD = "OPD"
    PHARMACY = "PHARMACY"
    HOSPITALIZATION = "HOSPITALIZATION"


class ClaimDecisionType(str, Enum):
    APPROVED = "APPROVED"
    PARTIAL = "PARTIAL"
    REJECTED = "REJECTED"
    MANUAL_REVIEW = "MANUAL_REVIEW"


class DocumentType(str, Enum):
    PRESCRIPTION = "PRESCRIPTION"
    HOSPITAL_BILL = "HOSPITAL_BILL"
    LAB_REPORT = "LAB_REPORT"
    PHARMACY_BILL = "PHARMACY_BILL"
    UNKNOWN = "UNKNOWN"