# lad_llm_llama_project

# Setup
## NVIDA and CUDA
- check `nvidia-smi` exists
- Check cuda `ls /dev | grep nvidia`
- Check `nvcc --version`
    -- If not working, still okay.
- check 
```
python3 - <<'EOF'
import torch
print("CUDA available:", torch.cuda.is_available())
print("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None")
EOF
```
- https://docs.nvidia.com/cuda/wsl-user-guide/index.html#nvidia-gpu-computing-on-wsl-2
- https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0&target_type=deb_local

## Ollama
- curl -fsSL https://ollama.com/install.sh | sh
- ollama --version
- ollama run llama3.2:3b
    - background server `http://localhost:11434`
- test prompt `>>> Write a haiku about GPUs`
- Control VRAM usage (important for laptops)
    - OLLAMA_NUM_GPU_LAYERS=20 ollama run llama3.2:3b

## MCP
- `python mcp_tools/weather/weather_mcp_server.py`

## RAG
- `python rag_indexer.py`
- `python rag_mcp_server.py`

### Python
- pip install ollama


# Resources
- https://medium.com/@akankshasinha247/building-multi-agent-architectures-orchestrating-intelligent-agent-systems-46700e50250b
- https://github.com/patchy631/ai-engineering-hub/blob/main/llamaindex-mcp/ollama_client.ipynb