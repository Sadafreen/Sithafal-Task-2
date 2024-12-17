# Sithafal-Task2
Here is a `README.md` file for your project:

```markdown
# Flask-based RAG (Retrieval-Augmented Generation) System

This project implements a Retrieval-Augmented Generation (RAG) pipeline using Flask, Sentence Transformers, FAISS, and Gemini API. The goal of the system is to crawl, scrape, and process textual content from websites, store embeddings in a vector index, and retrieve relevant information in response to user queries, generating an answer using the Gemini API.

## Features
- **Web Crawling and Scraping:** Extracts textual content from webpages.
- **Text Embeddings:** Uses the SentenceTransformer model to convert text into embeddings.
- **FAISS Vector Index:** Stores and retrieves text embeddings efficiently.
- **Gemini API Integration:** Generates answers to user queries by passing retrieved information to the Gemini API.
- **Flask Web Application:** Provides a user-friendly interface to interact with the system.

## Requirements

- Python 3.7+
- Install the required packages using `pip`:

```bash
pip install -r requirements.txt
```

### Required Packages

- `requests`: To make HTTP requests for crawling and interacting with APIs.
- `beautifulsoup4`: For scraping content from webpages.
- `flask`: A web framework for building the application.
- `sentence-transformers`: For generating text embeddings.
- `faiss-cpu`: For storing and retrieving embeddings using FAISS.
- `transformers`: For interacting with the Gemini API.

## Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create `.env` file

You need to create a `.env` file in the root directory of the project to store your **Gemini API Key**:

```
GEMINI_API_KEY=your_api_key_here
```

## Usage

### Step 1: Crawl and Process Websites

The `process_and_store(urls)` function crawls and scrapes the provided URLs, extracts the text, generates embeddings, and stores them in a FAISS vector index for fast retrieval.

You can modify the `urls` list in the `app.py` file to include the URLs you want to crawl.

### Step 2: Run the Flask App

Run the Flask application to start the web server:

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000/`.

### Step 3: Query the System

Once the server is running, you can send POST requests to `/query` with the `query` parameter to get answers.

Example cURL request:

```bash
curl -X POST -d "query=What is FAISS?" http://127.0.0.1:5000/query
```

You will receive a JSON response with the query and the generated answer.

### Step 4: Handle Errors

If a required package is missing or there is an error while processing, the system will provide appropriate error messages.

## File Structure

```
.
├── app.py                 # Flask app for handling web requests
├── requirements.txt       # List of required Python packages
├── templates
│   └── index.html         # The homepage HTML template
└── .env                   # Environment variables file (for API keys)
```

## Troubleshooting

1. **Missing Dependencies:**
   - If you encounter missing dependencies, run:
     ```bash
     pip install -r requirements.txt
     ```

2. **Gemini API Issues:**
   - Make sure your Gemini API key is correctly set in the `.env` file.

3. **FAISS or SentenceTransformer Errors:**
   - Ensure you have installed the correct versions of `faiss-cpu` and `sentence-transformers`.

## Contributing

Feel free to fork the repository and submit issues or pull requests. Please ensure that your contributions adhere to the project's coding standards.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```

This `README.md` provides an overview of your project, installation instructions, usage guidelines, and basic troubleshooting. It can be further expanded with additional sections as needed.
