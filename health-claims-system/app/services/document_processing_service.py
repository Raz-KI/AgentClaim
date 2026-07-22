import logging
from typing import List
from app.schemas.claim import ExtractedDocument
from app.services.gemini_extraction_service import GeminiDocumentExtractionService

logger = logging.getLogger("DocumentProcessingService")


class DocumentProcessingService:
    def __init__(self, extraction_service: GeminiDocumentExtractionService | None = None):
        self.extraction_service = extraction_service or GeminiDocumentExtractionService()

    def process_documents(self, file_paths: List[str], docs_type: List[str]) -> List[ExtractedDocument]:
        """
        Orchestrates document extraction by iterating saved disk paths and document types.
        """
        if len(file_paths) != len(docs_type):
            raise ValueError("Mismatched counts between saved files and provided document types.")

        extractions: List[ExtractedDocument] = []

        for file_path, doc_type in zip(file_paths, docs_type):
            logger.info(f"Processing saved file: {file_path} as {doc_type}")
            
            with open(file_path, "rb") as f:
                file_bytes = f.read()

            extraction = self.extraction_service.extract_from_bytes(
                image_bytes=file_bytes,
                document_type=doc_type
            )
            extractions.append(extraction)

        return extractions