import os
import sys
import json
import faiss
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from groq import Groq

# Load environment once at the top
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_rag_response(civilization, book, question):
    # -------- Paths --------
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chunks_path = os.path.join(BASE_PATH, "indexes", civilization, book, "chunks.jsonl")
    index_path = os.path.join(BASE_PATH, "indexes", civilization, book, "faiss.index")

    # -------- Load Chunks --------
    chunks = []
    if not os.path.exists(chunks_path):
        # If the book folder isn't found, we'll still let the AI try to answer generally
        context = "No local documents found for this specific book."
    else:
        with open(chunks_path, "r", encoding="utf-8") as f:
            for line in f:
                chunks.append(json.loads(line))
        
        # -------- Load FAISS & Search --------
        index = faiss.read_index(index_path)
        query_vector = model.encode([question]).astype("float32")
        k = 3
        distances, indices = index.search(query_vector, k)
        retrieved_chunks = [chunks[i] for i in indices[0]]
        context = "\n\n".join([c["text"] for c in retrieved_chunks])

    # -------- NEW HYBRID PROMPT --------
    # This tells the AI to use the context for accuracy, but its own brain for everything else
    prompt = f"""
    You are Artefact, a helpful AI expert in classical literature and general knowledge.

    USER CATEGORY: {civilization}
    USER BOOK: {book}

    INSTRUCTIONS:
    1. If the user is asking about {book} or {civilization}, use the "Context" below to provide a precise, grounded answer. 
    2. If the user misspells something (e.g., 'ramayan' instead of 'ramayana'), understand their intent and answer using the context.
    3. If the user is just saying 'hi', 'hello', or asking a general question NOT related to the books, answer naturally like a normal chatbot. 
    4. Do NOT say "Not found in knowledge base" unless the question is specific to a book and you truly have zero information.

    Context:
    {context}

    Question: {question}
    """

    # -------- Call Groq --------
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are Artefact, a dual-purpose AI: a general assistant and a classical literature expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6 # Increased slightly to make it feel less "robotic"
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        civ = sys.argv[1]
        bk = sys.argv[2]
        qs = " ".join(sys.argv[3:])
        print(get_rag_response(civ, bk, qs))