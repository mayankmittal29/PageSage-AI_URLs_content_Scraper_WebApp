import requests
from bs4 import BeautifulSoup
import re
import nltk
import emoji
import string
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download NLTK resources if not already downloaded
nltk.download('punkt')
nltk.download('stopwords')

def tokenize_text(text):
    
        # patterns = {
        #     # r'\b(?:https?://|www\.)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?' : '<URL>',
        #     r'#[\w$%&-]+': '<HASHTAG>',                    # Hashtags
        #     r'@\w+': '<MENTION>',                    # Mentions (e.g., @username)
        #     r'\d+\s*%': '<PERCENTAGE>',                 # Percentages (e.g., 10%)
        #     r'\d+\s*(?:years|yr|y)\s*old': '<AGE>',  # Age values (e.g., 25 years old)
        #     r'\d{1,2}[:/]\d{1,2}': '<TIME>',        # Time (e.g., 12:30 or 12/30)
        #     r'(?:\d{1,2}\s*(?:am|pm))': '<TIME>',   # Time in 12-hour format (e.g., 12:30pm)
        #     r'\d+\s*(?:months?|years?|days?)': '<TIME_PERIOD>' , # Time periods (e.g., 3 months)
        #     r'\d{10}': '<PHONE>',                        # Phone numbers (simple 10-digit matching, can be adjusted)
        #     r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}': '<EMAIL>',  # Email addresses
        #     r'\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+\s+\d{4}?': '<DATE>',  # Format: 27th December 2007
        #     r'[A-Za-z]+\s+\d{1,2}(?:st|nd|rd|th)?,\s+\d{4}?': '<DATE>',  # Format: December 27th, 2007
        #     r'\d+°' :'<DEGREE>',
        #     r'\w\s?\.\s?\w\s?\.\s?\w': '<ABBREVATION>',                 # Abbrevation
        #     r'[A-Za-z0-9_-]+\.(?:zip?|txt?|htm?)' : '<FILENAME>',     # Filename
        # }
        text = text.replace('''"''','')
        text = text.replace('...','')
        text = text.replace('--',' ')
        text = text.replace('viz.','viz')
        text = text.replace('e.g.','eg')
        text = re.sub(r'\b([A-Z])\.', r'\1', text)
        text = re.sub(r'\[\s*\d+\s*\]', '', text)  # Removes citation brackets like [18] or [ 18 ]
        text = re.sub(r'\b(?:Mr|Mrs|Ms|Miss|Dr|Prof|Sr|Jr|Capt|Col|Gen|Rev|Hon|Fr|St|Sir|Madam|Mx)\.\s*','',text)
        text = re.sub(r'\(\b(?:https?://|www\.)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?\)', r'(<URL>)', text)
        text = re.sub(r'\b(?:https?://|www\.)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?', '<URL>', text)
        text = re.sub(r'\(([^()]*?)[!?.]([^()]*)\)', r'(\1\2)', text)
        # Replace all special patterns with placeholders
        # for pattern, placeholder in patterns.items():
        #     text = re.sub(pattern, placeholder, text)
        # Adjust the sentence pattern to include punctuation
        sentence_pattern = r'([.!?;])'
        # Split the text into sentences and keep the punctuation with the sentence
        sentences = re.split(sentence_pattern, text)
        # Reorganize the split parts back into sentences including punctuation
        sentence_groups = []
        for i in range(0, len(sentences) - 1, 2):
            sentence = sentences[i].strip() + sentences[i+1].strip()
            sentence_groups.append(sentence)
        if(len(sentences)%2==1):
            sentence_groups.append(sentences[-1].strip())
        # Tokenize each sentence and preserve punctuation
        tokenized_sentences = []
        for sentence in sentence_groups:
            # Match words, punctuation, and other significant symbols
            tokens = re.findall(r'[A-Za-z0-9<>’\'@#%\$\d\-]+(?:_[A-Za-z0-9]+)*|[.,!?;:"()\[\]]', sentence.strip())
            if tokens and tokens != ['.']:  # Only add non-empty sentences
                tokenized_sentences.append(tokens)

        return tokenized_sentences

def clean_text(text):
    # Lowercase
    text = text.lower()
    return tokenize_text(text)

def extract_full_content(soup):
    # First remove unwanted elements
    for unwanted in soup.find_all(['nav', 'footer', 'header', 'aside', 'script', 'style', 'iframe']):
        unwanted.decompose()
    
    # Try to find the main content area
    main_content = None
    for selector in [
        {'tag': 'main'},
        {'tag': 'article'},
        {'tag': ['div', 'section'], 'attrs': {'id': re.compile('(content|main|article)', re.I)}},
        {'tag': ['div', 'section'], 'attrs': {'class': re.compile('(content|main|article|text|body)', re.I)}}
    ]:
        tag = selector.get('tag')
        attrs = selector.get('attrs', {})
        found = soup.find(tag, attrs) if attrs else soup.find(tag)
        if found and len(found.get_text(strip=True)) > 200:  # Ensure it has substantial content
            main_content = found
            break
    
    # If we found main content, extract from there, otherwise use whole body
    text_content = []
    if main_content:
        elements = main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'blockquote', 'pre', 'code'])
    else:
        elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'blockquote', 'pre', 'code'])
    
    # Add elements that have meaningful content
    for elem in elements:
        text = elem.get_text(strip=True)
        if text and len(text) > 10:  # Avoid very short fragments
            text_content.append(text)
    
    return "\n".join(text_content)

def scrape_and_store(urls):
    documents = []
    raw_texts = []

    for url in urls:
        try:
            print(f"🔎 Scraping URL: {url}")
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract visible text
            text = extract_full_content(soup)

            if text:
                raw_texts.append(f"URL: {url}\n{text}\n{'='*80}\n")
                documents.append({"content": text, "metadata": {"source": url}})
                print(f"✅ Successfully scraped {url}")
            else:
                print(f"⚠️ No text found at {url}")
            # Save raw scraped data
            with open("scrap.txt", "w", encoding="utf-8") as raw_file:
                raw_file.writelines(raw_texts)
            print("📄 Raw scraped data saved to scrap.txt")
        except Exception as e:
            print(f"❌ Error scraping {url}: {str(e)}")


    # Process and clean each document
    cleaned_corpus = []
    for doc in documents:
        tokenized_sentences = clean_text(doc["content"])
        cleaned_corpus.append(tokenized_sentences)

    with open("cleaned.txt", "w", encoding="utf-8") as clean_file:
        for doc_sentences in cleaned_corpus:
            for sentence in doc_sentences:
                # Convert the list of tokens to a string format
                sentence_str = ' '.join(sentence)
                clean_file.write(sentence_str + '\n')
            clean_file.write('---\n')  # Separator between documents

    print("🧹 Cleaned, tokenized data saved to cleaned.txt")

    return f"Scraped {len(documents)} URLs. Raw and cleaned data saved."

# Example usage
urls = [
    'https://en.wikipedia.org/wiki/Mukesh_Ambani',
]

scrape_and_store(urls)
