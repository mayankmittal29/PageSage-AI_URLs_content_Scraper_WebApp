# import os
# import requests
# import chromadb
# from sentence_transformers import SentenceTransformer
# from chromadb import PersistentClient

# # Initialize ChromaDB client
# chroma_client = PersistentClient(path="chromedb")
# print("Available collections:")
# print(chroma_client.list_collections())

# # Get the correct collection
# collection = chroma_client.get_collection(name="sentence_embeddings")
# embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# print(f"📊 Collection statistics: {collection.count()} documents")

# def generate_answer_with_hf(prompt, model_id="google/flan-t5-base"):
#     """
#     Use Hugging Face's free inference API to generate an answer.
#     You can get a free API token at https://huggingface.co/settings/tokens
#     """
#     API_TOKEN = ''
    
#     # If no token is provided, inform the user
#     if not API_TOKEN:
#         print("⚠️ No Hugging Face API token found. Using a very basic answer extraction method.")
#         return None
    
#     API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
#     headers = {"Authorization": f"Bearer {API_TOKEN}"}
    
#     try:
#         response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         return response.json()[0]["generated_text"]
#     except Exception as e:
#         print(f"⚠️ Hugging Face API error: {str(e)}")
#         return None

# def simple_answer_extraction(question, documents):
#     """
#     A very basic approach to extract answers when no LLM is available.
#     This is a fallback method and won't be as sophisticated as an LLM.
#     """
#     # Combine documents into a single text
#     combined_text = " ".join(documents)
    
#     # Convert to lowercase for easier matching
#     question_lower = question.lower()
#     combined_text_lower = combined_text.lower()
    
#     # Extract simple answers based on question type
#     if "who is" in question_lower or "what is" in question_lower:
#         # Find the subject of the question
#         subject = question_lower.replace("who is", "").replace("what is", "").strip()
        
#         # Look for sentences containing the subject
#         for doc in documents:
#             if subject in doc.lower():
#                 return doc
                
#     if "when" in question_lower:
#         # Look for dates or time references
#         import re
#         date_patterns = [
#             r'\d{1,2}/\d{1,2}/\d{2,4}',  # MM/DD/YYYY
#             r'\d{1,2}-\d{1,2}-\d{2,4}',  # MM-DD-YYYY
#             r'\b\d{4}\b',                # YYYY
#             r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\b \d{1,2}(st|nd|rd|th)?, \d{4}'
#         ]
        
#         for pattern in date_patterns:
#             matches = re.findall(pattern, combined_text)
#             if matches:
#                 return f"According to the information: {matches[0]} (found in context)"
    
#     # Default to returning the most relevant document
#     return f"According to the most relevant information: {documents[0]}"

# def answer_question(question):
#     print(f"🧠 Processing question: {question}")
    
#     # Create embedding for question
#     question_embedding = embedding_model.encode(question).tolist()
    
#     # Search for relevant documents in Chroma
#     results = collection.query(
#         query_embeddings=[question_embedding],
#         n_results=5,
#         include=["documents", "metadatas", "distances"]
#     )
    
#     documents = results['documents'][0]
#     distances = results['distances'][0]
    
#     print(f"🔍 Retrieved {len(documents)} documents for context")
#     for i, (doc, dist) in enumerate(zip(documents, distances)):
#         print(f"Document {i+1} (similarity: {1-dist:.4f}): {doc[:50]}...")
    
#     # Construct the prompt for LLM
#     context = "\n\n".join(documents)
#     prompt = f"""Answer the following question based only on the context provided. If the context doesn't contain the answer, say 'I don't have enough information to answer this question.'
    
# Context:
# {context}

# Question:
# {question}

# Answer:"""
    
#     # Try Hugging Face Inference API first
#     answer = generate_answer_with_hf(prompt)
    
#     # If Hugging Face fails, fall back to simple extraction
#     if not answer:
#         answer = simple_answer_extraction(question, documents)
#         print("✅ Answer generated using simple extraction")
#     else:
#         print("✅ Answer generated using Hugging Face")
        
#     return answer

# # Example usage
# if __name__ == "__main__":
#     while True:
#         question = input("\nEnter your question (or 'quit' to exit): ")
#         if question.lower() in ['quit', 'exit', 'q']:
#             break
#         answer = answer_question(question)
#         print("\n🤖 Answer:")
#         print(answer)

import os
import requests
import chromadb
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient

# Initialize ChromaDB client
chroma_client = PersistentClient(path="chromedb")
print("Available collections:")
print(chroma_client.list_collections())

# Get the correct collection
collection = chroma_client.get_collection(name="sentence_embeddings")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

print(f"📊 Collection statistics: {collection.count()} documents")

# Hugging Face API setup
HF_API_TOKEN = ""  # Replace with your actual token
HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

def generate_answer_with_hf(prompt):
    """
    Uses Hugging Face API to generate an answer based on the prompt.
    """
    if not HF_API_TOKEN or HF_API_TOKEN == "":
        print("⚠️ Please set your Hugging Face API token.")
        return None

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 256,
            "temperature": 0.7,
            "top_p": 0.9,
            "repetition_penalty": 1.2
        }
    }

    try:
        response = requests.post(HF_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()

        # The structure depends on the model output
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"].strip()
        else:
            print("⚠️ Unexpected response format:", result)
            return None
    except Exception as e:
        print(f"⚠️ Hugging Face API error: {str(e)}")
        return None

def answer_question(question):
    print(f"🧠 Processing question: {question}")
    
    # Create embedding for question
    question_embedding = embedding_model.encode(question).tolist()
    
    # Search for relevant documents in Chroma
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=5,
        include=["documents", "metadatas", "distances"]
    )
    
    documents = results['documents'][0]
    distances = results['distances'][0]
    
    print(f"🔍 Retrieved {len(documents)} documents for context")
    for i, (doc, dist) in enumerate(zip(documents, distances)):
        print(f"Document {i+1} (similarity: {1-dist:.4f}): {doc[:80]}...")
    
    # Construct the prompt for LLM
    context = "\n\n".join(documents)
    prompt = f"""Answer the following question based only on the context provided. If the context doesn't contain the answer, say 'I don't have enough information to answer this question.'

Context:
{context}

Question:
{question}

Answer:"""
    
    # Generate answer using Hugging Face API
    answer = generate_answer_with_hf(prompt)
    
    if not answer:
        print("⚠️ No answer returned from Hugging Face.")
        # Optional fallback:
        answer = simple_answer_extraction(question, documents)
        print("✅ Answer generated using simple extraction")
    else:
        print("✅ Answer generated using Hugging Face")
        
    return answer

# Basic fallback extraction (optional)
def simple_answer_extraction(question, documents):
    combined_text = " ".join(documents)
    question_lower = question.lower()
    
    # Example keyword search
    if "who is" in question_lower or "what is" in question_lower:
        subject = question_lower.replace("who is", "").replace("what is", "").strip()
        for doc in documents:
            if subject in doc.lower():
                return doc
                
    return f"According to the most relevant information: {documents[0]}"

# Example usage
if __name__ == "__main__":
    while True:
        question = input("\nEnter your question (or 'quit' to exit): ")
        if question.lower() in ['quit', 'exit', 'q']:
            break
        answer = answer_question(question)
        print("\n🤖 Answer:")
        print(answer)
