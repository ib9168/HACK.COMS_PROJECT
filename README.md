# 👗 VirtualCloset
**Your AI-powered wardrobe assistant**

VirtualCloset helps users organize their clothes, generate outfit ideas, and discover new combinations using Google Gemini.

---

## ✨ Features
- Add, edit, and remove items in a **digital closet**
- Ask in natural language (e.g., “I have a red floral skirt”) and get **AI outfit ideas**
- Pair selected items and get a **Gemini-powered** rationale
- Data persisted locally via **SQLite**

---

## 🧠 Inspiration
Deciding what to wear is time-consuming. We wanted to make fashion easier and smarter by combining creativity with AI.

---

## 📦 Tech Stack
- **Frontend:** Java, JavaFX
- **Backend:** Python, FastAPI
- **AI:** Google Gemini (via `google-genai`)
- **Data:** SQLite + Pandas
- **Other:** Pydantic, SQLAlchemy, Uvicorn, python-dotenv


---

## ⚙️ Prerequisites
- **Python 3.11+**
- **Java 17+** (JDK)
- **Maven** (for the JavaFX app)
- A Google Gemini API key

---

## 🔐 Environment Variables
Create a `.env` file inside **`clothe-ai-backend/`**:
GOOGLE_API_KEY=your-real-key
> Tip: Do **not** hardcode keys in code or commit `.env`.

---

## 🚀 Run the Backend (FastAPI)
```bash
cd clothe-ai-backend
pip install -r requirements.txt

# start dev server
uvicorn app:app --reload
# Server: http://127.0.0.1:8000
# Docs:   http://127.0.0.1:8000/docs

Run the front end:
cd clothe-ai-frontend/main_page
mvn clean javafx:run

In your java code, point API front end to:
http://127.0.0.1:8000
