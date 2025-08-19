A Streamlit-based web application that scans product labels from images using OCR and retrieves detailed product information by querying a MongoDB database or the OpenFoodFacts (OFF) API.

Features

Upload Product Images: Supports JPG, JPEG, PNG formats.

OCR Text Extraction: Uses EasyOCR to read product labels.

Database Search: Finds product details in MongoDB.

Fallback API Search: Uses OpenFoodFacts API if product not found in MongoDB.

Multi-Language Support: Tries English first; automatically translates if needed.

Displays Key Information:

Product Name

Brand

Ingredients

Nutrition Facts

Product Categories

Tech Stack

Python 3.11+

Streamlit – Interactive web app framework

EasyOCR – Optical character recognition

MongoDB – Product database

OpenFoodFacts API – Public food product database

googletrans – Text translation

Installation & Setup
1. Clone the Repository
git clone https://github.com/your-username/ocr-product-scanner.git
cd ocr-product-scanner

2. Create & Activate Python Environment (Optional but Recommended)
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

3. Install Required Packages
pip install -r requirements.txt


requirements.txt contents:

streamlit
easyocr
pymongo
requests
googletrans==4.0.0-rc1

4. Configure MongoDB

Replace the MongoDB URI in db_utils.py with your own:

MONGO_URI = "your_mongodb_connection_string"
DB_NAME = "your_db_name"
COLLECTION_NAME = "your_collection_name"

5. Run the Application
streamlit run main.py


The app will open in your default browser at http://localhost:8501.

Upload a product image and view the extracted product details.

Screenshots

You can add a few screenshots here showing:

Uploading an image

OCR extracted text

Displayed product info

Notes

The app first attempts to find a match in MongoDB.

If MongoDB has no match, it uses the OpenFoodFacts API.

Ingredients and nutrition facts are cleaned and displayed in a readable format.

Multi-language support ensures non-English labels are translated automatically.
