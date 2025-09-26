## Project Description

This project is a proof-of-concept implementation of Retrieval-Augmented Generation (RAG) with a Large Language Model (LLM). It operates on a collection of research abstracts, enabling semantic search and contextualized question-answering over scientific literature.
The retrieval step is intentionally simple: the system selects the top-5 nearest neighbors directly from the vector store, without rerankers or additional filtering.

## Dataset

This project relies on the **[arXiv Abstracts 2021 dataset](https://huggingface.co/datasets/gfissore/arxiv-abstracts-2021)**, hosted on Hugging Face.

- Contains scientific abstracts from **arXiv** as of 2021  
- Includes metadata such as:  
  - `id` (arXiv identifier)  
  - `title`  
  - `authors`  
  - `categories`  
  - `abstract`  
- Used here as the source collection for semantic search and RAG-based question answering

## Configuration

The project expects a `.env` file in the root directory.  
This file defines all environment variables required by the application.

At minimum, you must set your **OpenAI API key** (`OPENAI_API_KEY`) since the application relies heavily on the OpenAI API.

Example `.env`:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=papers
POSTGRES_HOST=localhost
POSTGRES_CONNECTOR=postgresql+psycopg://postgres:postgres@{HOST}:5432/papers

VECTOR_STORE_COLLECTION_NAME=arxiv_abstracts

OPENAI_API_KEY=your_openai_key

EMBEDDING_MODEL=text-embedding-3-small
RETRIEVER_MODEL=gpt-5-nano
MAIN_MODEL=gpt-5-nano
```

## Installation

### 1. Start Postgres and populate the database

The application uses a standard Postgres instance with the pgvector extension enabled.
Embeddings are stored in a vector column inside Postgres and retrieved via nearest-neighbor search.

Start the database:

```bash 
docker compose up -d pgvector
```


Run the setup scripts (requires dependencies to be installed):

```
uv sync --frozen

# Download the dataset
uv run download_abstracts.py

# Generate embeddings and insert them into Postgres
uv run db_init.py
```

### 2. Launch the FastAPI application
```
docker compose up -d --build fastapi
```
The service will then be available at http://localhost:8000.


