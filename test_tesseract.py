import fitz
import pytesseract  # type: ignore[import-untyped]

pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract_OSR\tesseract.exe'

print(f"PyMuPDF (fitz) версия: {fitz.__version__}")

# Проверка Tesseract (выведет версию движка, если он найден)
try:
    print(f"Tesseract версия: {pytesseract.get_tesseract_version()}")
except Exception as e:
    print(f"Ошибка с Tesseract: {e}")
