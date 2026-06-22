import fitz
import pytesseract  # type: ignore[import-untyped]
from PIL import Image
import re
import docx

pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract_OSR\tesseract.exe'


def extract_contents(pdf_path):
    doc = fitz.open(pdf_path)

    # Поиск страницы с содержанием
    for page_num in range(max(0, len(doc) - 10), len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text = pytesseract.image_to_string(img, lang='rus', config='--psm 6')

        if "Содержание" in text or "Оглавление" in text:
            print(f"Содержание найдено на странице {page_num + 1}")
            break

    # Очистка текста
    cleaned_text = re.sub(r'\s+', ' ', text)
    cleaned_text = cleaned_text.replace('\n', ' ')

    # Разделение на колонки
    mid_index = len(cleaned_text) // 2
    column1 = cleaned_text[:mid_index]
    column2 = cleaned_text[mid_index:]

    # Функция для обработки одной колонки с учетом структуры
    def process_column(column):
        # Разделяем строки по точкам с пробелами
        lines = re.split(r'(?<=\d)\s+', column)
        result = []
        section = ''
        subsection = ''

        for line in lines:
            # Ищем номер страницы в конце строки
            match = re.search(r'(\d+)$', line)
            if match:
                page = match.group(1)
                title = line[:line.rfind(page)].strip()

                # Определяем тип заголовка
                if re.match(r'^\d+\.', title):  # Подраздел
                    subsection = title
                    result.append((subsection, '', page))
                elif re.match(r'^[А-Я][а-я]+', title):  # Раздел
                    section = title
                    result.append((section, '', ''))
                else:  # Обычный пункт
                    result.append((section, title, page))
        return result

    # Обрабатываем обе колонки
    contents = process_column(column1) + process_column(column2)

    return contents


def save_to_word(contents, output_path='contents.docx'):
    doc = docx.Document()

    doc.add_heading('Содержание', level=1)

    current_section = ''
    current_subsection = ''

    for section, title, page in contents:
        if section and section != current_section:
            paragraph = doc.add_paragraph()
            run = paragraph.add_run(section)
            run.font.bold = True
            run.font.size = docx.shared.Pt(14)
            current_section = section

        elif title and title != current_subsection:
            paragraph = doc.add_paragraph()
            run = paragraph.add_run(title)
            run.font.bold = True
            run.font.size = docx.shared.Pt(12)
            current_subsection = title

        elif page:
            paragraph = doc.add_paragraph()
            run = paragraph.add_run(title)
            run.font.bold = False
            run.font.size = docx.shared.Pt(10)
            paragraph.add_run(f'\t\t\t\t{page}')

    doc.save(output_path)
    print(f"Файл сохранён как {output_path}")


if __name__ == "__main__":
    pdf_path = '3800 задач по физике для школьников и поступающих в ВУЗы.pdf'
    contents = extract_contents(pdf_path)
    save_to_word(contents)
