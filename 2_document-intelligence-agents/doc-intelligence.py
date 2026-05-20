# pip install pytesseract pdf2image Pillow
from pdf2image import convert_from_path
import pytesseract
from dataclasses import dataclass
from typing import List

CONFIDENCE_THRESHOLD = 80  # Minimum confidence percentage to consider text as valid

# This function converts PDF pages to images, performs OCR, and returns a list of tokens with their confidence scores.
# The OcrToken dataclass is used to store the text and its associated confidence score. Only tokens that meet the confidence threshold are included in the results.
@dataclass
class OcrToken: 
    text: str
    confidence: float   # 0.0 - 100.0


# Convert PDF pages to images and perform OCR, returning tokens with confidence scores.
def preprocess_and_ocr(pdf_path: str) -> List[OcrToken]:

    # Convert PDF to high-res images for better OCR accuracy
    # Higher DPI can improve OCR results but may increase processing time and memory usage. Adjust as needed based on your documents and system capabilities.
    images = convert_from_path(pdf_path, dpi=300)  
    tokens: List[OcrToken] = []

    for image in images:

        # Perform OCR on the image
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        
        # Extract text and confidence
        for i, word in enumerate(data["text"]):
            conf = int(data["conf"][i])
            if word.strip() and conf >= CONFIDENCE_THRESHOLD:
                tokens.append(OcrToken(text=word, confidence=conf))

    return tokens

if __name__ == "__main__":
    tokens = preprocess_and_ocr("./docs/sql-ddl.pdf")
    for token in tokens:
        print(f"{token.text} ({token.confidence:.1f}%)")