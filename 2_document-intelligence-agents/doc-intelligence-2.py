# Quick Implementation
# Example: Document Intelligence Agent (layout-aware key-value extraction)

# pip install pillow pytesseract pdf2image rapidfuzz
# System requirement: Tesseract OCR and Poppler must be installed on your system for the above libraries to work correctly (https://tesseract-ocr.github.io/tessdoc/Installation.html 
# and https://poppler.freedesktop.org/).

import os
from dataclasses import dataclass
from typing import List, Dict, Tuple
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
from rapidfuzz import fuzz, process

# 1) Minimial Schema Definition
# Each field has a set of cue keywords that typically appear near the value in an invoice like document. 

SCHEMA = {
    "invoice_number": ["invoice number", "inv no", "invoice #", "bill number"],
    "invoice_date": ["invoice date", "date of issue", "billing date"],
    "total_amount": ["total amount", "amount due", "total due", "balance due"],
}

@dataclass
class Token:
    text: str
    x: int
    y: int
    w: int
    h: int
    conf: float
    line_id: int

def ocr_tokens(image: Image.Image) -> List[Token]:
    # Perform OCR and return tokens with their bounding boxes and a simple line grouping
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    tokens= []

    for i in range(len(data["text"])):
        text = data["text"][i].strip()
        if not text: 
            continue
        x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
        conf = float(data["conf"][i]) if data["conf"][i] != '-1' else 0.0  # When Tesseract has no confidence value for a token, it returns the string '-1'

        # Build a simple line id from Tessaract block/para/line indices
        line_id = (
            data["block_num"][i],
            data["par_num"][i],
            data["line_num"][i]
        )
        tokens.append(
            Token(
                text=text,
                x=x,
                y=y,
                w=w,
                h=h,
                conf=conf,
                line_id=hash(line_id),
            )
        )
    return tokens

def join_line(tokens: List[Token]) -> Dict[int, List[Token]]:
    # Group tokens by line using the line_id hash and sort left to right 
    lines: Dict[int, List[Token]] = {}
    for t in tokens:
        lines.setdefault(t.line_id, []).append(t)
    for lid in lines:
        lines[lid] = sorted(lines[lid], key=lambda t: t.x)
    return lines

def normalize(s: str) -> str:
    return "".join(ch.lower() for ch in s if ch.isalnum() or ch.isspace())

def best_keyword_match(text: str, candidates: List[str], cutoff=80) -> Tuple[str, int]:
    # Use fuzzy matching to find the best matching keyword from the schema cues
    choices = [(kw, normalize(kw)) for kw in candidates]
    best = ("", 0)
    for orig, norm_kw in choices: 
        score = fuzz.partial_ratio(normalize(text), norm_kw)
        if score > best[1]: 
            best = (orig, score)
    return best if best[1] >= cutoff else ("", 0)

def extract_near_keyword(lines: Dict[int, List[Token]], keywords: List[str]) -> str:
    """
        Strategy: 
        1) Find a line that contains or closely matches a keyword from the schema cues using fuzzy matching.
        2) Return the text to the right of that keyword on the same line, else fall back to the next line below in the same column region
    """

    # pass1: same line, value to the right 
    for lid, toks in lines.items(): 
        line_text = " ".join(t.text for t in toks)
        kw, score = best_keyword_match(line_text, keywords)
      
        if not kw: 
            continue
        # find token index where keyword occurs (rough approach)
        idx = process.extractOne(kw, [t.text for t in toks], scorer=fuzz.partial_ratio)
        
        if idx is None:
            continue

        start_i = idx[2]
        value = " ".join(t.text for t in toks[start_i+1:]).strip(": ").strip()  # Take text to the right of the keyword

        if value:
            return value
        
        # pass2: look at the line below within same horizontal band
        sorted_lines = sorted(lines.items(), key=lambda kv: min(t.y for t in kv[1]))  # Sort lines by their vertical position
        for i, (lid, toks) in enumerate(sorted_lines[:-1]): 
            line_text = " ".join(t.text for t in toks)
            kw, score = best_keyword_match(line_text, keywords)
            if not kw:
                continue
            # find token index where keyword occurs (rough approach)
            idx = process.extractOne(kw, [t.text for t in toks], scorer=fuzz.partial_ratio)

            if idx is None:
                continue

            # candidate next line
            _, next_toks = sorted_lines[i+1]
            value = " ".join(t.text for t in next_toks).strip(": ").strip()

            if value: 
                return value
    
    return " "  # Return empty string if no value found

def extract_fields_from_image(image: Image.Image) -> Dict[str, str]:
    tokens = ocr_tokens(image)
    lines = join_line(tokens)

    results = {}

    for field, cues in SCHEMA.items():
        results[field] = extract_near_keyword(lines, cues)
    return results

def extract_from_pdf(pdf_path: str, dpi=300) -> Dict[str, str]:
    pages = convert_from_path(pdf_path, dpi=dpi, fmt="png")
    
    # Simple strategy: attempt extraction page by page merge non-empty fields)
    final = {k: "" for k in SCHEMA}
    for page in pages:
        fields = extract_fields_from_image(page)
        for k, v in fields.items():
            if v and not final[k]:  # Update only if we don't have a value yet
                final[k] = v
    return final

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python doc-intelligence-2.py <path-to-image-or-pdf>")
        sys.exit(1)

    path = sys.argv[1]

    if path.lower().endswith(".pdf"):
        results = extract_from_pdf(path)
    else:
        image = Image.open(path)
        results = extract_fields_from_image(image)

    print("Extracted fields: ")
    for k, v in results.items():
        print(f" {k}: {v}")