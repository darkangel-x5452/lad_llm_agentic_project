from sentence_transformers import SentenceTransformer
import faiss
import json

class SemanticMemory:
    def __init__(self, 
                 model_name="all-MiniLM-L6-v2", 
                #  model_name='llama3.2:3b',
                 index_path="memory.index", 
                 meta_path="memory_meta.json"
                 ):
        self.embedder = SentenceTransformer(model_name)
        self.index_path = index_path
        self.meta_path = meta_path

        # Load or initialize
        try:
            self.index = faiss.read_index(index_path)
            with open(meta_path) as f:
                self.meta = json.load(f)
        except:
            self.index = faiss.IndexFlatL2(384)
            self.meta = []

    def add(self, text, metadata=None):
        emb = self.embedder.encode([text])
        self.index.add(emb)
        self.meta.append({"text": text, "metadata": metadata or {}})
        self.save()

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "w") as f:
            json.dump(self.meta, f)

    def query(self, query, top_k=3):
        q_emb = self.embedder.encode([query])
        D, I = self.index.search(q_emb, top_k)
        if len(self.meta) == 0:
            return []
        return [self.meta[i] for i in I[0]]
