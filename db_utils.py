from pymongo import MongoClient
from fuzzywuzzy import fuzz
import math

# Connect to in_data collection
client = MongoClient("mongodb+srv://ingredoai2:BXM6Hc1R57Hkiofy@cluster0.zimunh9.mongodb.net/")
db = client["test-ai"]
collection = db["in_data"]

def safe_lower(value):
    """Convert value to lowercase string safely."""
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    return str(value).lower()

def search_mongodb_ranked(ocr_terms, top_k=3):
    all_products = list(collection.find({}))
    scored = []

    for term in ocr_terms:
        for product in all_products:
            name = safe_lower(product.get("product_name_en"))
            brand = safe_lower(product.get("brands"))
            code = safe_lower(product.get("code"))

            # Exact barcode match
            if term.isdigit() and term == code:
                return product, f" Exact barcode match in MongoDB: {term}"

            # Fuzzy matching
            score_name = fuzz.partial_ratio(term, name) if name else 0
            score_brand = fuzz.partial_ratio(term, brand) if brand else 0
            score_code = fuzz.partial_ratio(term, code) if code else 0

            score = max(score_name, score_brand - 5, score_code - 10)

            if score > 0:
                scored.append((score, term, product))

    scored.sort(reverse=True, key=lambda x: x[0])
    top_matches = scored[:top_k]

    if top_matches and top_matches[0][0] >= 70:
        return top_matches[0][2], f"🔍 Fuzzy match in MongoDB with term '{top_matches[0][1]}' (score {top_matches[0][0]})"

    return None, None
