import json
import os
import re
import pandas as pd
import anthropic
from pypdf import PdfReader
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv


# Load enviroment variables (.env)
load_dotenv()


# Anthropic client initialization
client = anthropic.Anthropic(
    api_key= os.getenv("ANTHROPIC_API_KEY")
)

# step 1
def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

# step 2
def extracted_data(pages_data: str) -> str:
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
    prompt = PromptTemplate.from_template(template= template)
    formatted_prompt = prompt.format(invoice_text= pages_data)

    response = client.messages.create(
        model= "claude-3-haiku-20240307",
        max_tokens= 512,
        temperature= 0.1,
        messages=[
            {"role": "user", "content": formatted_prompt}
        ]
    )
    return response.content[0].text

# step 3
def clean_invoice_text(text: str):
    return re.sub(r"\s+", " ", text).strip()

def json_to_dataframe(json_text: str):
    try:
        data_dict = json.loads(json_text)
        return pd.DataFrame([data_dict])
    except Exception as e:
        print("JSON parse hatası:", e)
        return pd.DataFrame()