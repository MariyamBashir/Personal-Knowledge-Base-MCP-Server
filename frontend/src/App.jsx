import {
  BookOpen,
  FileText,
  Search,
  Database,
  Activity,
  ChevronRight,
  Menu,
  X,
  ArrowUpRight,
} from "lucide-react";

import { useEffect, useState } from "react";
import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000";

function App() {
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [apiOnline, setApiOnline] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Search state
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [searchLoading, setSearchLoading] = useState(false);
  const [searchPerformed, setSearchPerformed] = useState(false);
  const [searchError, setSearchError] = useState("");

  const [selectedDocument, setSelectedDocument] = useState(null);
  const [documentLoading, setDocumentLoading] = useState(false);
  const [documentError, setDocumentError] = useState("");

  useEffect(() => {
    fetchSources();
  }, []);

  async function fetchSources() {
    try {
      const response = await fetch(`${API_BASE_URL}/sources`);

      if (!response.ok) {
        throw new Error("Failed to fetch sources");
      }

      const data = await response.json();

      setSources(data.sources || []);
      setApiOnline(true);
    } catch (error) {
      console.error("API error:", error);
      setApiOnline(false);
    } finally {
      setLoading(false);
    }
  }

  async function handleSearch() {
    const query = searchQuery.trim();

    if (!query) {
      return;
    }

    setSearchLoading(true);
    setSearchError("");
    setSearchPerformed(true);

    try {
      const response = await fetch(
        `${API_BASE_URL}/search?query=${encodeURIComponent(query)}&top_k=5`
      );

      if (!response.ok) {
        throw new Error("Search request failed");
      }

      const data = await response.json();

      setSearchResults(data.results || []);
      setApiOnline(true);
    } catch (error) {
      console.error("Search error:", error);
      setSearchResults([]);
      setSearchError(
        "Unable to perform the search. Please make sure the backend is running."
      );
      setApiOnline(false);
    } finally {
      setSearchLoading(false);
    }
  }

  function handleSearchKeyDown(event) {
    if (event.key === "Enter") {
      handleSearch();
    }
  }

  async function openDocument(docId) {
  setDocumentLoading(true);
  setDocumentError("");
  setSelectedDocument(null);

  try {
    const response = await fetch(
      `${API_BASE_URL}/documents/${encodeURIComponent(docId)}`
    );

    if (!response.ok) {
      throw new Error("Failed to fetch document");
    }

    const data = await response.json();

    if (!data.found) {
      throw new Error("Document not found");
    }

    setSelectedDocument(data);
    setApiOnline(true);
  } catch (error) {
    console.error("Document error:", error);
    setDocumentError(
      "Unable to load this document. Please try again."
    );
  } finally {
    setDocumentLoading(false);
  }
}

  const subjects = [...new Set(sources.map((source) => source.subject))];

  return (
    <div className="app">

      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="sidebar-overlay"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`sidebar ${sidebarOpen ? "sidebar-open" : ""}`}>

        <div className="sidebar-header">
          <div className="brand-icon">
            <BookOpen size={22} />
          </div>

          <div className="brand-text">
            <h2>Knowledge Base</h2>
            <span>MCP Server</span>
          </div>

          <button
            className="mobile-close"
            onClick={() => setSidebarOpen(false)}
          >
            <X size={20} />
          </button>
        </div>

        <nav className="navigation">

          <div className="nav-section-title">
            WORKSPACE
          </div>

          <button className="nav-item active">
            <BookOpen size={19} />
            <span>Dashboard</span>
          </button>

          <button className="nav-item">
            <Search size={19} />
            <span>Search</span>
          </button>

          <button className="nav-item">
            <Database size={19} />
            <span>Sources</span>
          </button>

        </nav>

        <div className="sidebar-bottom">
          <div className="server-status">
            <span
              className={`status-dot ${
                apiOnline ? "online" : "offline"
              }`}
            />

            <div>
              <strong>
                {apiOnline ? "API Online" : "API Offline"}
              </strong>

              <span>
                {apiOnline
                  ? "Connected to backend"
                  : "Unable to connect"}
              </span>
            </div>
          </div>
        </div>

      </aside>

      {/* Main */}
      <main className="main">

        {/* Top bar */}
        <header className="topbar">

          <button
            className="mobile-menu"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu size={22} />
          </button>

          <div className="breadcrumb">
            <span>Workspace</span>
            <ChevronRight size={15} />
            <strong>Dashboard</strong>
          </div>

          <div className="connection-status">
            <Activity size={17} />

            <span>
              {apiOnline ? "Connected" : "Disconnected"}
            </span>
          </div>

        </header>

        {/* Content */}
        <div className="content">

          {/* Hero */}
          <section className="hero">

            <div>
              <div className="eyebrow">
                <span className="eyebrow-dot" />
                PERSONAL KNOWLEDGE SYSTEM
              </div>

              <h1>
                Your knowledge,
                <br />
                <span>organized intelligently.</span>
              </h1>

              <p>
                Search, explore, and retrieve information from
                your personal documents using semantic search.
              </p>
            </div>

          </section>

          {/* Stats */}
          <section className="stats-grid">

            <div className="stat-card">
              <div className="stat-icon purple">
                <FileText size={21} />
              </div>

              <div>
                <span className="stat-label">
                  Documents
                </span>

                <strong>
                  {loading ? "—" : sources.length}
                </strong>

                <small>
                  Available sources
                </small>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon blue">
                <Database size={21} />
              </div>

              <div>
                <span className="stat-label">
                  Subjects
                </span>

                <strong>
                  {loading ? "—" : subjects.length}
                </strong>

                <small>
                  Knowledge categories
                </small>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon green">
                <Activity size={21} />
              </div>

              <div>
                <span className="stat-label">
                  System
                </span>

                <strong>
                  {apiOnline ? "Ready" : "Offline"}
                </strong>

                <small>
                  Backend connection
                </small>
              </div>
            </div>

          </section>

          {/* Search */}
          <section className="search-section">

            <div className="section-heading">
              <div>
                <h2>Search your knowledge</h2>

                <p>
                  Ask a question and find the most relevant
                  information from your documents.
                </p>
              </div>
            </div>

            <div className="search-box">

              <Search size={21} />

              <input
                type="text"
                value={searchQuery}
                onChange={(event) => setSearchQuery(event.target.value)}
                onKeyDown={handleSearchKeyDown}
                placeholder="Ask something about your documents..."
              />

              <button
                onClick={handleSearch}
                disabled={searchLoading || !searchQuery.trim()}
              >
                {searchLoading ? "Searching..." : "Search"}
              </button>

            </div>

            {/* Search error */}
            {searchError && (
              <div className="search-error">
                {searchError}
              </div>
            )}

            {/* Search results */}
            {searchPerformed && (
              <div className="results-section">

                <div className="results-header">
                  <div>
                    <h3>Search results</h3>

                    <p>
                      {searchLoading
                        ? "Searching your knowledge base..."
                        : `${searchResults.length} relevant result${
                            searchResults.length === 1 ? "" : "s"
                          } found`}
                    </p>
                  </div>
                </div>

                {searchLoading ? (
                  <div className="loading">
                    Searching your knowledge base...
                  </div>
                ) : searchResults.length === 0 ? (
                  <div className="empty-state">
                    <Search size={30} />
                    <p>No relevant information found.</p>
                    <span>
                      Try asking your question in a different way.
                    </span>
                  </div>
                ) : (
                  <div className="results-list">

                    {searchResults.map((result) => (

                      <div
                        className="result-card"
                        key={`${result.doc_id}-${result.chunk}-${result.rank}`}
                      >

                        <div className="result-main">

                          <div className="result-icon">
                            <FileText size={19} />
                          </div>

                          <div className="result-content">

                            <div className="result-title-row">

                              <div>
                                <h4>
                                  {result.source}
                                </h4>

                                <div className="result-meta">
                                  <span>
                                    {result.subject}
                                  </span>

                                  <span>•</span>

                                  <span>
                                    Page {result.page}
                                  </span>

                                  <span>•</span>

                                  <span>
                                    Chunk {result.chunk}
                                  </span>
                                </div>
                              </div>

                              <div className="match-score">
                                {(result.score * 100).toFixed(2)}%
                                <small>match</small>
                              </div>

                            </div>

                            <p className="result-text">
                              {result.text}
                            </p>

                            <div className="result-footer">

                              <span>
                                Rank #{result.rank}
                              </span>

                              <button onClick={() => openDocument(result.doc_id)}>
                                View source
                                <ArrowUpRight size={14} />
                              </button>

                            </div>

                          </div>

                        </div>

                      </div>

                    ))}

                  </div>
                )}

              </div>
            )}

          </section>

          {/* Sources */}
          <section className="sources-section">

            <div className="section-heading">

              <div>
                <h2>Your sources</h2>

                <p>
                  Documents currently stored in your
                  personal knowledge base.
                </p>
              </div>

              <button className="view-all">
                View all
                <ChevronRight size={16} />
              </button>

            </div>

            {loading ? (
              <div className="loading">
                Loading sources...
              </div>
            ) : sources.length === 0 ? (
              <div className="empty-state">
                <FileText size={30} />
                <p>No documents found.</p>
              </div>
            ) : (
              <div className="source-grid">

                {sources.map((source) => (

                  <div
                    className="source-card"
                    key={source.doc_id}
                    onClick={() => openDocument(source.doc_id)}
                  >

                    <div className="source-top">

                      <div className="file-icon">
                        <FileText size={19} />
                      </div>

                      <span className="subject-badge">
                        {source.subject}
                      </span>

                    </div>

                    <h3>
                      {source.filename}
                    </h3>

                    <p>
                      Document ID: {source.doc_id}
                    </p>

                    <div className="source-footer">
                      <span>Knowledge source</span>
                      <ChevronRight size={16} />
                    </div>

                  </div>

                ))}

              </div>
            )}

          </section>

        </div>

            </main>

      {/* Document Viewer */}
      {(selectedDocument || documentLoading || documentError) && (
        <div
          className="document-overlay"
          onClick={() => {
            if (!documentLoading) {
              setSelectedDocument(null);
              setDocumentError("");
            }
          }}
        >
          <div
            className="document-modal"
            onClick={(event) => event.stopPropagation()}
          >

            {/* Modal Header */}
            <div className="document-header">

              <div className="document-heading">

                <div className="document-file-icon">
                  <FileText size={20} />
                </div>

                <div>
                  <h2>
                    {selectedDocument?.filename || "Loading document..."}
                  </h2>

                  {selectedDocument && (
                    <div className="document-meta">
                      <span>{selectedDocument.subject}</span>
                      <span>•</span>
                      <span>ID: {selectedDocument.doc_id}</span>
                    </div>
                  )}
                </div>

              </div>

              <button
                className="document-close"
                onClick={() => {
                  setSelectedDocument(null);
                  setDocumentError("");
                }}
                disabled={documentLoading}
              >
                <X size={20} />
              </button>

            </div>

            {/* Modal Body */}
            <div className="document-body">

              {documentLoading && (
                <div className="document-loading">
                  <div className="loading-spinner" />

                  <h3>Loading document</h3>

                  <p>
                    Retrieving the complete document from your
                    knowledge base...
                  </p>
                </div>
              )}

              {documentError && (
                <div className="document-error">
                  <FileText size={28} />

                  <h3>Unable to load document</h3>

                  <p>{documentError}</p>
                </div>
              )}

              {selectedDocument && !documentLoading && !documentError && (
                <>
                  {/* Document information */}
                  <div className="document-info-grid">

                    <div className="document-info-card">
                      <span>Document ID</span>
                      <strong>{selectedDocument.doc_id}</strong>
                    </div>

                    <div className="document-info-card">
                      <span>Subject</span>
                      <strong>{selectedDocument.subject}</strong>
                    </div>

                    <div className="document-info-card">
                      <span>Total chunks</span>
                      <strong>{selectedDocument.total_chunks}</strong>
                    </div>

                  </div>

                  {/* Content */}
                  <div className="document-content">

                    <div className="document-content-heading">
                      <div>
                        <span>DOCUMENT CONTENT</span>
                        <h3>Full source context</h3>
                      </div>
                    </div>

                    <div className="document-text">
                      {selectedDocument.content}
                    </div>

                  </div>

                  {/* Chunks */}
                  {selectedDocument.chunks?.length > 0 && (
                    <div className="document-chunks">

                      <div className="document-content-heading">
                        <div>
                          <span>RETRIEVAL CONTEXT</span>
                          <h3>
                            {selectedDocument.chunks.length}{" "}
                            {selectedDocument.chunks.length === 1
                              ? "chunk"
                              : "chunks"}
                          </h3>
                        </div>
                      </div>

                      {selectedDocument.chunks.map((chunk) => (
                        <div
                          className="chunk-card"
                          key={`${chunk.filename}-${chunk.chunk_index}`}
                        >

                          <div className="chunk-header">
                            <span>
                              Page {chunk.page_number}
                            </span>

                            <span>
                              Chunk {chunk.chunk_index}
                            </span>
                          </div>

                          <p>
                            {chunk.text}
                          </p>

                        </div>
                      ))}

                    </div>
                  )}

                </>
              )}

            </div>

          </div>
        </div>
      )}

    </div>
  );
}

export default App;