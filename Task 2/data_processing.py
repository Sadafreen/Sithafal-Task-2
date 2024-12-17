import requests
from bs4 import BeautifulSoup
import sys
from flask import Flask, request, jsonify, render_template

try:
    from sentence_transformers import SentenceTransformer
except ModuleNotFoundError as e:
    print("Error: Missing required package 'sentence_transformers'. Please install it using 'pip install sentence-transformers'.")
    sys.exit(1)

try:
    import faiss
except ModuleNotFoundError as e:
    print("Error: Missing required package 'faiss'. Please install it using 'pip install faiss-cpu'.")
    sys.exit(1)

from transformers import pipeline

# Initialize components
try:
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Embedding model
except Exception as e:
    print(f"Error initializing SentenceTransformer model: {e}")
    sys.exit(1)

vector_dim = embedding_model.get_sentence_embedding_dimension()
index = faiss.IndexFlatL2(vector_dim)  # FAISS vector index
metadata_store = []  # Store metadata associated with embeddings

gemini_api_key = "AIzaSyDnEZOA092YEBdA3CYysRgZRIihV4kJxoo"  # Gemini API key

def crawl_and_scrape(url):
    """Crawl and scrape a single webpage."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}. Error: {e}")
        return []
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extract textual content from paragraphs and headers
    texts = [tag.get_text(strip=True) for tag in soup.find_all(['p', 'h1', 'h2', 'h3'])]
    return texts

def process_and_store(urls):
    """Process and store embeddings and metadata for given URLs."""
    for url in urls:
        print(f"Processing: {url}")
        content = crawl_and_scrape(url)
        for i, chunk in enumerate(content):
            try:
                embedding = embedding_model.encode(chunk, convert_to_tensor=False)
                index.add(embedding.reshape(1, -1))
                metadata_store.append({'url': url, 'content': chunk})
            except Exception as e:
                print(f"Error processing chunk: {chunk[:30]}... Error: {e}")

def retrieve_similar_chunks(query, top_k=5):
    """Retrieve similar chunks for a given query."""
    try:
        query_embedding = embedding_model.encode(query, convert_to_tensor=False).reshape(1, -1)
        distances, indices = index.search(query_embedding, top_k)
        return [metadata_store[idx] for idx in indices[0] if idx < len(metadata_store)]
    except Exception as e:
        print(f"Error retrieving similar chunks for query '{query}': {e}")
        return []

def generate_response_with_gemini(query):
    """Generate a response using the Gemini API with retrieved information."""
    relevant_chunks = retrieve_similar_chunks(query)
    if not relevant_chunks:
        return "No relevant information found."

    context = "\n".join([chunk['content'] for chunk in relevant_chunks])

    gemini_api_url = "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generate"  # Gemini endpoint

    payload = {
        "prompt": f"Context:\n{context}\n\nQuestion: {query}\nAnswer:",
        "temperature": 0.7,
        "maxOutputTokens": 200
    }

    headers = {
        "Authorization": f"Bearer {gemini_api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(gemini_api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("candidates", [{}])[0].get("output", "No response generated.").strip()
    except requests.exceptions.RequestException as e:
        return f"Error communicating with Gemini API: {e}"

# Flask App
app = Flask(_name_)

@app.route('/')
def home():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query_pipeline():
    """Handle user queries through the RAG pipeline."""
    user_query = request.form.get('query')
    if not user_query:
        return jsonify({'error': 'Query cannot be empty.'}), 400
    
    # Generate response
    answer = generate_response_with_gemini(user_query)
    return jsonify({'query': user_query, 'answer': answer})

if _name_ == '_main_':
    # URLs to process
    urls = [
        "https://www.google.com/",
        "https://www.facebook.com/"
    ]

    # Step 1: Crawl and store data
    process_and_store(urls)

    # Step 2: Start the Flask app
    app.run(debug=True)