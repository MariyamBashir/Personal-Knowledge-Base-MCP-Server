# Personal Knowledge MCP Server

A full-stack personal knowledge-base system that allows users to upload PDF documents, convert their content into semantic embeddings, store them in Qdrant Cloud, and search their knowledge using natural-language queries.

The system provides both a **FastAPI REST API** and a **FastMCP server**, together with a **React/Vite frontend dashboard** for interacting with the knowledge base.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat&logo=vite)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector%20Database-red)
![MCP](https://img.shields.io/badge/MCP-FastMCP-purple)

---

## 🎯 Overview

The Personal Knowledge MCP Server combines document processing, semantic search, vector storage, and MCP integration into a single knowledge-base system.

Users can:

- Upload PDF documents
- Organize documents by subject
- Search their knowledge using natural-language queries
- View semantic search results and similarity scores
- Open complete source documents
- Browse available knowledge sources
- Retrieve documents through MCP tools
- Maintain isolated knowledge spaces using user IDs

The system processes documents through the following pipeline:

``` text 
PDF Document
     ↓
Text Extraction
     ↓
Text Chunking
     ↓
Sentence Transformer Embeddings
     ↓
Qdrant Cloud
     ↓
Semantic Retrieval
     ↓
FastAPI / MCP
     ↓
React Dashboard 
```
---

## 🚀 Features

Document Processing

- PDF upload
- PDF text extraction using PyPDF
- Text chunking
- Subject/category organization
- Automatic document ingestion

## Semantic Search

- Natural-language queries
- Sentence Transformer embeddings
- Semantic similarity search
- Ranked search results
- Similarity scores
- Retrieval of relevant document chunks

## Document Retrieval

- List available sources
- Retrieve complete document context
- Display document metadata
- Display full document content
- Display retrieval chunks

---

## MCP Integration
The project includes a FastMCP server exposing the knowledge base through callable MCP tools:

- ping()
- search_notes()
- get_document()
- list_sources()

## Multi-User Support
Documents are associated with a user_id.

Search and document retrieval operations are filtered by the requesting user's ID, preventing users from accessing documents belonging to another user.

---

## Web Dashboard
The React/Vite frontend provides:

- Dashboard statistics
- API connection status
- Semantic search
- Search result navigation
- Source listing
- Document viewer
- PDF upload
- Automatic source refresh after upload
- Responsive navigation

---

## 💻 Technology Stack

| Component | Technologies |
| :--- | :--- |
| **Backend** | Python, FastAPI, FastMCP, Uvicorn, PyPDF |
| **AI / Vector Store** | Sentence Transformers (384-dimensional embeddings), Qdrant Cloud |
| **Frontend** | React, Vite, JavaScript, CSS, Lucide React |

---

## Embedding Model

The project uses:

all-MiniLM-L6-v2

Embedding dimension:

384

---

## 🛠️ Getting Started

## Prerequisites
Make sure you have installed:

- Python 3.10+
- Node.js
- npm
- A Qdrant Cloud account

  ### 1. Backend Configuration

Navigate to the `backend` directory and initialize the Python environment:

```bash
cd backend
python -m venv .venv
```

# Activate the environment (macOS/Linux)
source .venv/bin/activate
# Activate the environment (Windows PowerShell)
.\.venv\Scripts\Activate

pip install -r requirements.txt

Create a .env file in the backend directory with your Qdrant credentials:

Code snippet
```
- QDRANT_URL=your_qdrant_cluster_url
- QDRANT_API_KEY=your_qdrant_api_key
```
Launch the Services (Run in separate terminal sessions):

# Initialize the FastAPI REST API (Port 8000)
uvicorn app.main:app --reload

# Initialize the MCP Server
python -m app.mcp_server

2. Frontend Configuration

Navigate to the frontend directory to launch the web dashboard:

- cd frontend
- npm install
- npm run dev
The web interface will be accessible at http://localhost:5173.

## 🧪 Testing

## The backend includes test scripts covering:

- Document reading
- Text chunking
- Embedding generation
- Qdrant connection
- Document ingestion
- Retrieval
- Semantic search queries
- Similarity thresholds
- No-match behavior
- MCP tools
- Multi-user isolation
- User ID indexing

## The frontend has been manually tested for:

- API connection
- Dashboard statistics
- Semantic search
- Search results
- Source navigation
- Document viewer
- PDF upload
- Uploaded document retrieval
- Mobile/responsive navigation
- End-to-end document workflow

---

## 🔐 Security

- Qdrant credentials are stored in environment variables.
- .env is excluded from version control.
- Documents are filtered by user_id.
- Cross-user document access is blocked at the retrieval layer. 

For production use, the system should additionally implement:

- User authentication
- Authorization
- Secure user identity management
- Production secrets management
- HTTPS
- Production deployment configuration
- Future Improvements

---

## 🔮 Potential future improvements include:

- User authentication and accounts
- Multiple file formats
- Document deletion
- Document metadata editing
- Pagination for large knowledge bases
- Improved retrieval/ranking strategies
- Production deployment
- AI-generated answers based on retrieved context
- Conversation history
- Advanced document filtering
- More granular permissions

---

## Project Status
Completed

The project currently provides a working end-to-end personal knowledge-base system featuring:

- PDF document ingestion
- Text extraction and chunking
- Semantic embeddings
- Qdrant Cloud vector storage
- Semantic document retrieval
- FastAPI REST API
- FastMCP integration
- MCP tools
- Multi-user document isolation
- React/Vite frontend
- PDF upload
- Source listing
- Full document viewing
- Search result retrieval
- End-to-end testing

---

## Author

**Maryam Bashir**

- **GitHub:** [MariyamBashir](https://github.com/MariyamBashir)
- **LinkedIn:** [Maryam Bashir](https://linkedin.com/in/maryam-bashir-3000542b3)
