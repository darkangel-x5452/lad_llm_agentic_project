from mcp.server.fastmcp import FastMCP
import faiss, json
from sentence_transformers import SentenceTransformer

INDEX_PATH = "vector.index"
META_PATH = "meta.json"

index = faiss.read_index(INDEX_PATH)
with open(META_PATH) as f:
    docs = json.load(f)

embedder = SentenceTransformer("all-MiniLM-L6-v2")

mcp = FastMCP(
    name="Private RAG MCP",
    host="0.0.0.0",
    port=4444,
)

@mcp.tool()
def retrieve_private_docs(query: str, top_k: int = 3) -> list:
    """
    Retrieve relevant private document passages.
    Returns list of text + source metadata.
    """
    q_emb = embedder.encode([query])
    _, idxs = index.search(q_emb, top_k)

    results = []
    for i in idxs[0]:
        results.append(docs[i])

    return results

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
