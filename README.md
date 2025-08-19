# OCR-Based Product Information Scanner

A **Streamlit-based web application** that scans product labels from images using OCR and retrieves detailed product information by querying a **MongoDB database** or the **OpenFoodFacts (OFF) API**.

---

## 🚀 Features
- **Upload Product Images**: Supports JPG, JPEG, PNG formats.  
- **OCR Text Extraction**: Uses EasyOCR to read product labels.  
- **Database Search**: Finds product details in MongoDB.  
- **Fallback API Search**: Uses OpenFoodFacts API if product not found in MongoDB.  
- **Multi-Language Support**: Tries English first; automatically translates if needed.  
- **Displays Key Information**:
  - Product Name  
  - Brand  
  - Ingredients  
  - Nutrition Facts  
  - Product Categories  

---

## 🛠️ Tech Stack
- **Python 3.11+**  
- **Streamlit** – Interactive web app framework  
- **EasyOCR** – Optical character recognition  
- **MongoDB** – Product database  
- **OpenFoodFacts API** – Public food product database  
- **googletrans** – Text translation  

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ocr-product-scanner.git
cd ocr-product-scanner
