# 🏛️ Mythology AI: Retrieval-Augmented Generation (RAG) Agent

An intelligent, source-grounded assistant designed to explore classical literature and ancient epics with zero hallucinations. This project utilizes a **RAG (Retrieval-Augmented Generation)** architecture to ensure that every AI response is backed by actual verses from a verified database of 75,000+ text segments.

---

## 🚀 The Problem: AI Hallucinations
Standard Large Language Models (like ChatGPT) often "hallucinate" or provide factually incorrect details when asked about niche mythological characters or complex ancient themes. They lack a specific "source of truth."

## ✨ Our Solution: The RAG Engine
This project bridges the gap by implementing a **Source-Grounded** mechanism. Instead of relying on general training data, the system:
1. **Retrieves** relevant verses from a custom FAISS Vector Database.
2. **Augments** the AI's prompt with this verified context.
3. **Generates** a response that is 100% factually reliable.

---

## 🛠️ Tech Stack

**Frontend:**
* **React.js & Vite:** For a high-performance, responsive UI.
* **CSS3 (Glassmorphism):** A modern, dark-themed aesthetic.
* **Axios:** For seamless API communication.

**Backend:**
* **Flask:** Python micro-framework for orchestrating the RAG pipeline.
* **FAISS (Facebook AI Similarity Search):** High-speed vector database for semantic search.
* **Sentence-Transformers (`all-MiniLM-L6-v2`):** To convert human language into mathematical vectors.

**AI Model:**
* **Llama 3 (via Groq):** Advanced LLM for natural language synthesis.

---

## 🏗️ System Architecture



1. **User Query:** User asks a question via the React UI.
2. **Embedding:** The Flask backend converts the query into a vector using Sentence-Transformers.
3. **Semantic Search:** FAISS performs a similarity search across 75,000+ mythology segments.
4. **Context Injection:** The most relevant snippets are fed into the Llama-3 prompt.
5. **Grounded Response:** The LLM generates an answer based *only* on the provided context.

---

## 📂 Project Structure

```text
Mythology_RAG/
├── frontend/                # React + Vite Application
│   ├── src/
│   │   ├── App.jsx          # Chat Logic
│   │   └── App.css          # Modern UI Styling
├── backend/                 # Flask Server
│   ├── app.py               # Main Orchestrator
│   ├── faiss_index/         # Vector Database files
│   └── requirements.txt     # Python Dependencies
└── data/                    # Raw Classical Literature (TXT/CSV)
