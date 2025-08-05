import json
import os
import re
import anthropic
import pandas as pd
from pypdf import PdfReader
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables (.env)
load_dotenv()

# Anthropic client initialization
client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def extracted_data(pages_data: str):
    template = """
Aşağıdaki fatura metninden şu bilgileri çıkart:
- Fatura Numarası
- Fatura Tarihi
- Müşteri Adı
- Toplam Tutar
- Ödeme Tarihi (varsa)

Metin:
--------------------
{invoice_text}
--------------------

Lütfen bilgileri JSON formatında çıkar.
"""
    prompt = PromptTemplate.from_template(template)
    formatted_prompt = prompt.format(invoice_text=pages_data)

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=512,
        temperature=0.1,
        messages=[
            {"role": "user", "content": formatted_prompt}
        ]
    )
    return response.content[0].text

def clean_invoice_text(text: str):
    return re.sub(r"\s+", " ", text).strip()

def to_snake_case(text):
    text = re.sub(r"[\s\-]+", "_", text)
    text = re.sub(r'(?<!^)(?=[A-Z])', '_', text)
    return text.lower()

def json_to_dataframe(json_text: str):
    try:
        data_dict = json.loads(json_text)

        # Apply snake_case normalization
        normalized_dict = {}
        for key, value in data_dict.items():
            new_key = to_snake_case(key)
            normalized_dict[new_key] = value

        return pd.DataFrame([normalized_dict])
    except Exception as e:
        print("JSON parse error:", e)
        return pd.DataFrame()
