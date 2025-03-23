# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from app.scraper import scrape_website
# from app.embeddings import add_to_chroma, query_chroma
# from app.qna import generate_answer
# import os

# # load_dotenv()

# # app = FastAPI(title="PageSage Backend 🚀")

# # # Request Models
# # class ScrapeRequest(BaseModel):
# #     url: str

# # class QuestionRequest(BaseModel):
# #     question: str

# # @app.get("/")
# # async def root():
# #     return {"message": "Welcome to PageSage Backend API 🚀"}

# # @app.post("/scrape")
# # async def scrape_and_index(request: ScrapeRequest):
# #     print(request)
# #     url = request.url
# #     print(url)
# #     try:
# #         content = scrape_website(url)
# #         add_to_chroma(url, content)
# #         return {"message": "Scraping and indexing successful!", "url": url}
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))

# # @app.post("/ask")
# # async def ask_question(request: QuestionRequest):
# #     question = request.question
# #     try:
# #         docs = query_chroma(question)
# #         answer = generate_answer(question, docs)
# #         return {"question": question, "answer": answer}
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))
# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Hello from PageSage Backend!"}
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.scraper import scrape_and_store
from app.qna import answer_question

app = FastAPI()

# Allow frontend (React app) to talk to backend (FastAPI)
origins = [
    "http://localhost:3000",  # Frontend port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "PageSage Backend is up!"}

@app.post("/scrape")
async def scrape(request: Request):
    data = await request.json()
    urls = data.get("urls", [])
    print(f"Received URLs to scrape: {urls}")  # Terminal log

    if not urls:
        return {"message": "No URLs provided!"}
    result = scrape_and_store(urls)
    return {"message": result}

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    question = data.get("question", "")
    print(f"Received Question: {question}")  # Terminal log

    if not question:
        return {"answer": "No question provided!"}
    answer="received"
    answer = answer_question(question)
    return {"answer": answer}
