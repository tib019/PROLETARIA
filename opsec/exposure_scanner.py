"""
ExposureScanner — erkennt digitale Spuren einer Organisation oder Person
in öffentlich zugänglichen Quellen (OSINT-defensiv).

Keine aktiven Angriffe. Kein Zugriff auf private Systeme.
Nur Auswertung öffentlicher Daten zur Bedrohungsbewertung.
"""
from __future__ import annotations

import re
import json
import hashlib
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ExposureFinding:
    source: str          # e.g. "github", "pastebin", "whois", "shodan_public"
    severity: str        # "critical" | "high" | "medium" | "low" | "info"
    category: str        # "pii", "credential", "infrastructure", "metadata"
    description: str
    raw_snippet: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "severity": self.severity,
            "category": self.category,
            "description": self.description,
            "raw_snippet": self.raw_snippet[:200],
            "timestamp": self.timestamp.isoformat(),
        }


class ExposureScanner:
    """
    Scannt öffentliche Quellen auf Spuren einer Entität.

    Einsatz:
    - Selbst-Audit vor öffentlichen Aktionen
    - Überprüfung ob Kommunikationsinfrastruktur kompromittiert wurde
    - Einschätzung der eigenen Sichtbarkeit für staatliche Akteure
    """

    # Muster, die auf kompromittierte OPSEC hinweisen
    CREDENTIAL_PATTERNS = [
        r"(?i)password\s*[=:]\s*\S+",
        r"(?i)api[_-]?key\s*[=:]\s*\S+",
        r"(?i)token\s*[=:]\s*[A-Za-z0-9_\-\.]{20,}",
        r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----",
    ]

    EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
    IP_PATTERN    = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_url = ollama_url
        self._findings: list[ExposureFinding] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def scan_text(self, text: str, source: str = "manual") -> list[ExposureFinding]:
        """Scannt beliebigen Text auf OPSEC-Lücken."""
        findings: list[ExposureFinding] = []

        findings += self._check_credentials(text, source)
        findings += self._check_pii(text, source)
        findings += self._check_infrastructure(text, source)

        self._findings.extend(findings)
        return findings

    def scan_file_metadata(self, filepath: str) -> list[ExposureFinding]:
        """
        Prüft Datei-Metadaten auf eingebettete Informationen
        (Autor, GPS-Koordinaten in EXIF, Software-Version etc.).
        """
        import os
        findings: list[ExposureFinding] = []

        try:
            stat = os.stat(filepath)
            if stat.st_size > 50 * 1024 * 1024:
                findings.append(ExposureFinding(
                    source="file_metadata",
                    severity="info",
                    category="metadata",
                    description=f"Große Datei ({stat.st_size // 1024} KB) — Inhalt prüfen",
                ))

            # EXIF für Bilder
            if filepath.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff')):
                findings += self._check_exif(filepath)

            # Office-Dokumente
            if filepath.lower().endswith(('.docx', '.xlsx', '.pptx', '.odt')):
                findings += self._check_office_metadata(filepath)

        except (OSError, PermissionError) as e:
            logger.warning("Metadaten-Scan fehlgeschlagen: %s", e)

        self._findings.extend(findings)
        return findings

    def assess_risk(self) -> dict:
        """Aggregiertes Risikoprofil aller Findings."""
        severity_weights = {"critical": 10, "high": 5, "medium": 2, "low": 1, "info": 0}
        score = sum(severity_weights.get(f.severity, 0) for f in self._findings)

        return {
            "total_findings": len(self._findings),
            "risk_score": score,
            "risk_level": self._score_to_level(score),
            "by_severity": self._count_by_severity(),
            "by_category": self._count_by_category(),
            "findings": [f.to_dict() for f in self._findings],
            "timestamp": datetime.utcnow().isoformat(),
        }

    def clear(self):
        self._findings.clear()

    # ------------------------------------------------------------------
    # Internal checks
    # ------------------------------------------------------------------

    def _check_credentials(self, text: str, source: str) -> list[ExposureFinding]:
        findings = []
        for pattern in self.CREDENTIAL_PATTERNS:
            for match in re.finditer(pattern, text):
                findings.append(ExposureFinding(
                    source=source,
                    severity="critical",
                    category="credential",
                    description="Mögliche Zugangsdaten im Klartext gefunden",
                    raw_snippet=match.group()[:80],
                ))
        return findings

    def _check_pii(self, text: str, source: str) -> list[ExposureFinding]:
        findings = []
        emails = self.EMAIL_PATTERN.findall(text)
        for email in set(emails):
            findings.append(ExposureFinding(
                source=source,
                severity="medium",
                category="pii",
                description=f"E-Mail-Adresse gefunden: {self._redact(email)}",
                raw_snippet=email,
            ))
        return findings

    def _check_infrastructure(self, text: str, source: str) -> list[ExposureFinding]:
        findings = []
        ips = self.IP_PATTERN.findall(text)
        private_ranges = [("10.", "high"), ("192.168.", "high"), ("172.", "medium")]
        for ip in set(ips):
            for prefix, severity in private_ranges:
                if ip.startswith(prefix):
                    findings.append(ExposureFinding(
                        source=source,
                        severity=severity,
                        category="infrastructure",
                        description=f"Private IP-Adresse öffentlich sichtbar: {ip}",
                        raw_snippet=ip,
                    ))
        return findings

    def _check_exif(self, filepath: str) -> list[ExposureFinding]:
        findings = []
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS
            img = Image.open(filepath)
            exif = img._getexif()
            if exif:
                for tag_id, value in exif.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag in ("GPSInfo", "GPS"):
                        findings.append(ExposureFinding(
                            source="exif",
                            severity="high",
                            category="pii",
                            description="GPS-Koordinaten in Bilddatei",
                            raw_snippet=str(value)[:80],
                        ))
                    elif tag in ("Artist", "Author", "Copyright", "CameraOwnerName"):
                        findings.append(ExposureFinding(
                            source="exif",
                            severity="medium",
                            category="pii",
                            description=f"Persönlicher Metadatenwert: {tag}",
                            raw_snippet=str(value)[:80],
                        ))
        except Exception:
            pass
        return findings

    def _check_office_metadata(self, filepath: str) -> list[ExposureFinding]:
        findings = []
        try:
            import zipfile
            import xml.etree.ElementTree as ET
            with zipfile.ZipFile(filepath) as z:
                for name in ("docProps/core.xml", "docProps/app.xml"):
                    if name in z.namelist():
                        xml = z.read(name).decode("utf-8", errors="replace")
                        root = ET.fromstring(xml)
                        for child in root.iter():
                            if child.text and child.text.strip():
                                tag = child.tag.split("}")[-1]
                                if tag in ("creator", "lastModifiedBy", "company"):
                                    findings.append(ExposureFinding(
                                        source="office_metadata",
                                        severity="medium",
                                        category="pii",
                                        description=f"Büro-Metadatum '{tag}' enthält Wert",
                                        raw_snippet=child.text[:80],
                                    ))
        except Exception:
            pass
        return findings

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _redact(value: str) -> str:
        h = hashlib.sha256(value.encode()).hexdigest()[:8]
        return f"[REDACTED:{h}]"

    @staticmethod
    def _score_to_level(score: int) -> str:
        if score >= 20:
            return "KRITISCH"
        if score >= 10:
            return "HOCH"
        if score >= 4:
            return "MITTEL"
        if score >= 1:
            return "NIEDRIG"
        return "SAUBER"

    def _count_by_severity(self) -> dict:
        counts: dict[str, int] = {}
        for f in self._findings:
            counts[f.severity] = counts.get(f.severity, 0) + 1
        return counts

    def _count_by_category(self) -> dict:
        counts: dict[str, int] = {}
        for f in self._findings:
            counts[f.category] = counts.get(f.category, 0) + 1
        return counts
