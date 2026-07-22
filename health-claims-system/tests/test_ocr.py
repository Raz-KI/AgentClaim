import os
import cv2
import numpy as np
import fitz  # PyMuPDF
import easyocr
from pydantic import BaseModel

class OCRResult(BaseModel):
    text: str
    confidence: float


class OCRService:

    def __init__(self):
        # Initialize EasyOCR (Note: if you have a GPU, set gpu=True for 10x speed)
        self.reader = easyocr.Reader(['en'], gpu=False)

    def _preprocess_and_crop(self, file_path: str) -> str:
        """
        Detects if there's a heavy dark background border, crops to the actual document 
        contour, and saves over the temp/original image to ensure EasyOCR gets a clean image.
        """
        img = cv2.imread(file_path)
        if img is None:
            return file_path

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Threshold to separate the white page from a dark background border
        _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
        
        # Find contours of the white document
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Find the largest continuous block (the page)
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Only crop if the detected document area is reasonable (e.g. at least 20% of the image)
            if cv2.contourArea(largest_contour) > (img.shape[0] * img.shape[1] * 0.2):
                x, y, w, h = cv2.boundingRect(largest_contour)
                
                # Crop with a slight safety padding (15px) so we don't clip text near edge
                pad = 15
                y1 = max(0, y - pad)
                y2 = min(img.shape[0], y + h + pad)
                x1 = max(0, x - pad)
                x2 = min(img.shape[1], x + w + pad)
                
                cropped = img[y1:y2, x1:x2]
                cv2.imwrite(file_path, cropped)
                
        return file_path

    def process_document(self, file_path: str):
        extension = file_path.lower().split(".")[-1]

        if extension == "pdf":
            return self._process_pdf(file_path)
        else:
            # Preprocess stand-alone images BEFORE OCR processing
            processed_path = self._preprocess_and_crop(file_path)
            return self._process_image(processed_path)

    def _process_image(self, file_path: str):
        # Run EasyOCR
        results = self.reader.readtext(file_path)

        text_lines = []
        confidence_scores = []

        for _, detected_text, confidence in results:
            if detected_text.strip():
                text_lines.append(detected_text)
                confidence_scores.append(confidence)

        # Structure text with proper line breaks instead of a single massive line
        text = "\n".join(text_lines)

        avg_confidence = (
            sum(confidence_scores) / len(confidence_scores)
            if confidence_scores
            else 0.0
        )

        return OCRResult(
            text=text,
            confidence=avg_confidence
        )

    def _process_pdf(self, file_path: str):
        doc = fitz.open(file_path)
        full_text = ""
        confidences = []

        for page_num, page in enumerate(doc):
            text = page.get_text()

            # If it's a digital PDF with searchable text
            if text.strip():
                full_text += text + "\n"
                confidences.append(1.0)
            else:
                # Scanned PDF page: Convert page to high-res image
                zoom = 3.0  # Boost resolution to 300 DPI
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)
                
                temp_image_path = f"temp_page_{page_num}.png"
                pix.save(temp_image_path)

                # Preprocess this newly rendered page to crop out scanner margins/borders
                processed_img_path = self._preprocess_and_crop(temp_image_path)

                # Extract Text via OCR
                result = self._process_image(processed_img_path)
                full_text += result.text + "\n"
                confidences.append(result.confidence)

                # Clean up the temp image
                if os.path.exists(temp_image_path):
                    os.remove(temp_image_path)

        avg_confidence = (
            sum(confidences) / len(confidences)
            if confidences
            else 0.0
        )

        return OCRResult(
            text=full_text,
            confidence=avg_confidence
        )


# --- RUNNING THE TEST ---
if __name__ == "__main__":
    ocr = OCRService()

    # If 'bill.jpg' is in your directory, it will automatically crop the black background, 
    # run EasyOCR on the clean white page, and output accurate text.
    result = ocr.process_document("bill.jpg")

    print("--- OCR RESULT ---")
    print(f"Confidence: {result.confidence:.4f}")
    print("\nExtracted Text:\n")
    print(result.text)