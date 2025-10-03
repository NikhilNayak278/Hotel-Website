# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import chromadb
import subprocess
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or your site URL
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to Chroma
chroma_client = chromadb.PersistentClient(path="./my_chroma_store")
collection = chroma_client.get_collection("docs")

class Query(BaseModel):
    query: str

@app.post("/rag")
def rag(query: Query):
    # Step 1: Embed user query
    q_emb = embed_model.encode([query.query]).tolist()
    
    # Step 2: Retrieve top 3 docs
    results = collection.query(query_embeddings=q_emb, n_results=3)
    context = " ".join([doc for doc in results["documents"][0]])
    
    # Step 3: Call Ollama
    prompt = f"Context:\n{context}\n\nQuestion: {query.query}\nAnswer:"
    result = subprocess.run(
        ["ollama", "run", "llama2"],
        input=prompt.encode(),
        capture_output=True
    )
    answer = result.stdout.decode().strip()

    return {"answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)