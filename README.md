# 🧠 AI Resume Builder with Gemini API

[![Streamlit App](https://img.shields.io/badge/Live-Demo-00C853?style=for-the-badge&logo=streamlit&logoColor=white)](https://resumely.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-FF4081?style=for-the-badge)](LICENSE)

> ✨ Instantly generate professional resume summaries using **Google Gemini Pro** and a sleek **Streamlit** UI.

---

## 📸 Preview

![AI Resume Builder Screenshot](https://github.com/chhavibhalla/ai-resume-builder/assets/screenshot-placeholder.png) <!-- Replace with actual screenshot link -->

---

## 🚀 Features

✅ Streamlit-powered responsive web UI  
🧠 AI-generated resume summaries using **Gemini Pro**  
📄 Upload and extract from PDF/DOCX resumes  
📝 Manual input for name, skills, experience, and education  
📤 Export summary as downloadable PDF  
🔐 Secure API key handling via `.streamlit/secrets.toml`  
🔥 Deployed on [Streamlit Cloud](https://resumely.streamlit.app/)

---

## 🛠️ Tech Stack

| Layer        | Tools Used                           |
|--------------|--------------------------------------|
| **Frontend** | Streamlit                            |
| **AI Engine**| Google Generative AI (Gemini Pro)    |
| **Backend**  | Python                               |
| **PDF Tools**| `fpdf`, `fpdf2`, `PyPDF2`, `docx2txt`|
| **Env Mgmt** | `python-dotenv`, `.streamlit/secrets.toml`|

---

## 📦 Requirements

> All dependencies are listed in `requirements.txt`

```txt
streamlit
google-generativeai
pandas
fpdf
docx2txt
PyPDF2
fpdf2>=2.7.4
python-dotenv


🔧 Setup & Installation
Clone the repository
bash
git clone https://github.com/chhavibhalla/ai-resume-builder.git
cd ai-resume-builder

bash
pip install -r requirements.txt

Add Google Gemini API Key
Create the file .streamlit/secrets.toml and add:
toml
[generativeai]
GOOGLE_API_KEY = "your_google_gemini_api_key"
Or use .env if preferred:
env
GOOGLE_API_KEY=your_google_gemini_api_key

Run the App
bash

streamlit run stream.py

✨ How It Works
User fills out resume info OR uploads resume file (PDF/DOCX)

Extracted or typed data is sent to Google Gemini Pro

Gemini returns a polished summary tailored to job profiles

User can preview, download, or copy the summary

🌐 Live App
Visit 👉 https://resumely.streamlit.app

🧑‍💻 Contributors
Made with ❤️ by:

Chhavi Bhalla

Prateek 

📄 License
This project is licensed under the MIT License.

💡 Future Improvements
🔍 Job description analysis for better summaries

📬 Email or LinkedIn integration

🎨 More resume templates and export formats

🗣️ Multi-language support
