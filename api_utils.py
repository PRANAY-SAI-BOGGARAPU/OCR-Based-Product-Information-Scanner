import requests

def search_openfoodfacts(ocr_terms):

    for term in ocr_terms:

        if term.isdigit():
            url = f"https://world.openfoodfacts.org/api/v0/product/{term}.json"
            resp = requests.get(url)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == 1:
                    return data["product"], f" Found product in OpenFoodFacts by barcode: {term}"

        # Text search
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={term}&search_simple=1&action=process&json=1&page_size=3"
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("products"):
                for prod in data["products"]:
                    if prod.get("product_name"):
                        return prod, f" Found product in OpenFoodFacts using '{term}'"
    return None, None
