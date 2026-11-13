# RAG Chatbot

A document-based question-answering chatbot built using FastAPI, Retrieval-Augmented Generation (RAG), Sentence Transformers, ChromaDB, and Groq.

## Features

- Upload PDF documents.
- Extract text from uploaded PDFs.
- Split documents into smaller chunks.
- Generate embeddings using Sentence Transformers.
- Store document chunks in ChromaDB.
- Retrieve relevant information based on user questions.
- Generate answers using the Groq API.

## Technologies Used

- Python
- FastAPI
- Sentence Transformers
- ChromaDB
- LangChain Text Splitters
- PyMuPDF
- Groq API

## Installation

1. Clone the repository:

   git clone https://github.com/srijhakrishnakumar-lgtm/rag_chatbot.git

2. Navigate into the project:

   cd rag_chatbot

3. Create a virtual environment:

   python -m venv venv

4. Activate the virtual environment:

   venv\Scripts\activate

5. Install dependencies:

   pip install -r requirements.txt

6. Create a .env file and add your Groq API key:

   GROQ_API_KEY=your_api_key

## Run the Application

   python -m uvicorn main:app --reload

Open the API documentation:

http://127.0.0.1:8000/docs

## Project Structure

rag_chatbot/
|-- main.py
|-- rag_chatbot/
|   |-- main2.py
|-- requirements.txt
|-- .gitignore
|-- README.md
