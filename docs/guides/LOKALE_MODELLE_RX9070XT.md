# Lokale Modelle auf RX 9070 XT (16 GB VRAM, 32 GB RAM)

Stand: November 2026. Grundlage sind c't/heise-Empfehlungen (Quellen unten).
Modellnamen und Messwerte stammen von dort und sind **nicht** selbst nachgemessen.
Vor dem Download die exakten Repo-Namen auf Hugging Face prüfen.

## Kurzfassung

| Zweck | Modell | Quant | Wo liegt es | Warum |
|---|---|---|---|---|
| Allround / Analyse (Standard) | Qwen 3.8-27B (dicht) | `UD-Q3_K_XL` | komplett im VRAM | c't-Tipp für 16-GB-Karten; Q3 macht 27B auf 16 GB möglich |
| Coding-Agent (OpenCode o. Ä.) | Qwen 3.6-35B-A3B (MoE) | `Q4_K_M` | Experten teils im System-RAM | c't: ~35 tok/s auf RX 9060 XT; die 9070 XT hat mit 640 GB/s die doppelte Bandbreite |
| Experimentell, schnell | Qwen 3.8 Flash Next | – | VRAM + RAM | mit der Engine **Strata** (min. 12 GB VRAM + 32 GB RAM), getestet unter Ubuntu |

Grenzen bei 16 GB:

- Langer Kontext frisst VRAM über den KV-Cache. Für ernsthaftes Coding mit langem
  Kontext nennt c't 24–32 GB als bequeme Klasse. Mit 27B-Q3 den Kontext eher
  auf 16k–32k begrenzen und den KV-Cache quantisieren (`q8_0`).
- Q3 kostet messbar Qualität. Wenn Antworten unsauber werden, auf das MoE-Modell
  in Q4_K_M ausweichen.

## AMD-spezifisch: ROCm statt CUDA

Die Docker-Compose-Dateien in `anti-ki` reservieren eine **NVIDIA**-GPU
(`driver: nvidia`). Auf der RX 9070 XT greift das nicht, Ollama läuft dann nur auf
der CPU. Lösung:

- Ollama-Image `ollama/ollama:rocm` verwenden
- Geräte `/dev/kfd` und `/dev/dri` in den Container durchreichen
- in `anti-ki` dafür: `docker compose -f docker-compose.yml -f docker-compose.amd.yml up -d`

Die RX 9070 XT (RDNA 4, `gfx1201`) braucht einen aktuellen ROCm-Treiber (6.4 oder neuer).
Ohne Docker geht alternativ llama.cpp mit dem **Vulkan**-Backend. Das braucht kein ROCm
und ist auf RDNA 4 oft genauso schnell.

## Einbindung ins Konglomerat

Alle Module sprechen Ollama an. Das Modell wird per Umgebungsvariable gesetzt:

| Modul | Variable | aktueller Default |
|---|---|---|
| `PROLETARIA/llm-server` | `PROLETARIA_MODEL` | `proletaria-llm` → Fallback `mistral` |
| `anti-ki` | `LLM_MODEL` | `mistral` |
| `proletaria-llm/proletariallm` (CLI) | `PROLETARIA_MODEL` | `qwen2.5-coder:7b` |

GGUF direkt von Hugging Face in Ollama holen (Platzhalter `<repo>` durch das echte
Unsloth-GGUF-Repo ersetzen):

```bash
ollama pull hf.co/<repo>:UD-Q3_K_XL     # Qwen 3.8-27B
ollama pull hf.co/<repo>:Q4_K_M         # Qwen 3.6-35B-A3B
export LLM_MODEL=hf.co/<repo>:UD-Q3_K_XL
```

Für MoE-Modelle mit llama.cpp die Experten in den RAM legen und den Rest auf die GPU:

```bash
llama-server -m qwen3.6-35b-a3b-Q4_K_M.gguf -ngl 99 --n-cpu-moe 20 -c 32768 \
  --cache-type-k q8_0 --cache-type-v q8_0
```

`--n-cpu-moe` so weit senken, bis der VRAM voll ist.

## Training (proletaria-llm)

`training/finetune_qlora.py` und `requirements_train.txt` setzen CUDA und NVIDIA
voraus (bitsandbytes). Auf der RX 9070 XT nur unter Linux mit ROCm-PyTorch und
ROCm-fähigem bitsandbytes. Deshalb der Ubuntu-Dual-Boot. Unter Windows ist
QLoRA-Training auf AMD praktisch nicht nutzbar.

## Quellen

- heise: „Lokale KI: Das läuft auf deinem Rechner“
- heise: „Was ich über lokale KI gelernt habe“
- alpha-digital: „Hardware für lokale KI“ (c't-Messwerte)
- heise: „Strata im Test“
