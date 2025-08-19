A Streamlit-based application that uses Optical Character Recognition (OCR) to scan product labels from images and retrieve product details by matching them with a MongoDB database or the OpenFoodFacts (OFF) API.

Features

Upload a product image (JPG, JPEG, PNG)

Extract text from product label using EasyOCR

Search product information in MongoDB

Fallback to OpenFoodFacts API if MongoDB doesn’t contain the product

Multi-language support → Tries English first, auto-translates if needed, else shows original language

Displays:

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

googletrans – Text translation (with fallback)

Requirements :

streamlit
easyocr
pymongo
requests
googletrans==4.0.0-rc1
