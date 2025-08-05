import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import io

from utils import get_pdf_text, extracted_data, clean_invoice_text, json_to_dataframe

# Load .env file for API key
load_dotenv()

# Streamlit page settings
st.set_page_config(
    page_title="Invoice Extraction Bot",
    page_icon="📄",
    layout="centered"
)

st.title("🧾 Invoice Extraction Bot")
st.markdown("Extract structured data like invoice number, date, total amount, and customer info from your PDF invoices using **Claude 3 Haiku** (Anthropic).")

# File uploader
uploaded_files = st.file_uploader(
    "📤 Upload your invoice PDFs",
    type="pdf",
    accept_multiple_files=True
)

# Output storage
all_dataframes = []

# Extraction button
if st.button("🚀 Extract Data"):
    if not uploaded_files:
        st.warning("Please upload at least one PDF file.")
    else:
        with st.spinner("🔍 Extracting data from invoices..."):
            for file in uploaded_files:
                try:
                    st.markdown(f"### 📄 Processing: `{file.name}`")

                    raw_text = get_pdf_text(file)
                    cleaned_text = clean_invoice_text(raw_text)
                    json_response = extracted_data(cleaned_text)
                    df = json_to_dataframe(json_response)

                    if not df.empty:
                        df["File Name"] = file.name
                        st.success(f"✅ Data extracted from `{file.name}`")
                        st.dataframe(df)
                        all_dataframes.append(df)
                    else:
                        st.warning(f"⚠️ No data extracted from `{file.name}`.")

                except Exception as e:
                    st.error(f"❌ Error processing `{file.name}`: {e}")

        # Combine and offer download
        if all_dataframes:
            combined_df = pd.concat(all_dataframes, ignore_index=True)
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                combined_df.to_excel(writer, index=False, sheet_name="Invoices")

            st.download_button(
                label="📥 Download Excel",
                data=excel_buffer.getvalue(),
                file_name="extracted_invoices.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
