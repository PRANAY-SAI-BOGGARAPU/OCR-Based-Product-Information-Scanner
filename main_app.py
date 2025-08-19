
import streamlit as st
from ocr_utils import extract_text_from_image
from db_utils import search_mongodb_ranked
from api_utils import search_openfoodfacts
from googletrans import Translator
import ast
import re

st.set_page_config(page_title="OCRTASK", layout="wide")
st.title("OCR-Based Product Information Scanner")

translator = Translator()


def get_in_english(product, en_key, fallback_key):
    """Return English text, translating if needed."""
    text = product.get(en_key) or product.get(fallback_key, "N/A")
    if not text or text == "N/A":
        return "N/A"
    try:
        detected = translator.detect(text).lang
        if detected != "en":
            return translator.translate(text, dest="en").text
    except Exception:
        return text
    return text

def clean_ingredients(ingredients_input):
 
    if not ingredients_input:
        return "N/A"
    if isinstance(ingredients_input, str):
        try:
            parsed = ast.literal_eval(ingredients_input)
            if isinstance(parsed, list):
                ingredients_input = parsed
            else:
                return ingredients_input
        except Exception:
            return ingredients_input
    if isinstance(ingredients_input, list):
        texts = [item.get("text", "") for item in ingredients_input if isinstance(item, dict) and item.get("text")]
        return ", ".join(texts) if texts else "N/A"
    return "N/A"

def clean_nutrition(nutrition_input):
   
    if not nutrition_input:
        return {}
    if isinstance(nutrition_input, dict):
        return {k: str(v) for k, v in nutrition_input.items()}
    if isinstance(nutrition_input, list):
        cleaned = {}
        for item in nutrition_input:
            if isinstance(item, dict):
                name = item.get("name", "Unknown")
                value = item.get("value", "")
                unit = item.get("unit", "")
                cleaned[name] = f"{value} {unit}".strip()
        return cleaned
    return {"raw": str(nutrition_input)}

def extract_ocr_terms(raw_text):
  
    if not raw_text:
        return []
    terms = [line.strip() for line in raw_text.splitlines() if line.strip()]
    digits = re.findall(r'\b\d{8,}\b', raw_text)
    return terms + digits


uploaded_file = st.file_uploader("Upload a product image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image_path = "temp_image.png"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.read())
    st.image(image_path, caption="Uploaded Image", width=250)


    with st.spinner("Extracting text from image..."):
        try:
            result = extract_text_from_image(image_path)
            if isinstance(result, tuple):
                ocr_terms, raw_text = result
            else:
                raw_text = result
                ocr_terms = extract_ocr_terms(raw_text)

            st.subheader("OCR Extracted Text")
            st.write(raw_text)
        except Exception as e:
            st.error(f"OCR failed: {e}")
            st.stop()

  
    product = None
    match_info = "No product found"

    with st.spinner("Searching product in MongoDB..."):
        try:
            if ocr_terms:
        
                product, match_info = search_mongodb_ranked(ocr_terms)
        except Exception as e:
            st.warning(f"MongoDB search failed: {e}")

  
    if not product and ocr_terms:
        with st.spinner("Searching product in OpenFoodFacts..."):
            for term in ocr_terms:
                try:
                    product, match_info = search_openfoodfacts(term)
                    if product:
                        break
                except Exception as e:
                    st.warning(f"OpenFoodFacts search failed for term '{term}': {e}")

  
    if product:
        st.subheader("Product Information")
        st.write("**Match Info:**", match_info)

        product_name = get_in_english(product, "product_name_en", "product_name")
        brand = get_in_english(product, "brands_en", "brands")
        ingredients = clean_ingredients(product.get("ingredients", []))
        categories = get_in_english(product, "categories_en", "categories")
        nutrition = clean_nutrition(product.get("nutriments", product.get("nutrition_facts")))

        st.write(f"**Product Name:** {product_name}")
        st.write(f"**Brand:** {brand}")
        st.write(f"**Ingredients:** {ingredients}")
        st.write(f"**Product Categories:** {categories}")

        st.write("**Nutrition Facts:**")
        if nutrition:
            for k, v in nutrition.items():
                st.write(f"- {k}: {v}")
        else:
            st.write("N/A")
    else:
        st.error("No product found")
