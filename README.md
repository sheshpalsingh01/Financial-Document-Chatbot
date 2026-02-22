# 📊 Financial AI Assistant (Hybrid RAG for Financial Documents)

An AI-powered financial document analysis system built using LangChain, Streamlit, and a Hybrid Retrieval Architecture.

This application allows users to upload financial reports (PDFs) and interact with them via an AI chatbot that preserves:

- Revenue figures
- Growth rates (%)
- Financial metrics
- Numerical precision
- Table-based data

Unlike basic RAG systems, this implementation uses Hybrid Retrieval (Semantic + Structured Extraction) to prevent numeric data loss.

---

## 🚀 Features

✅ Upload financial PDF documents  
✅ Extract both narrative text and tables  
✅ Preserve numeric values (growth %, revenue, profit)  
✅ Hybrid Retrieval (Vector Search + Structured Table Search)  
✅ Financial-aware prompt engineering  
✅ Streamlit UI for interactive Q&A  
✅ Production-ready architecture  

---

## 🧠 Architecture Overview
PDF Upload
↓
Dual Extraction
├── Text Extraction (Narrative)
└── Table Extraction (Structured Data)
↓
Numeric Normalization
↓
Storage
├── Vector DB (FAISS)
└── JSON (Extracted Tables)
↓
Hybrid Retrieval
↓
LLM Response
↓
Streamlit Interface


This approach ensures that financial metrics are not lost during embedding or chunking.

---

## 🛠 Tech Stack

- Python
- Streamlit
- LangChain
- OpenAI / LLM API
- FAISS (Vector DB)
- pdfplumber (Table Extraction)
- Pandas
- Regex-based numeric normalization

---

## 🔎 Why Hybrid RAG?

Traditional RAG systems struggle with:

- Percentages
- Financial tables
- Large numbers
- Structured metrics

This project solves that by:

- Extracting tables separately
- Normalizing numbers
- Combining structured + semantic retrieval

---

## 📦 Installation

### 1️⃣ Clone the repo

```bash
git clone https://github.com/yourusername/financial-ai-assistant.git
cd financial-ai-assistant

2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Add API Key
Create a .env file
NVIDIA_API_KEY=your_api_key_here

5️⃣ Run the app
streamlit run app.py