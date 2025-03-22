# # from sentence_transformers import SentenceTransformer
# # import chromadb
# # from chromadb.config import Settings

# # # Initialize ChromaDB and SentenceTransformer
# # chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chromadb"))
# # collection = chroma_client.get_or_create_collection(name="pagesage")

# # embedder = SentenceTransformer('all-MiniLM-L6-v2')

# # def add_to_chroma(url: str, content: str):
# #     docs = [content[i:i+500] for i in range(0, len(content), 500)]  # chunking text
# #     embeddings = embedder.encode(docs)

# #     for i, (doc, embedding) in enumerate(zip(docs, embeddings)):
# #         collection.add(
# #             documents=[doc],
# #             ids=[f"{url}_{i}"],
# #             embeddings=[embedding.tolist()]
# #         )

# # def query_chroma(query: str, n_results: int = 3):
# #     query_embedding = embedder.encode([query])[0].tolist()
    
# #     results = collection.query(
# #         query_embeddings=[query_embedding],
# #         n_results=n_results
# #     )
    
# #     docs = results.get('documents', [[]])[0]
    
# #     return docs
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# Initialize ChromaDB client
chroma_client = chromadb.Client(Settings(chroma_db_impl="chromadb.db.impl.sqlite", persist_directory="./chromadb"))

# Create collection if it doesn't exist
collection_name = "pagesage_documents"
collection = chroma_client.get_or_create_collection(name=collection_name)

# Load the sentence transformer model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def add_documents_to_chroma(documents):
    for idx, doc in enumerate(documents):
        embedding = embedding_model.encode(doc["content"])
        collection.add(
            documents=[doc["content"]],
            embeddings=[embedding.tolist()],
            ids=[f"doc_{idx}"],
            metadatas=[doc["metadata"]]
        )
        print(f"✅ Added doc_{idx} to ChromaDB")
