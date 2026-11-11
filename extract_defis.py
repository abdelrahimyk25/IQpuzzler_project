import json
from pathlib import Path
import sys

# Import pymupdf (alias fitz)
import pymupdf as fitz

# Chemins
PROJECT_ROOT = Path(__file__).parent
PDF_PATH = PROJECT_ROOT / "SmartGames_IQ_Puzzler_Pro_XXL_IQ_Puzzler_Pro_XXL_-_Livret_de_défis_(1)_(1).pdf"
JSON_PATH = PROJECT_ROOT / "defis.json"

START_PAGE = 4   # 1‑based page numbers in the PDF
END_PAGE   = 98

def extract_page_text(page_number: int) -> str:
    """Retourne le texte brut d’une page du PDF (sans OCR)."""
    doc = fitz.open(str(PDF_PATH))
    page = doc.load_page(page_number - 1)   # pymupdf est 0‑based
    txt = page.get_text("text")
    doc.close()
    return txt

def main():
    if not PDF_PATH.is_file():
        print(f"❌ PDF introuvable : {PDF_PATH}")
        sys.exit(1)

    # Charge le JSON existant (ou crée‑le s’il n’existe pas)
    if JSON_PATH.is_file():
        data = json.load(open(JSON_PATH, "r", encoding="utf-8"))
    else:
        data = {}

    for num in range(START_PAGE, END_PAGE + 1):
        raw = extract_page_text(num)
        defi_id = str(num - 3)   # le premier défi correspond à la page 4
        entry = data.get(defi_id, {})
        entry["raw_text"] = raw.strip()
        # on conserve les champs déjà présents (mode, difficulte, ...) si ils existent
        data[defi_id] = entry
        print(f"✅ Page {num} → défi {defi_id} enregistré (texte brut {len(raw)} caractères)")

    # Sauvegarde
    json.dump(data, open(JSON_PATH, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("\n🗂 defis.json mis à jour avec les champs `raw_text` pour les défis 1‑95.")

if __name__ == "__main__":
    main()
