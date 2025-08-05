import streamlit as st
from utils import get_pdf_text, extracted_data



# Streamlit page settings
st.set_page_config(
    page_title="Invoice Extraction Bot",
    page_icon="📄",
    layout="centered"
)

st.title("🧾 Invoice Extraction Bot")
st.markdown("Bu araç, yüklediğiniz PDF faturaların içeriğini okuyup metin olarak gösterir.")



# File uploader
uploaded_files = st.file_uploader(
    "📤 Lütfen PDF faturaları yükleyin",
    type="pdf",
    accept_multiple_files= True
)


# File Processing
if uploaded_files:
    for file in uploaded_files:
        st.markdown(f"### Dosya: `{file.name}`")
        try:
            raw_text = get_pdf_text(file)
            st.text_area("📃 Faturadaki Metin", raw_text, height=250)

            if st.button(f"📤 `{file.name}` için Veriyi Çıkar"):
                with st.spinner("Claude veriyi cikariyor..."):
                    json_output = extracted_data(raw_text)
                    st.code(json_output, language="json")

        except Exception as e:
            st.error(f"❌ Hata oluştu: {e}")