
# Personal Knowledge MCP Server

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)](https://reactjs.org/)

An enterprise-ready, full-stack knowledge base system designed to ingest PDF documents, generate semantic embeddings, and facilitate natural-language querying. The system exposes its capabilities via a REST API and a Model Context Protocol (MCP) server, allowing seamless integration with modern LLM workflows.

---

## 🎯 System Overview

*   **Semantic Search Engine:** Utilizes Sentence Transformers (`all-MiniLM-L6-v2`) and Qdrant Cloud vector database for high-accuracy contextual retrieval.
*   **Model Context Protocol (MCP):** Native FastMCP integration exposes internal knowledge stores directly to AI agents.
*   **Multi-Tenant Architecture:** Implements strict user-level data isolation to ensure secure and partitioned document management.
*   **Modern Frontend Dashboard:** A responsive React/Vite web interface for document ingestion and metadata visualization.

---

## 💻 Technology Stack

| Component | Technologies |
| :--- | :--- |
| **Backend** | Python, FastAPI, FastMCP, Uvicorn, PyPDF |
| **AI / Vector Store** | Sentence Transformers (384-dimensional embeddings), Qdrant Cloud |
| **Frontend** | React, Vite, JavaScript, CSS, Lucide React |

---

## 🚀 Getting Started

### 1. Backend Configuration

Navigate to the `backend` directory and initialize the Python environment:

```bash
cd backend
python -m venv .venv

# Activate the environment (macOS/Linux)
source .venv/bin/activate
# Activate the environment (Windows PowerShell)
.\.venv\Scripts\Activate

pip install -r requirements.txt

Create a .env file in the backend directory with your Qdrant credentials:

Code snippet

QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key

Launch the Services (Run in separate terminal sessions):

# Initialize the FastAPI REST API (Port 8000)
uvicorn app.main:app --reload

# Initialize the MCP Server
python -m app.mcp_server

2. Frontend Configuration

Navigate to the frontend directory to launch the web dashboard:

cd frontend
npm install
npm run dev
The web interface will be accessible at http://localhost:5173.

MCP Server Tools

The integrated FastMCP server exposes the following functions to connected LLM clients:

search_notes(query: str, top_k: int = 5): Executes semantic search over the user's vector data.

get_document(doc_id: str): Retrieves the raw source text for a specified document ID.

list_sources(): Outputs an index of all available documents in the knowledge base.

ping(): Diagnostics tool to verify MCP server health and connection status.

🔒 Security & Data Isolation

This system is built with strict user-level data isolation. All system requests (both REST and MCP) require a valid user_id parameter. This architecture guarantees that users can only upload, query, and retrieve documents within their designated partition, preventing unauthorized cross-tenant data access.

🚀 Project Status
Completed

The project currently provides a working personal knowledge-base system with:

Semantic document retrieval
MCP tools
FastAPI API
Qdrant vector storage
Multi-user isolation
React/Vite frontend
PDF upload
Document viewing
Source listing
End-to-end tested workflow

The project is ready for demonstration.