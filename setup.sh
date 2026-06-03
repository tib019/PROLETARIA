#!/usr/bin/env bash
set -e
echo "=== PROLETARIA Setup ==="
echo ""
echo "[1/3] Submodule initialisieren..."
git submodule update --init --recursive
echo "[2/3] Python Dependencies..."
pip install -r requirements.txt
echo "[3/3] Ollama prüfen..."
command -v ollama && echo "  ✓ Ollama gefunden — ollama pull mistral" || echo "  ✗ https://ollama.ai installieren"
echo ""
echo "=== Fertig === docker compose up -d"
