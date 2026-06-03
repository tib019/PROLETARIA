# ADR-001: Monorepo mit Git-Submodulen

**Status:** Akzeptiert  
**Datum:** 2026-06  
**Autor:** Tobias Buß

---

## Kontext

PROLETARIA verbindet fünf eigenständige Repositories zu einem Konglomerat.
Drei Strategien wurden erwogen:

1. **Vollständiges Monorepo** — Alle fünf Repos in ein einziges zusammenführen
2. **Git-Submodule** — PROLETARIA als Dach-Repo, alte Repos als Submodule
3. **Lose Referenzen** — Nur Dokumentation + Links, kein technischer Zusammenhang

## Entscheidung

**Git-Submodule** (Option 2) mit direktem Code in PROLETARIA für neue Module.

## Begründung

| Kriterium | Monorepo | Submodule | Lose Refs |
|-----------|----------|-----------|-----------|
| Alte Repos unverändert | ✗ | ✅ | ✅ |
| Einheitlicher Stack-Start | ✅ | ✅ | ✗ |
| Unabhängige Weiterentwicklung | ✗ | ✅ | ✅ |
| Cybersyn akademisch isoliert | ✗ | ✅ | ✅ |
| Technische Integration | ✅ | ✅ | ✗ |

**Cybersyn 2.0** ist ein akademisches Forschungsprojekt das nicht verändert
werden darf — es als Submodul einzubinden ermöglicht Referenzierung ohne Eingriff.

Die neuen Module (`opsec/`, `verhoer-trainer/`, `llm-server/`) die Repos
übergreifend verbinden, leben direkt in PROLETARIA.

## Konsequenzen

- `git clone --recurse-submodules` erforderlich für vollständige Installation
- Submodul-Updates via `git submodule update --remote`
- Jeder alte Repo kann unabhängig weiterentwickelt werden
- PROLETARIA verweist immer auf einen spezifischen Commit der Submodule (kein automatisches Tracking)
