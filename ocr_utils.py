import re
import easyocr


reader = easyocr.Reader(['en'])

def extract_text_from_image(image_path):
  
    results = reader.readtext(image_path, detail=0)
    cleaned_terms = []
    for text in results:
        words = re.findall(r"[A-Za-z0-9]+", text.lower())
        cleaned_terms.extend(words)


    cleaned_terms = [t for t in cleaned_terms if len(t) > 2]
    return cleaned_terms, results
