"""
serve.py — FastAPI-Server für ProletariaLLM

Stellt ProletariaLLM als REST API bereit, die von ANTI-KI und anderen
Konglomerat-Komponenten genutzt werden kann.

Start: uvicorn inference.serve:app --port 8001 --reload
Docs:  http://localhost:8001/docs

Alle Anfragen werden lokal verarbeitet — kein externer API-Aufruf.
"""
from __future__ import annotations

import json
import time
import os
from typing import Optional

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

OLLAMA_URL   = os.getenv("OLLAMA_URL", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("PROLETARIA_MODEL", "proletaria-llm")
FALLBACK_MODEL = "mistral"

app = FastAPI(
    title="ProletariaLLM API",
    description="Lokales politisches Sprachmodell — datenschutzkonform, kein Cloud-Logging",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = """Du bist ProletariaLLM — ein politisch informiertes Sprachmodell
für linke Organisationen. Du analysierst Texte aus einer kritisch-materialistischen
Perspektive, kennst die Geschichte der Arbeiterbewegung und hilfst bei:
- Politischer Textanalyse und Narrativerkennung
- Vorbereitung auf rechtliche Situationen (Auskunftsrechte, Schweigerecht)
- Verständnis von Überwachungstechnologien und -strukturen
- Formulierung von DSGVO-Anfragen und rechtlichen Schreiben

Du gibst keine Anweisungen für illegale Aktivitäten.
Du arbeitest lokal — alle Gespräche sind privat."""


# ── Schemas ───────────────────────────────────────────────────────────────────

class GenerateRequest(BaseModel):
    prompt: str
    system: Optional[str] = None
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1024
    stream: bool = False


class ChatMessage(BaseModel):
    role: str   # "user" | "assistant" | "system"
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2048


class AnalyzeRequest(BaseModel):
    text: str
    task: str = "narrative"  # "narrative" | "legal" | "opsec" | "free"
    context: str = ""


# ── Helpers ───────────────────────────────────────────────────────────────────

def _active_model() -> str:
    """Wählt verfügbares Modell."""
    try:
        resp = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        if resp.ok:
            names = [m["name"] for m in resp.json().get("models", [])]
            if any(DEFAULT_MODEL in n for n in names):
                return DEFAULT_MODEL
            if any(FALLBACK_MODEL in n for n in names):
                return FALLBACK_MODEL
    except Exception:
        pass
    return DEFAULT_MODEL


def _ollama_generate(prompt: str, system: str, model: str, temperature: float, max_tokens: int) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "system": system,
        "stream": False,
        "options": {"temperature": temperature, "num_predict": max_tokens},
    }
    try:
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json().get("response", "")
    except requests.exceptions.ConnectionError:
        raise HTTPException(503, "Ollama nicht erreichbar. Bitte 'ollama serve' starten.")
    except requests.exceptions.Timeout:
        raise HTTPException(504, "Ollama-Anfrage Timeout. Modell lädt möglicherweise noch.")


def _ollama_chat(messages: list[dict], model: str, temperature: float, max_tokens: int) -> str:
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature, "num_predict": max_tokens},
    }
    try:
        resp = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json().get("message", {}).get("content", "")
    except requests.exceptions.ConnectionError:
        raise HTTPException(503, "Ollama nicht erreichbar.")


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    try:
        resp = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        ollama_ok = resp.ok
        models = [m["name"] for m in resp.json().get("models", [])] if ollama_ok else []
    except Exception:
        ollama_ok = False
        models = []

    return {
        "status": "ok" if ollama_ok else "degraded",
        "ollama_reachable": ollama_ok,
        "active_model": _active_model(),
        "available_models": models,
        "timestamp": time.time(),
    }


@app.post("/generate")
def generate(req: GenerateRequest):
    """Einfache Text-Generierung."""
    model = req.model or _active_model()
    system = req.system or SYSTEM_PROMPT
    response = _ollama_generate(req.prompt, system, model, req.temperature, req.max_tokens)
    return {
        "response": response,
        "model": model,
        "prompt_length": len(req.prompt),
    }


@app.post("/chat")
def chat(req: ChatRequest):
    """Multi-Turn Konversation."""
    model = req.model or _active_model()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += [{"role": m.role, "content": m.content} for m in req.messages]

    response = _ollama_chat(messages, model, req.temperature, req.max_tokens)
    return {
        "response": response,
        "model": model,
        "turn_count": len(req.messages),
    }


@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    """Spezialisierte politische Textanalyse."""
    task_prompts = {
        "narrative": (
            "Analysiere den folgenden Text auf:\n"
            "1. Dominante Narrative und Frames\n"
            "2. Politische Verortung des Textes\n"
            "3. Rhetorische Strategien\n"
            "4. Mögliche Gegennarrative\n\n"
            "Antworte strukturiert auf Deutsch.\n\nText:\n"
        ),
        "legal": (
            "Analysiere den folgenden Text aus rechtlicher Perspektive:\n"
            "1. Relevante Rechtsgrundlagen (DE/EU)\n"
            "2. Relevante Datenschutzrechte (DSGVO)\n"
            "3. Handlungsempfehlungen\n"
            "4. Mögliche rechtliche Risiken\n\nText:\n"
        ),
        "opsec": (
            "Analysiere den folgenden Text auf OPSEC-Relevanz:\n"
            "1. Welche sensiblen Informationen sind enthalten?\n"
            "2. Welche Metadaten könnten abgeleitet werden?\n"
            "3. Welche OPSEC-Maßnahmen werden empfohlen?\n\nText:\n"
        ),
        "free": "",
    }

    prefix = task_prompts.get(req.task, task_prompts["free"])
    context_block = f"\nKontext: {req.context}\n" if req.context else ""
    full_prompt = prefix + context_block + req.text

    model = _active_model()
    response = _ollama_generate(full_prompt, SYSTEM_PROMPT, model, 0.5, 2048)

    return {
        "analysis": response,
        "task": req.task,
        "model": model,
        "text_length": len(req.text),
    }


@app.get("/models")
def list_models():
    """Listet verfügbare Ollama-Modelle."""
    try:
        resp = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        raise HTTPException(503, f"Ollama nicht erreichbar: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("inference.serve:app", host="0.0.0.0", port=8001, reload=True)
