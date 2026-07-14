

import easyocr
import fitz
from PIL import Image
import os

from pydantic import BaseModel

class OCRResult(BaseModel):
    text: str
    confidence: float


class OCRService:

    def __init__(self):
        self.reader = easyocr.Reader(
            ['en'],
            gpu=False
        )


    def process_document(self, file_path:str):

        extension = file_path.lower().split(".")[-1]


        if extension == "pdf":
            return self._process_pdf(file_path)

        else:
            return self._process_image(file_path)



    def _process_image(self,file_path):

        results = self.reader.readtext(file_path)


        text = ""
        confidence_scores=[]


        for _, detected_text, confidence in results:

            text += detected_text + " "

            confidence_scores.append(confidence)


        avg_confidence = (
            sum(confidence_scores)
            /
            len(confidence_scores)
            if confidence_scores
            else 0
        )


        return OCRResult(
            text=text,
            confidence=avg_confidence
        )



    def _process_pdf(self,file_path):

        doc = fitz.open(file_path)

        full_text=""
        confidences=[]


        for page in doc:


            # Try extracting normal PDF text
            text = page.get_text()


            if text.strip():

                full_text += text


                confidences.append(1.0)


            else:

                # scanned pdf

                pix = page.get_pixmap()

                image_path="temp_page.png"

                pix.save(image_path)


                result=self._process_image(
                    image_path
                )


                full_text += result.text

                confidences.append(
                    result.confidence
                )


                os.remove(image_path)



        avg_confidence=(
            sum(confidences)
            /
            len(confidences)
            if confidences
            else 0
        )


        return OCRResult(
            text=full_text,
            confidence=avg_confidence
        )
ocr = OCRService()


result = ocr.process_document(
    "bill.jpg"
)


print(result)
print(result.text)
print(result.confidence)