# With replacing table -------------------------------------------------------------------------

from pdfminer.high_level import extract_text
import tabula
import re


def replace_exact_floats(text, value):
    pattern = r"(?<!\S)" + re.escape(str(value)) + r"(?!\S)"
    return re.sub(pattern, "", text)


def pdf_to_text_and_tables(file_path):
    text = extract_text(file_path)
    text = text.replace('\xad\n', '')

    # Remove table values from the extracted text
    tables = tabula.read_pdf(file_path, pages='all', silent=True)
    table_values = []
    for table in tables:
        table_values.extend(table.values.flatten())

    # Remove table text from the extracted text
    text_without_tables = text
    for i, value in enumerate(table_values):
        if i == len(table_values) - 1:
            all_values = ' -/- '.join(map(str, table_values))
            text_without_tables = text_without_tables.replace(str(value), all_values)
        try:
            float_value = float(value)
            text_without_tables = replace_exact_floats(text_without_tables, value)
        except ValueError:
            text_without_tables = text_without_tables.replace(str(value), "")

    paragraphs = text_without_tables.split('\n\n')

    # Remove paragraphs that match the table values or contain only content inside
    filtered_paragraphs = []
    for paragraph in paragraphs:
        if paragraph.strip() == '-' or not paragraph.strip() or len(paragraph.strip().split()) == 1:
            continue
        #paragraph = paragraph.replace("\n", "\n ")
        filtered_paragraphs.append(paragraph.strip())

    return filtered_paragraphs, tables


