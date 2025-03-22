# import requests
# from bs4 import BeautifulSoup

# def scrape_website(url: str) -> str:
#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
        
#         soup = BeautifulSoup(response.text, "html.parser")

#         # Extract visible text
#         text = ' '.join([p.get_text(strip=True) for p in soup.find_all(['p', 'h1', 'h2', 'h3'])])
        
#         return text
#     except Exception as e:
#         raise Exception(f"Scraping failed: {e}")
import requests
from bs4 import BeautifulSoup
from app.embeddings import add_documents_to_chroma

def scrape_and_store(urls):
    documents = []

    for url in urls:
        try:
            print(f"Scraping URL: {url}")
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract visible text
            paragraphs = soup.find_all('p')
            print(paragraphs)
            text = "\n".join([p.get_text() for p in paragraphs])
            print(text)
            if text:
                documents.append({"content": text, "metadata": {"source": url}})
                print(f"✅ Successfully scraped {url}")
            else:
                print(f"⚠️ No text found at {url}")

        except Exception as e:
            print(f"❌ Error scraping {url}: {str(e)}")

    if documents:
        print("🚀 Adding documents to ChromaDB...")
        add_documents_to_chroma(documents)
        return f"Scraped and stored {len(documents)} documents!"
    else:
        return "No documents were scraped."

