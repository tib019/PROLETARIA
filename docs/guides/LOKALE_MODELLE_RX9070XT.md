# Lokale Modelle auf RX 9070 XT (16 GB VRAM, 32 GB RAM)

Stand: 7. November 2026. Grundlage ist das c't-3003-Video vom 06.11.2026 (Transkript auf heise),
gegengeprüft mit Unsloth-Doku, Strata-README und AMD-Specs (Abschnitt „Faktencheck“).
Messwerte sind **nicht** selbst nachgemessen.

## Kurzfassung

| Zweck | Modell | Quant | Wo liegt es | Warum |
|---|---|---|---|---|
| Allround / Analyse (Standard) | Qwen 3.8-27B (dicht) | `UD-Q3_K_XL` (~13,2 GB) | komplett im VRAM | c't-Tipp für 16-GB-Karten, dann bis 128K Kontext; etwas schlechter als Q4 |
| Kurzer Kontext, beste Qualität | Qwen 3.8-27B | `UD-Q4_K_M` | komplett im VRAM | c't hat genau das auf der RX 9070 XT gemessen: 34,4 tok/s, aber nur 8K Kontext, keine Bilderkennung |
| Coding-Agent (OpenCode o. Ä.) | Qwen 3.6-35B-A3B (MoE) | `Q4_K_M` (~24 GB) | ~⅓ der Gewichte im System-RAM | lässt viel VRAM für Kontext frei; Tempo auf der 9070 XT nicht gemessen |
| Experimentell, schnell | Qwen 3.8 Flash Next (125B MoE) | Q2_0 | VRAM + RAM (+ SSD) | Engine **Strata**; Strata nennt für die RX 9070 XT ~60 tok/s; bei 32 GB RAM nur die kleinste „Coder“-Variante |

Grenzen bei 16 GB:

- Langer Kontext frisst VRAM über den KV-Cache. Für Coding-Agenten nennt c't
  mindestens 60K Kontext plus Bilderkennung; mit 24–32 GB passt das bei Q4 „locker“.
  Mit 27B-Q3 nennt c't bis 128K. Läuft der VRAM über, den KV-Cache quantisieren (`q8_0`)
  oder den Kontext senken.
- Q3 kostet messbar Qualität. Wenn Antworten unsauber werden, auf das MoE-Modell
  in Q4_K_M ausweichen.

## AMD-spezifisch: ROCm statt CUDA

Die Docker-Compose-Dateien in `anti-ki` reservieren eine **NVIDIA**-GPU
(`driver: nvidia`), der PROLETARIA-Gesamtstack gar keine. Auf der RX 9070 XT läuft
Ollama dann nur auf der CPU. Lösung:

- Ollama-Image `ollama/ollama:rocm` verwenden
- Geräte `/dev/kfd` und `/dev/dri` in den Container durchreichen
- in `PROLETARIA`, `anti-ki` und `anti-ki/llm_core` liegt dafür jeweils eine `docker-compose.amd.yml`:
  `docker compose -f docker-compose.yml -f docker-compose.amd.yml up -d`

**Prüfen, ob die GPU wirklich rechnet:** `anti-ki/scripts/check_amd_gpu.sh`. Das Skript prüft
Treiber, Image, GPU-Erkennung und `ollama ps` (Anteil GPU/CPU) und misst die Tokens pro Sekunde.
Optionen: `--stack root|core`, `--model`, `--ctx`, `--no-start`, `--container`
(PROLETARIA-Stack: `--no-start --container proletaria-ollama`).

Die RX 9070 XT (RDNA 4, `gfx1201`) wird offiziell erst ab **ROCm 7.2** unterstützt. Erkennt
Ollama die Karte nicht, `HSA_OVERRIDE_GFX_VERSION=12.0.1` setzen.
Ohne Docker geht alternativ llama.cpp mit dem **Vulkan**-Backend. Das braucht kein ROCm
und ist auf RDNA 4 oft genauso schnell.

## Einbindung ins Konglomerat

Alle Module sprechen Ollama an. Das Modell wird per Umgebungsvariable gesetzt:

| Modul | Variable | Default |
|---|---|---|
| `PROLETARIA/llm-server` | `PROLETARIA_MODEL` / `PROLETARIA_FALLBACK_MODEL` | `proletaria-llm` → Ersatz Qwen 3.8-27B |
| `proletaria-llm/inference/chat.py` | `--model` | `proletaria-llm` → Ersatz Qwen 3.8-27B |
| `anti-ki` | `LLM_MODEL` | Qwen 3.8-27B (`llm_core` lädt es automatisch) |
| `proletaria-llm/proletariallm` (CLI) | `PROLETARIA_MODEL` | `proletaria-stub` (Testmodus), Beispiel nutzt Qwen 3.8-27B |

Qwen 3.8-27B steht überall als `hf.co/unsloth/Qwen3.8-27B-GGUF:UD-Q3_K_XL`
(Repo geprüft: 13,15 GB; `:UD-Q4_K_M` = 16,46 GB).

GGUF direkt von Hugging Face in Ollama holen:

```bash
ollama pull hf.co/unsloth/Qwen3.8-27B-GGUF:UD-Q3_K_XL
ollama pull hf.co/unsloth/<Qwen3.6-35B-A3B-Repo>:Q4_K_M   # Repo-Namen vorher prüfen
export LLM_MODEL=hf.co/unsloth/Qwen3.8-27B-GGUF:UD-Q3_K_XL
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

## Faktencheck der c't-Aussagen

| Aussage | Ergebnis |
|---|---|
| Qwen 3.8-27B und Qwen 3.8 Flash Next sind die relevantesten Modelle unter 8000 € | **bestätigt** (wörtlich im Transkript) |
| 16 GB: Qwen 3.8-27B in `UD-Q3_K_XL` | **bestätigt**, ergänzt: dann 128K Kontext; Datei ~13,2 GB |
| 24–32 GB bequem für Coding mit langem Kontext | **sinngemäß bestätigt** (Q4 + Kontext passt „locker“; Agenten brauchen ≥ 60K) |
| RX 9070 XT meistverkaufte Karte, Tipp Qwen 3.6-35B-A3B Q4_K_M mit OpenCode | **nicht prüfbar**: stammt aus dem September-Video, das ich nicht gefunden habe |
| ~35 tok/s auf der RX 9060 XT | **nicht belegt**. Öffentlich gibt es dazu nur Schätzungen. Die einzige c't-Zahl in der Nähe ist 34,4 tok/s auf der **RX 9070 XT** mit 27B UD-Q4_K_M. Möglicherweise wurden die beiden Werte verwechselt |
| RX 9070 XT hat 640 GB/s, doppelt so viel wie die RX 9060 XT | **bestätigt**: 256 Bit × 20 Gbps = 640 GB/s (RX 9060 XT: 128 Bit, 320 GB/s) |
| Strata: min. 12 GB VRAM + 32 GB RAM | **bestätigt, mit Einschränkung**: 32 GB reichen nur für die kleinste „Coder“-Variante, die allgemeinen 2-Bit-Varianten brauchen ~48 GB, 64 GB für alle; ~80 GB freier Plattenplatz |
| Strata nur unter Ubuntu/Nvidia getestet, AMD „soll gehen“ | **überholt**: Strata läuft unter Windows und Linux, die RX 9070 XT steht in der Liste unterstützter Karten (Strata-eigener Benchmark: ~60 tok/s Q2_0) |
| (mein Fehler, korrigiert) ROCm 6.4 reicht | **falsch**: gfx1201 offiziell erst ab ROCm 7.2 |

## Quellen

- heise/c't 3003: „Lokale KI: Das läuft auf deinem Rechner“ (06.11.2026), https://www.heise.de/news/Lokale-KI-Das-laeuft-auf-deinem-Rechner-11515316.html
- heise: „Was ich über lokale KI gelernt habe“
- alpha-digital: „Hardware für lokale KI“ (c't-Messwerte)
- heise: „Strata im Test“
- Unsloth: https://unsloth.ai/docs/models/qwen3.8
- Strata: https://github.com/mach10x/strata
- AMD-Specs RX 9070 XT: https://www.club386.com/amd-reveals-radeon-rx-9070-series-gpu-specs-and-performance-launches-march-6/
- ROCm/RX 9070 XT: https://localaimaster.com/blog/rx-9070-xt-local-ai
