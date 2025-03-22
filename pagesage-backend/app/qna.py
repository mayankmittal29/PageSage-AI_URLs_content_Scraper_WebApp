# import os
# from langchain.chat_models import ChatOpenAI
# from langchain.schema import HumanMessage

# openai_api_key = os.getenv("OPENAI_API_KEY")

# def generate_answer(question: str, docs: list):
#     context = "\n\n".join(docs)
    
#     prompt = (
#         f"You are an expert assistant. Answer the following question based on the given context.\n\n"
#         f"Context:\n{context}\n\n"
#         f"Question: {question}\n\n"
#         f"Answer:"
#     )
    
#     chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)

#     messages = [HumanMessage(content=prompt)]

#     response = chat(messages)

#     return response.content
import os
import openai
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


openai.api_key = ''

# Initialize Chroma client and embedding model
chroma_client = chromadb.Client(Settings(chroma_db_impl="chromadb.db.impl.sqlite", persist_directory="./chromadb"))
collection = chroma_client.get_or_create_collection(name="pagesage_documents")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def answer_question(question):
    print(f"🧠 Processing question: {question}")

    # Create embedding for question
    question_embedding = embedding_model.encode(question)

    # Search for relevant documents in Chroma
    results = collection.query(
        query_embeddings=[question_embedding.tolist()],
        n_results=3
    )

    documents = results['documents'][0]
    print(f"🔍 Retrieved {len(documents)} documents for context")

    # Construct the prompt for GPT-3.5 Turbo
    context = "\n\n".join(documents)

    prompt = f"""You are PageSage AI. Use the following context to answer the question.

    Context:
    {context}

    Question:
    {question}

    Answer:"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.5
        )

        answer = response['choices'][0]['message']['content']
        print(f"✅ Answer generated")
        return answer

    except Exception as e:
        print(f"❌ Error generating answer: {str(e)}")
        return "Sorry, I couldn't process your question right now."
