import fitz  # PyMuPDF


def check_pdf_type(file_path):
    doc = fitz.open(file_path)
    page = doc.load_page(0)

    # Проверяем наличие изображений
    images = page.get_images()
    if images:
        print("Файл содержит изображения")

    # Проверяем наличие текстового слоя
    text = page.get_text()
    if text:
        print("В файле есть текстовый слой")
    else:
        print("Текстового слоя нет")

    # Проверяем количество страниц с изображениями
    image_pages = 0
    for page_num in range(len(doc)):
        if doc.load_page(page_num).get_images():
            image_pages += 1

    print(f"Страниц с изображениями: {image_pages}")
    print(f"Всего страниц: {len(doc)}")


check_pdf_type('3800 задач по физике для школьников и поступающих в ВУЗы.pdf')
