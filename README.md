# 💼 FinCon AI — Financial & Regulatory Intelligence Assistant

**FinCon AI** is a financial research and regulatory intelligence assistant built using a **Hierarchical Hybrid Retrieval-Augmented Generation (RAG)** architecture.

The system is designed to help users analyze financial controlling documentation, accounting standards, regulatory requirements, and corporate policies through context-aware retrieval and grounded AI-generated responses.

It combines semantic search, keyword-based retrieval, hierarchical document indexing, and Cross-Encoder reranking to improve retrieval relevance and provide traceable source references.

**Core domains:** Financial Controlling · IFRS · US GAAP · Regulatory Compliance · Corporate Policies

---

## 🌟 Key Features

### 1. Hierarchical Parent-Child Indexing

A two-level document indexing strategy designed to balance retrieval precision with contextual completeness.

- **Parent Chunks (1,200 characters):** Preserve broader accounting and regulatory context.
- **Child Chunks (300 characters):** Enable more granular semantic and keyword-based matching.
- **Context Expansion:** Retrieved child chunks are mapped back to their parent chunks before generation, providing the LLM with richer context.

### 2. Hybrid Retrieval — Dense + Sparse Search

Combines semantic understanding with exact-term matching.

- **Dense Retrieval — ChromaDB:** Uses `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` to generate multilingual embeddings for semantic similarity search.
- **Sparse Retrieval — BM25:** Uses Elasticsearch as the BM25 search engine, with a local `rank_bm25` fallback for keyword-based retrieval.
- **Reciprocal Rank Fusion (RRF):** Combines dense and sparse retrieval rankings into a unified candidate list.

This approach supports both conceptual financial queries and exact terminology, including `IFRS 16`, `ASC 606`, `DoA`, and `CapEx`.

### 3. Cross-Encoder Reranking

Uses `BAAI/bge-reranker-base` to evaluate retrieved query-document pairs and reorder candidate chunks based on their relevance to the original question.

This refinement step helps reduce irrelevant matches and improve the quality of the final context.

### 4. Grounded Generation & Citation Support

The generation pipeline uses financial-domain prompting and retrieved document context to produce evidence-based responses.

- Context-aware answer generation.
- Source attribution and section-level citation support.
- Reduced reliance on unsupported model knowledge.
- Traceability between generated responses and retrieved documentation.

### 5. RAG Evaluation Suite

Includes an evaluation workflow for assessing retrieval quality against a golden benchmark dataset.

Evaluation focuses on:

- Retrieval Hit Rate.
- Context Recall.
- Benchmark-based retrieval assessment.

---

## 🏗️ System Architecture

```text
                  USER QUERY
                      |
                      v
             QUERY PROCESSING
                      |
              Query Expansion
                      |
          +-----------+-----------+
          |                       |
          v                       v
    DENSE RETRIEVAL         SPARSE RETRIEVAL
      ChromaDB              Elasticsearch
          |                 / rank_bm25
          |                       |
          +-----------+-----------+
                      |
                      v
          RECIPROCAL RANK FUSION
                      |
                      v
             CROSS-ENCODER
                RERANKING
                      |
                      v
             PARENT CONTEXT
               EXPANSION
                      |
                      v
              GROUNDED LLM
                GENERATION
                      |
                      v
           ANSWER + CITATIONS
```

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Vector Database | ChromaDB |
| Embedding Model | Sentence Transformers |
| Sparse Retrieval | Elasticsearch / BM25 |
| Retrieval Fusion | Reciprocal Rank Fusion |
| Reranking | BAAI/bge-reranker-base |
| LLM Integration | Configured LLM Provider |
| Backend API | FastAPI |
| Interactive Interface | Streamlit |
| Evaluation | Custom RAG Evaluation Suite |

---

## 🚀 Quickstart Guide

### Prerequisites

- Python 3.11 recommended.
- Git.
- Access to the configured LLM provider and its API credentials, if required.
- Elasticsearch, if using the Elasticsearch sparse retrieval backend.

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd Milestone1_FinCon_RAG
```

### 2. Create and Activate the Environment

Using Conda:

```bash
conda create -n fincon python=3.11 -y
conda activate fincon
```

Or using Python virtual environments:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and add the configuration required by your LLM provider and other services.

Keep API keys and credentials out of source control.

### 5. Ingest Financial Documents

Place your source documents inside `data/raw/`, then run:

```bash
python -m src.ingestion.run_ingestion
```

This process prepares the document chunks and builds the configured retrieval indexes.

### 6. Launch the FastAPI Backend

```bash
uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload
```

Interactive API documentation:

[http://localhost:8000/docs](http://localhost:8000/docs)

### 7. Launch the Streamlit Interface

Open another terminal, activate the project environment, and run:

```bash
streamlit run ui/streamlit_app.py
```

Open the application at:

[http://localhost:8501](http://localhost:8501)

### 8. Run the RAG Evaluation

```bash
python -m src.evaluation.evaluate_rag
```

---

## 📁 Project Structure

```text
Milestone1_FinCon_RAG/
│
├── data/
│   ├── raw/                      # Source financial documents
│   ├── golden_eval_set.json      # Evaluation benchmark
│   ├── parent_docstore.json      # Hierarchical parent document store
│   └── bm25_index.pkl            # Local BM25 index
│
├── src/
│   ├── config.py                 # Application configuration
│   │
│   ├── ingestion/                # Document loading and indexing
│   │
│   ├── retrieval/                # Hybrid retrieval, RRF and reranking
│   │
│   ├── generation/               # Prompting and RAG generation pipeline
│   │
│   └── evaluation/               # RAG evaluation workflows
│
├── api/
│   └── app.py                    # FastAPI application
│
├── ui/
│   └── streamlit_app.py          # Interactive Streamlit dashboard
│
├── requirements.txt
├── README.md
└── .env                          # Local environment configuration
```

---

## 🔍 Example Research Questions

FinCon AI is designed to support questions such as:

- What are the recognition and measurement requirements under IFRS 16?
- How should revenue recognition be handled under ASC 606?
- What are the disclosure requirements for material cybersecurity incidents under SEC regulations?
- How do financial controlling policies define approval limits and delegation of authority?
- What are the key differences between IFRS and US GAAP for a specific accounting treatment?

---

## 🎯 Project Objectives

- Improve the relevance of financial and regulatory document retrieval.
- Preserve document context through hierarchical indexing.
- Combine semantic and lexical search for more comprehensive retrieval.
- Improve answer grounding through Cross-Encoder reranking.
- Support transparent financial research with source attribution.
- Evaluate retrieval performance using a benchmark-driven approach.

---

## 👨‍💻 Project

**FinCon AI — Financial & Regulatory Intelligence Assistant**

*Milestone 1 | Hierarchical Hybrid RAG System*

Built with Python, ChromaDB, Sentence Transformers, FastAPI, and Streamlit.