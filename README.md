# 🔍 LeadGen AI — Intelligent Lead Generation Assistant

A full-stack AI-powered lead generation assistant that scrapes company data from YellowPages, matches Ideal Customer Profile (ICP), and generates summaries using Gemini. Built with Flask + LangGraph + Gemini + Selenium.

### Video & Overview Document

https://drive.google.com/drive/folders/12PDXIDHRg8Unr4WdIk3Neu1BYgEwzVRO?usp=sharing

---

## 🚀 Features

- 🌐 **Company Scraping** from YellowPages using Selenium
- ✅ **ICP Matching** using Gemini (LLM)
- 📄 **Company Summarization** via Google Gemini API
- 💾 **Downloadable CSV** for scraped and matched data
- 🔁 **LangGraph Workflow** for clean modular logic

---

## 🔮 Future Development

The project can be further enhanced by integrating machine learning to refine lead scoring accuracy. By training ML models on factors influencing successful conversions (e.g., past customer behavior, engagement data), the tool can learn to prioritize leads more effectively. Clustering historical customer data can help identify common traits among high-value clients, allowing the system to recommend potential ICP profiles users might overlook.

Additionally, LangGraph’s modular design enables seamless experimentation with multiple models (e.g., scoring algorithms, summarization approaches) without altering the overall project structure. Developers can plug in new ML-based nodes—such as a custom classifier for ICP match scoring or a sentiment analyzer for summary tone—into the LangGraph pipeline, making it ideal for A/B testing and rapid iteration. This flexibility accelerates innovation while keeping the system stable and maintainable.

---

## 🧠 Workflow Overview

```text
User Input (Industry + City)
        ↓
[LangGraph] → Scrape → ICP Match → Summarize
        ↓
Flask Session Stores Progress
        ↓
Frontend Render (HTML)
```

---


## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/chinmay1p/Lead-Gen-Tool.git
```

### 2. Create `.env` file

```env
GOOGLE_API_KEY=your_gemini_api_key
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Make sure **Google Chrome** and **ChromeDriver** are installed and compatible.

### 4. Run the App

```bash
python main.py
```

---

## 📦 Requirements

- Python 3.8+
- Flask
- Selenium
- pandas
- google-generativeai
- LangGraph
- BeautifulSoup4
- ChromeDriver

---

## Demo and working

![image](https://github.com/user-attachments/assets/5538cb21-9151-4333-9946-3d8521445cec)

![image](https://github.com/user-attachments/assets/45fd46c3-ba44-4ecc-82ae-e77c12b5ad99)

![image](https://github.com/user-attachments/assets/c66cf4d7-2fae-4f03-90bb-6e1c639813c9)

![image](https://github.com/user-attachments/assets/d9f716ce-6c87-4d7a-98e6-309e21a7caba)

![image](https://github.com/user-attachments/assets/699733e1-293b-49d9-ab2e-d2614e55a7c3)

![image](https://github.com/user-attachments/assets/a8fb8631-1b7f-4811-a191-3269387ab839)

![image](https://github.com/user-attachments/assets/f8b63486-fe77-47b0-8459-27cc2c9e926c)

![image](https://github.com/user-attachments/assets/aa4bb6fc-14a2-47f2-93f4-7254c199e546)

![image](https://github.com/user-attachments/assets/f3f40c78-70d9-47e5-abe6-70d9ee6752d3)

---
