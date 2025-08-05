# 🧾 Invoice Extraction Bot

This is a lightweight Streamlit web application that extracts structured information from PDF invoices using **Claude 3 Haiku** by Anthropic.

## 🚀 Features

- Upload one or more PDF invoices
- Extract:
  - Invoice Number
  - Invoice Date
  - Customer Name
  - Total Amount
  - Payment Date (if available)
- View results in tabular form
- Download all extracted data as a single Excel file

## 🧠 Powered By

- [Claude 3 Haiku (Anthropic)](https://www.anthropic.com/index/claude)
- [LangChain Prompt Templates](https://www.langchain.com/)
- [Streamlit](https://streamlit.io/)
- [PyPDF](https://pypi.org/project/pypdf/)

## 📂 Project Structure

``` bash
invoice_extractor/
│
├── app.py # Main Streamlit application
├── utils.py # Utility functions: PDF parsing, Claude API, etc.
├── requirements.txt # Project dependencies
├── .env # API key for Claude (not committed)
└── README.md # Project documentation
```


## ⚙️ Setup & Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/invoice-extraction-bot.git
cd invoice-extraction-bot
```

2. **Install dependencies::**
``` bash
pip install -r requirements.txt
```

3. **Set up your environment variables:**
``` bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here

```
4. **Run the app**
 ``` bash
   streamlit run app.py

   ```
