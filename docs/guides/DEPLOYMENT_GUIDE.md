# Deployment Guide

---

## Voraussetzungen

| Software | Version | Zweck |
|---------|---------|-------|
| Docker + Docker Compose | ≥ 24.0 | Stack-Orchestrierung |
| Git | ≥ 2.38 | Submodule-Support |
| Ollama | ≥ 0.1.30 | LLM-Inferenz |
| Python | ≥ 3.11 | OPSEC-Module direkt nutzen |
| Node.js | ≥ 20 | verhoer-trainer bauen |

Hardware (Minimum): 16 GB RAM, 50 GB Speicher
Hardware (Empfohlen): 32 GB RAM, NVIDIA GPU ≥ 8 GB VRAM, 100 GB SSD

---

## Schritt-für-Schritt Setup

### 1. Repository klonen

```bash
git clone --recurse-submodules https://github.com/tib019/PROLETARIA
cd PROLETARIA
```

Falls bereits geklont ohne Submodule:
```bash
git submodule update --init --recursive
```

### 2. Umgebungsvariablen konfigurieren

```bash
cp modules/anti-ki/config/.env.example modules/anti-ki/config/.env
```

Mindest-Konfiguration in `.env`:
```env
API_SECRET_KEY=dein_geheimer_schluessel_hier
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=proletaria_2024
OLLAMA_URL=http://ollama:11434
```

### 3. Ollama-Modelle laden

```bash
# Ollama starten (falls nicht als Service)
ollama serve &

# Basis-Modell laden
ollama pull mistral

# Nach ProletariaLLM Fine-Tuning:
# ollama create proletaria-llm -f Modelfile
```

### 4. Docker-Stack starten

```bash
docker compose up -d

# Status prüfen
docker compose ps
docker compose logs -f anti-ki
```

### 5. Services testen

```bash
# ANTI-KI API
curl http://localhost:8000/health

# LLM-Server
curl http://localhost:8001/health

# OSINT-Backend
curl http://localhost:8002/health
```

---

## Services und Ports

| Service | Port | URL |
|---------|------|-----|
| ANTI-KI API | 8000 | http://localhost:8000/docs |
| LLM-Server | 8001 | http://localhost:8001/docs |
| OSINT-Backend | 8002 | http://localhost:8002/docs |
| Neo4j Browser | 7474 | http://localhost:7474 |
| Neo4j Bolt | 7687 | bolt://localhost:7687 |
| Ollama | 11434 | http://localhost:11434 |

---

## Submodule aktualisieren

```bash
# Alle Submodule auf neuesten Stand bringen
git submodule update --remote --merge

# Einzelnes Submodul
git submodule update --remote modules/anti-ki
```

---

## Troubleshooting

### Ollama nicht erreichbar (503)

```bash
# Ollama-Service läuft?
systemctl status ollama
# oder
ollama serve

# Modell geladen?
ollama list
```

### Neo4j startet nicht

```bash
docker compose logs neo4j
# Häufige Ursache: zu wenig Heap-Speicher
# In docker-compose.yml: NEO4J_dbms_memory_heap_max__size=1G (statt 2G)
```

### Submodul-Konflikt

```bash
# Submodul zurücksetzen
git submodule update --init --force modules/anti-ki
```

### OPSEC-Module ImportError

```bash
# Python-Path prüfen
cd PROLETARIA
pip install -r requirements.txt
python -c "from opsec.exposure_scanner import ExposureScanner; print('OK')"
```

---

## Sicherheitshinweise

- **Kein öffentlicher Zugriff**: Alle Services nur auf `localhost` binden (Standard)
- **API-Key ändern**: `API_SECRET_KEY` in `.env` auf starken Wert setzen
- **Neo4j-Passwort**: Standard-Passwort aus `.env` ersetzen
- **Keine Cloud-Backups**: Daten lokal halten, kein automatisches Cloud-Sync
- **Regelmäßige Updates**: `git submodule update --remote` monatlich
