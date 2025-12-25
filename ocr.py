import os
import fitz  # PyMuPDF
import cv2   # OpenCV pour le traitement d'image
import pytesseract
import numpy as np
import json
import re


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(pixmap):
    """
    Étape 1 & 2 : Prétraitement et Nettoyage de l'image.
    Convertit l'image PyMuPDF en format OpenCV, met en gris et binarise.
    """
    # Conversion PyMuPDF (pixmap) -> Image numpy (OpenCV)
    img_array = np.frombuffer(pixmap.samples, dtype=np.uint8).reshape(pixmap.h, pixmap.w, pixmap.n)
    
    # Si l'image a 4 canaux (Alpha), on garde que RGB
    if pixmap.n == 4:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
    
    # Conversion en niveaux de gris
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    # Binarisation (Noir et Blanc pur) pour aider l'OCR
    # Cela sépare le texte du fond
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return binary

def extract_semantic_data(text):
    """
    Étape 4 : Extraction sémantique (Version Améliorée).
    """
    data = {
        "dates": [],
        "emails": [],
        "montants": [],
        "raw_text": text.strip()
    }

    # Dates (inchangé)
    date_pattern = r'\b\d{2}[/-]\d{2}[/-]\d{4}\b'
    data["dates"] = re.findall(date_pattern, text)

    # Emails (inchangé)
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    data["emails"] = re.findall(email_pattern, text)


    price_pattern = r'\b\d+[.,]\d{2}(?:\s?(?:€|\$|EUR|USD|-))?\b'
    
    found_prices = re.findall(price_pattern, text)
    # On nettoie les résultats pour enlever le tiret '-' à la fin s'il y en a un
    data["montants"] = [p.replace('-', '€').strip() for p in found_prices]

    return data

def process_document(file_path, output_format="json"):
    """
    Orchestre tout le processus OCR.
    """
    filename = os.path.basename(file_path)
    print(f"📄 Traitement de : {filename}")
    
    extracted_pages = []
    
    try:
        doc = fitz.open(file_path)
        
        for page_num, page in enumerate(doc):
            # 1. Convertir la page PDF en Image (haute résolution)
            pix = page.get_pixmap(dpi=300)
            
            # 2. Prétraitement (Nettoyage)
            processed_img = preprocess_image(pix)
            
            # 3. OCR (Extraction du texte de l'image)
            # lang='fra' pour le français (si installé), sinon 'eng'
            ocr_text = pytesseract.image_to_string(processed_img, lang='eng')
            
            # 4. Analyse sémantique
            page_data = extract_semantic_data(ocr_text)
            page_data["page"] = page_num + 1
            extracted_pages.append(page_data)
            
        doc.close()

        # 5. Structuration des données (Sortie)
        output_file = file_path + f".{output_format}"
        
        if output_format == "json":
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(extracted_pages, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Terminé ! Données sauvegardées dans : {output_file}")
        return extracted_pages

    except Exception as e:
        print(f"❌ Erreur : {e}")
        return None

# --- MAIN ---
if __name__ == "__main__":
    # Test avec un fichier local (change le nom ici)
    input_file = input("Entrez le chemin du fichier (PDF ou Image) : ").replace('"', '')
    
    if os.path.exists(input_file):
        process_document(input_file, output_format="json")
    else:

        print("Fichier introuvable.")
