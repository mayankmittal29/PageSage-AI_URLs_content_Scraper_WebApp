# # # from sentence_transformers import SentenceTransformer
# # # import chromadb
# # # from chromadb.config import Settings

# # # # Initialize ChromaDB and SentenceTransformer
# # # chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chromadb"))
# # # collection = chroma_client.get_or_create_collection(name="pagesage")

# # # embedder = SentenceTransformer('all-MiniLM-L6-v2')

# # # def add_to_chroma(url: str, content: str):
# # #     docs = [content[i:i+500] for i in range(0, len(content), 500)]  # chunking text
# # #     embeddings = embedder.encode(docs)

# # #     for i, (doc, embedding) in enumerate(zip(docs, embeddings)):
# # #         collection.add(
# # #             documents=[doc],
# # #             ids=[f"{url}_{i}"],
# # #             embeddings=[embedding.tolist()]
# # #         )

# # # def query_chroma(query: str, n_results: int = 3):
# # #     query_embedding = embedder.encode([query])[0].tolist()
    
# # #     results = collection.query(
# # #         query_embeddings=[query_embedding],
# # #         n_results=n_results
# # #     )
    
# # #     docs = results.get('documents', [[]])[0]
    
# # #     return docs
# from sentence_transformers import SentenceTransformer
# import chromadb
# from chromadb.config import Settings

# # Initialize ChromaDB client
# chroma_client = chromadb.Client(Settings(chroma_db_impl="chromadb.db.impl.sqlite", persist_directory="./chromadb"))

# # Create collection if it doesn't exist
# collection_name = "pagesage_documents"
# collection = chroma_client.get_or_create_collection(name=collection_name)

# # Load the sentence transformer model
# embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# def add_documents_to_chroma(documents):
#     for idx, doc in enumerate(documents):
#         embedding = embedding_model.encode(doc["content"])
#         collection.add(
#             documents=[doc["content"]],
#             embeddings=[embedding.tolist()],
#             ids=[f"doc_{idx}"],
#             metadatas=[doc["metadata"]]
#         )
#         print(f"✅ Added doc_{idx} to ChromaDB")
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import os

# Step 1: Load the cleaned sentences
def load_sentences(file_path):
    sentences = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Ignore empty lines or document separators
            if line and line != "---":
                sentences.append(line)
    return sentences

# Step 2: Generate embeddings using sentence-transformers
def generate_embeddings(sentences, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(sentences, show_progress_bar=True)
    return embeddings

# Step 3: Store embeddings in Chroma DB
def store_embeddings_in_chroma(sentences, embeddings, persist_directory="chromedb"):
    # Create the folder if not exists
    os.makedirs(persist_directory, exist_ok=True)

    # Initialize Chroma client with persistence
    client = chromadb.PersistentClient(path=persist_directory)

    # Create or get a collection
    collection_name = "sentence_embeddings"
    collection = client.get_or_create_collection(collection_name)

    # Add embeddings and sentences as metadata
    ids = [f"sentence_{i}" for i in range(len(sentences))]
    metadata = [{"text": sentence} for sentence in sentences]

    collection.add(
        embeddings=embeddings,
        documents=sentences,
        ids=ids,
        metadatas=metadata
    )

    print(f"✅ Stored {len(sentences)} sentences in Chroma DB at {persist_directory}")
def embed() :
    cleaned_file_path = "cleaned.txt"

    # Step 1
    sentences = load_sentences(cleaned_file_path)
    print(f"📄 Loaded {len(sentences)} sentences from {cleaned_file_path}")

    # Step 2
    embeddings = generate_embeddings(sentences)

    # Step 3
    store_embeddings_in_chroma(sentences, embeddings, persist_directory="chromedb")

