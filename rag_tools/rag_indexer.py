from sentence_transformers import SentenceTransformer
import faiss
import os
import json

MODEL = "all-MiniLM-L6-v2"
DOCS_DIR = "docs"
INDEX_PATH = "vector.index"
META_PATH = "meta.json"

embedder = SentenceTransformer(MODEL)

documents = []
metadata = []

for fname in os.listdir(DOCS_DIR):
    path = os.path.join(DOCS_DIR, fname)
    with open(path) as f:
        text = f.read()

    chunks = [c.strip() for c in text.split("\n") if c.strip()]
    for chunk in chunks:
        documents.append(chunk)
        metadata.append({"source": fname})

embeddings = embedder.encode(documents)

index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(embeddings)

faiss.write_index(index, INDEX_PATH)

with open(META_PATH, "w") as f:
    json.dump(
        [{"text": d, **m} for d, m in zip(documents, metadata)],
        f,
        indent=2
    )

print("Indexed private documents.")
