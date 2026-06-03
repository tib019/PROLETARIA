"""
SurveillanceDB — Wissensbasis bekannter Überwachungsakteure und -systeme

Katalogisiert staatliche und kommerzielle Überwachungsinfrastruktur,
um Organisationen bei der Risikoeinschätzung zu unterstützen.

Quellen: Netzpolitik.org, EDRi, Privacy International, Statewatch,
         Bundestag-Anfragen (Kleine Anfragen), EuGH/BVerfG-Entscheidungen
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


class ActorType(str, Enum):
    BEHOERDE        = "behoerde"       # BKA, LKA, Verfassungsschutz
    KOMMERZIELL     = "kommerziell"    # Palantir, Clearview, NSO
    NACHRICHTENDIENST = "nd"           # BND, CIA-Kooperationen
    POLIZEI         = "polizei"
    JUSTIZ          = "justiz"         # Staatsanwaltschaft


class ThreatLevel(str, Enum):
    KRITISCH = "kritisch"   # aktiv einsetzbar gegen linke Orgas
    HOCH     = "hoch"       # nachgewiesener Einsatz gegen Aktivismus
    MITTEL   = "mittel"     # bekannt, Einsatz unklar
    NIEDRIG  = "niedrig"    # theoretisch möglich
    INFO     = "info"       # reine Dokumentation


@dataclass
class SurveillanceActor:
    id: str
    name: str
    actor_type: ActorType
    threat_level: ThreatLevel
    country: str
    description: str
    capabilities: list[str] = field(default_factory=list)
    known_targets: list[str] = field(default_factory=list)   # Kategorien, keine Personen
    legal_basis: list[str] = field(default_factory=list)
    counter_measures: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    last_updated: str = field(default_factory=lambda: datetime.utcnow().date().isoformat())


class SurveillanceDB:
    """
    Lokale Wissensbasis über Überwachungsinfrastruktur.
    Wird genutzt für:
    - Kontextanreicherung in der ANTI-KI Narrativanalyse
    - OPSEC-Risikoeinschätzung
    - Automatische DSGVO-Anfragen-Generierung gegen bekannte Akteure
    """

    def __init__(self, db_path: str = "data/surveillance_actors.json"):
        self.db_path = Path(db_path)
        self._actors: dict[str, SurveillanceActor] = {}
        self._load_builtins()
        self._load_custom()

    # ------------------------------------------------------------------
    # Query API
    # ------------------------------------------------------------------

    def get(self, actor_id: str) -> Optional[SurveillanceActor]:
        return self._actors.get(actor_id)

    def search(
        self,
        country: Optional[str] = None,
        actor_type: Optional[ActorType] = None,
        min_threat: Optional[ThreatLevel] = None,
        capability: Optional[str] = None,
    ) -> list[SurveillanceActor]:
        level_order = ["info", "niedrig", "mittel", "hoch", "kritisch"]
        results = list(self._actors.values())

        if country:
            results = [a for a in results if a.country.lower() == country.lower()]
        if actor_type:
            results = [a for a in results if a.actor_type == actor_type]
        if min_threat:
            min_idx = level_order.index(min_threat)
            results = [a for a in results if level_order.index(a.threat_level) >= min_idx]
        if capability:
            cap_lower = capability.lower()
            results = [a for a in results if any(cap_lower in c.lower() for c in a.capabilities)]

        return sorted(results, key=lambda a: level_order.index(a.threat_level), reverse=True)

    def get_countermeasures(self, actor_id: str) -> list[str]:
        actor = self._actors.get(actor_id)
        return actor.counter_measures if actor else []

    def add_actor(self, actor: SurveillanceActor):
        self._actors[actor.id] = actor
        self._save_custom()

    def summary(self) -> dict:
        by_type: dict[str, int] = {}
        by_threat: dict[str, int] = {}
        by_country: dict[str, int] = {}
        for a in self._actors.values():
            by_type[a.actor_type] = by_type.get(a.actor_type, 0) + 1
            by_threat[a.threat_level] = by_threat.get(a.threat_level, 0) + 1
            by_country[a.country] = by_country.get(a.country, 0) + 1
        return {
            "total": len(self._actors),
            "by_type": by_type,
            "by_threat": by_threat,
            "by_country": by_country,
        }

    # ------------------------------------------------------------------
    # Built-in knowledge base
    # ------------------------------------------------------------------

    def _load_builtins(self):
        builtins = [
            SurveillanceActor(
                id="palantir_gotham",
                name="Palantir Gotham",
                actor_type=ActorType.KOMMERZIELL,
                threat_level=ThreatLevel.KRITISCH,
                country="USA",
                description=(
                    "Datenintegrations- und Analyseplattform, eingesetzt bei BKA, mehreren "
                    "deutschen Landespolizeien, Militär und Geheimdiensten. Ermöglicht "
                    "massenhafte Verknüpfung von Personendaten aus heterogenen Quellen."
                ),
                capabilities=[
                    "Massenverknüpfung strukturierter und unstrukturierter Daten",
                    "Personennetzwerk-Analyse",
                    "Prädiktive Polizeiarbeit",
                    "Geolokalisierung",
                    "Social-Media-Monitoring",
                    "Import von Telekommunikationsdaten",
                ],
                known_targets=["Linksextremismus-Fälle LKA", "Klimaaktivismus", "Migrantenorganisationen"],
                legal_basis=["§ 9a BKAG (Datenanalyse)", "Landespolizeigesetze"],
                counter_measures=[
                    "Minimierung digitaler Spuren",
                    "Verschlüsselte Kommunikation (Signal, Matrix)",
                    "Keine realen Namen in Aktivismussystemen",
                    "Regelmäßige Selbst-OSINT-Audits",
                    "DSGVO Art. 15 Auskunftsanfragen an BKA/LKA",
                ],
                sources=[
                    "Kleine Anfrage BT-Drs. 19/30750",
                    "Netzpolitik.org: Palantir bei deutschen Behörden",
                    "EDRi: Law enforcement data sharing",
                ],
            ),
            SurveillanceActor(
                id="clearview_ai",
                name="Clearview AI",
                actor_type=ActorType.KOMMERZIELL,
                threat_level=ThreatLevel.KRITISCH,
                country="USA",
                description=(
                    "Gesichtserkennung mit >30 Mrd. Bildern aus öffentlichen Quellen. "
                    "In Europa für staatliche Nutzung verboten (CNIL, GPA), "
                    "trotzdem Behördenanfragen dokumentiert."
                ),
                capabilities=[
                    "Gesichtserkennung",
                    "Rückwärtssuche anhand Fotos",
                    "Verknüpfung mit Social-Media-Profilen",
                    "Echtzeit-Identifikation auf Demonstrationen",
                ],
                known_targets=["Demonstrierende", "Aktivisten", "Geflüchtete"],
                legal_basis=["Umstritten — DSGVO-Verstoß festgestellt durch CNIL, ICO, GPA"],
                counter_measures=[
                    "Gesichtsverhüllung auf Demonstrationen",
                    "DSGVO Art. 17 Löschungsantrag (Clearview hat EU-Vertreter)",
                    "Brillen/Make-up gegen Gesichtserkennung",
                    "Keine Fotos von Aktivisten ohne Einwilligung veröffentlichen",
                ],
                sources=[
                    "CNIL Clearview-Entscheidung 2022",
                    "BayLDA Verfahren 2023",
                    "Privacy International Reports",
                ],
            ),
            SurveillanceActor(
                id="bka_hessendata",
                name="Hessen Data / ViVA (BKA)",
                actor_type=ActorType.BEHOERDE,
                threat_level=ThreatLevel.HOCH,
                country="Deutschland",
                description=(
                    "Vorgangsbearbeitungs- und Analysesystem der Polizeibehörden. "
                    "Verknüpfung von Ermittlungsvorgängen, Kontaktpersonen, "
                    "Fahrzeughaltern, Telekommunikation."
                ),
                capabilities=[
                    "Personenverknüpfung",
                    "Fahrzeugüberwachung (Kennzeichenleser KESY)",
                    "Kontopfändung",
                    "Ausschreibung zur Beobachtung",
                ],
                known_targets=["§ 129-Verfahren (Linke Gruppen)", "Klimaaktivismus", "Anti-AKW"],
                legal_basis=["BKAG", "StPO", "Landespolizeigesetze"],
                counter_measures=[
                    "Auskunftsrecht §19 BDSG nutzen",
                    "Anwaltliche Überprüfung von Verfassungsschutz-Dateien",
                    "Kein Fahrzeug auf eigene Namen bei Demonstrationen",
                    "Kollektive Strafverteidigungsstrukturen",
                ],
                sources=[
                    "Grundrechtekomitee: Polizeidatenbanken",
                    "BT-Drs. zu INPOL-Speicherung",
                ],
            ),
            SurveillanceActor(
                id="nso_pegasus",
                name="NSO Group / Pegasus",
                actor_type=ActorType.KOMMERZIELL,
                threat_level=ThreatLevel.KRITISCH,
                country="Israel",
                description=(
                    "Zero-Click-Spyware, die vollständige Gerätekontrolle ermöglicht. "
                    "Nachgewiesener Einsatz gegen Journalisten und Aktivisten weltweit. "
                    "In Deutschland durch BKA lizensiert (FINFISHER-Nachfolger)."
                ),
                capabilities=[
                    "Zero-Click-Exploit (kein Nutzerinteraktion notwendig)",
                    "Vollständiger Gerätezugriff",
                    "Kamera und Mikrofon aktivieren",
                    "Verschlüsselte Kommunikation mitlesen",
                    "Standortverfolgung",
                ],
                known_targets=["Menschenrechtler", "Journalisten", "Oppositionelle"],
                legal_basis=["§ 49 StPO Quellen-TKÜ (Deutschland)"],
                counter_measures=[
                    "GrapheneOS statt Android/iOS für Hochrisiko-Personen",
                    "Separates Gerät für sensitive Aktivitäten",
                    "Regelmäßige Gerätewartung durch technisch kompetente Personen",
                    "Mobile Verification Toolkit (MVT) zur Infektionsprüfung",
                    "Verzicht auf Smartphones bei kritischen Treffen",
                ],
                sources=[
                    "Citizen Lab: Pegasus Project",
                    "Amnesty International Tech Lab",
                    "BT-Drs. 20/1865 zu BKA Spyware",
                ],
            ),
            SurveillanceActor(
                id="fog_data_science",
                name="Fog Data Science",
                actor_type=ActorType.KOMMERZIELL,
                threat_level=ThreatLevel.HOCH,
                country="USA",
                description=(
                    "Datenhändler der Mobilgerätedaten aus App-Tracking-Ökosystem kauft "
                    "und an Strafverfolgungsbehörden verkauft. Erlaubt Standortverfolgung "
                    "ohne richterlichen Beschluss."
                ),
                capabilities=[
                    "Massenhafte Geolokalisierung via Ad-Tech",
                    "Pseudonyme Geräteverfolgung über Monate",
                    "Identifikation von Personengruppen an Orten",
                ],
                known_targets=["Demonstrierende (Dokumentiert: BLM-Proteste USA)", "Grenzgebiete"],
                legal_basis=["Kein Beschluss erforderlich — kommerzielle Daten"],
                counter_measures=[
                    "Werbeverfolgung im Gerät deaktivieren",
                    "Apps mit Privacy-Fokus (kein Google/Meta SDK)",
                    "Flugzeugmodus auf Demonstrationen",
                    "IMSI-Catcher-Detektion (SnoopSnitch)",
                ],
                sources=[
                    "EFF: Government Purchase of Mobility Data",
                    "Protocol: Fog Data Science Investigation",
                ],
            ),
            SurveillanceActor(
                id="verfassungsschutz_de",
                name="Bundesamt für Verfassungsschutz (BfV)",
                actor_type=ActorType.NACHRICHTENDIENST,
                threat_level=ThreatLevel.HOCH,
                country="Deutschland",
                description=(
                    "Inlandsgeheimdienst mit Beobachtungsauftrag für als extremistisch "
                    "eingestufte Gruppen. Führt geheime Dateien, nutzt V-Männer, "
                    "kooperiert mit ausländischen Diensten."
                ),
                capabilities=[
                    "V-Mann-Einsatz (HUMINT)",
                    "Observationen",
                    "Kommunikationsüberwachung mit G10-Genehmigung",
                    "Geheime Dateisysteme (Amtsdateien §17 BVerfSchG)",
                    "Zusammenarbeit mit EUROPOL, NSA",
                ],
                known_targets=["Linke Gruppen", "Anarchismus", "Klimaaktivismus (teils)", "DKP"],
                legal_basis=["BVerfSchG", "G10-Gesetz", "BNDG-Kooperationen"],
                counter_measures=[
                    "Konspirationsregeln für sensitive Aktivitäten",
                    "Auskunftsanfrage §15 BVerfSchG",
                    "Rechtliche Überprüfung der Beobachtung (BVerwG-Klage)",
                    "Akzeptanz dass Versammlungen ggf. observiert werden",
                    "Trennung zwischen öffentlicher und interner Kommunikation",
                ],
                sources=[
                    "BVerfSchG",
                    "Statewatch: German Intelligence Reports",
                    "Rote Hilfe: Materialien zu VS-Beobachtung",
                ],
            ),
        ]

        for actor in builtins:
            self._actors[actor.id] = actor

    # ------------------------------------------------------------------
    # Persistence for custom additions
    # ------------------------------------------------------------------

    def _load_custom(self):
        if not self.db_path.exists():
            return
        try:
            data = json.loads(self.db_path.read_text())
            for item in data:
                actor = SurveillanceActor(**{
                    k: v for k, v in item.items()
                    if k not in ("actor_type", "threat_level")
                })
                actor.actor_type = ActorType(item["actor_type"])
                actor.threat_level = ThreatLevel(item["threat_level"])
                self._actors[actor.id] = actor
        except Exception:
            pass

    def _save_custom(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        # Only save non-builtin actors
        builtin_ids = {
            "palantir_gotham", "clearview_ai", "bka_hessendata",
            "nso_pegasus", "fog_data_science", "verfassungsschutz_de",
        }
        custom = [
            {
                "id": a.id, "name": a.name, "actor_type": a.actor_type,
                "threat_level": a.threat_level, "country": a.country,
                "description": a.description, "capabilities": a.capabilities,
                "known_targets": a.known_targets, "legal_basis": a.legal_basis,
                "counter_measures": a.counter_measures, "sources": a.sources,
                "last_updated": a.last_updated,
            }
            for a in self._actors.values() if a.id not in builtin_ids
        ]
        self.db_path.write_text(json.dumps(custom, indent=2, ensure_ascii=False))
