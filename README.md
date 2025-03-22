

# 🦉 PageSage — Ask Anything from Any Webpage!

> **Unlock insights from any webpage in seconds. No BS. Only facts from the page.**


## 🚀 Live Demo
🔗 [Click here to try PageSage!](https://your-live-link.com)  
⚠️ **Note**: First-time scrape may take ~10 seconds while the Sage does its magic!

---

## ✨ Features
- 🔗 **Scrape Multiple URLs** — Just paste, click, and scrape content from any webpage.
- 🤖 **Ask Smart Questions** — Get answers strictly based on the scraped content (no hallucinations!).
- ⚡ **Fast & Lightweight** — Built with React + TailwindCSS on the front, FastAPI + FAISS on the back.
- 💾 **Embeddings & Vector Search** — Contextual answers powered by OpenAI + FAISS magic.
- 🧹 **Clean UI** — Minimal, intuitive, responsive. No clutter.

---

## 🎨 Tech Stack
| **Frontend**     | React.js + TailwindCSS |
|------------------|------------------------|
| **Backend**      | Python FastAPI         |
| **Scraper**      | BeautifulSoup + Requests |
| **Embeddings**   | OpenAI `text-embedding-ada-002` |
| **Vector Search**| FAISS                 |
| **LLM QA**       | OpenAI GPT-3.5 Turbo  |
| **Hosting**      | Vercel (Frontend), Railway/Render (Backend) |

---

## 🏗️ How It Works
1. **User submits URL(s)** from the web.
2. **FastAPI backend scrapes** the content, cleans it, and chunks it.
3. Chunks are **embedded using OpenAI embeddings** and stored in **FAISS**.
4. User **asks a question** in the UI.
5. Backend **embeds the question**, searches for similar chunks in FAISS, and passes them to **GPT-3.5-turbo**.
6. 🦉 **Sage answers** based on the scraped content!

---

## 📸 Screenshots

| Scrape Page | Ask Anything |
|-------------|--------------|
| ![Scrape](https://your-link.com/scrape.png) | ![Ask](https://your-link.com/ask.png) |

---

## ⚙️ Installation & Running Locally

### 📦 Backend Setup (FastAPI)
```bash
# 1. Clone the repo
git clone https://github.com/yourusername/pagesage.git
cd pagesage/backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run FastAPI server
uvicorn main:app --reload
```

### 🖼️ Frontend Setup (React + TailwindCSS)
```bash
# 1. Navigate to frontend
cd ../frontend

# 2. Install dependencies
npm install

# 3. Run React dev server
npm run dev
```

### ✅ Environment Variables

Backend `.env` (Place in `/backend`)
```
OPENAI_API_KEY=your-openai-api-key
```

Frontend `.env` (Optional for backend URL)
```
VITE_BACKEND_URL=http://localhost:8000
```

---

## 📝 API Endpoints

| **Route**       | **Method** | **Description**        |
|-----------------|------------|------------------------|
| `/scrape`       | POST       | Scrape URLs & create embeddings |
| `/ask`          | POST       | Ask questions about the content |

---

## 🤖 AI Workflow
1. **Scrape & Clean**: Grabs raw text (ignores navbars, ads, footers).
2. **Chunk & Embed**: Text split into chunks. OpenAI embeddings generated.
3. **Store in FAISS**: Vector index for fast similarity search.
4. **QA Logic**:
   - User submits a question.
   - Embedding generated.
   - Search for top-k matching chunks.
   - Pass chunks + question to GPT-3.5-turbo.
   - Return answer.

---

## 🚀 Deployment
### Frontend
1. Push frontend repo to GitHub.
2. Connect to **Vercel** → auto-deploy (build command `npm run build`, output `dist`).

### Backend
1. Push backend repo to GitHub.
2. Deploy on **Railway/Render**.
3. Expose FastAPI server endpoint (`/scrape`, `/ask`).

---

## 🎯 Project Structure
```
pagesage/
├── frontend/
│   ├── src/
│   ├── public/
│   └── ...
├── backend/
│   ├── main.py
│   ├── scraper.py
│   ├── embeddings.py
│   └── faiss_index/
└── README.md
```

---

## 🙌 Acknowledgments
- OpenAI for their powerful APIs!
- FAISS for blazing fast vector search.
- React & TailwindCSS for smooth frontend experience.
- FastAPI for a speedy backend framework.



## ✉️ Contact
Made with ❤️ by Mayank Mittal 
📧 Email: mayankmittal29042004@gmail.com  
🔗 LinkedIn: [https://www.linkedin.com/in/mayank-mittal-174a00254/](https://linkedin.com/in/yourprofile)

---
