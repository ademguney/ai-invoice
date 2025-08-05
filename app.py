import streamlit as st
from utils import get_pdf_text



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
            st.text_area("📃 Metin Çıktısı", raw_text, height=300)
        except Exception as e:
            st.error(f"❌ Hata oluştu: {e}")