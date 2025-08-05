from pypdf import PdfReader


def get_pdf_tesxt(pdf_doc) -> str:
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text