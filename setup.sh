#!/usr/bin/env bash
set -e
echo "=== PROLETARIA Setup ==="
echo ""
echo "[1/3] Submodule initialisieren..."
git submodule update --init --recursive
echo "[2/3] Python Dependencies..."
pip install -r requirements.txt
echo "[3/3] Ollama prüfen..."
command -v ollama && echo "  ✓ Ollama gefunden — ollama pull hf.co/unsloth/Qwen3.8-27B-GGUF:UD-Q3_K_XL" || echo "  ✗ https://ollama.ai installieren"
echo ""
echo "=== Fertig === docker compose up -d"
