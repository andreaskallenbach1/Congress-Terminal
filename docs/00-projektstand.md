# Projektstand und Details (ausgelagert aus CLAUDE.md)

Ausgelagert am 18.10.2026 (Andreas' Entscheidung): CLAUDE.md wird in jeden Agenten eines Laufs und bei jedem seiner
Schritte mitgeladen. Was der Lauf nicht braucht, steht hier. Inhalt unverändert übernommen; CLAUDE.md verweist hierher.

## Technik und Werkzeuge (vollständige Fassung)

- **Web-App:** statische PWA, gehostet über GitHub Pages aus diesem Repository; installierbar über Edge/Chrome.
- **Daten:** Briefings als Dateien im Repository (ein Briefing pro Tag + Archiv).
- **Läufe** schreiben Briefings fest auf `main`; eine GitHub Action baut und veröffentlicht die Seite. Der Routine-Endpunkt erlaubt keine Browser-Aufrufe (CORS-Vorabfrage → 405), daher der Weg über GitHub.
- **Phase-3-Maßnahmen (17.10.2026):** 40 Minuten sind Obergrenze; im Lauf nur GitHub plus die Recherche-Konnektoren (Tabelle unten); Statusdatei je Lauf; Kernaussagen (8–12 je Story) doppelt prüfen; Abrufe drosseln und zwischenspeichern; stufenweise bauen und testen, Betrieb mit voller Pipeline.
- **Git:** Entwicklung auf dem zugewiesenen `claude/…`-Branch; keine Pull Requests ohne Andreas' Auftrag.
- **Quellentest:** `./scripts/check_sources.sh` vor Änderungen an der Pipeline und bei Verdacht auf Ausfälle.
- **Design-Skills im Repository** (`.claude/skills/`, geprüft, Lizenzen beigelegt): `impeccable` (Apache-2.0, Design-Prozess und Detektor gegen KI-Standardoptik), `frontend-design` (Anthropic), `ui-ux-pro-max` (MIT, Paletten- und Schriftdatenbank). Produktwahrheit für das Design: `PRODUCT.md`.
- **Skills und Plugins** (nur geprüfte Herkunft, z. B. Anthropic-Verzeichnis):
  `frontend-design` (Oberfläche), `webapp-testing` (Playwright-Tests, Chromium ist vorinstalliert),
  Design-Plugin mit `design-critique` und `accessibility-review` (Phase 3), `skill-creator` (eigene Skills
  für Rubrik, Faktenprüfung, Story-Format), `dataviz` (Diagramme), `deep-research` (Vorbild für Sammler).
  Keine Skills aus ungeprüften Sammelportalen.
- **Verbrauch und Token-Sparen (Pro-Abo):** 25 Rollen. Hebel: Code statt KI für Fleißarbeit · Modell je Aufgabe (klein: Türsteher, Faktenkarten, Sammler, Verfahren · mittel: Story-Builder, Relevanz, Gegenagent, Historiker, Prüfer B, Neutralität · groß: Schiedsrichter, Redakteure, Prüfer A, Chefredaktion) · Türsteher · Faktenkarten · nur das Neue · Regeln als Skills. **Keine** gebündelte Prüfung: jede Kernaussage wird einzeln geprüft (Andreas' Entscheidung).
- **Web-App-Funktionen (zusätzlich):** Vorlesen je Story und ganze Ausgabe (Stimme, Stand 17.10.2026: Favoriten **Google Chirp 3 HD „Iapetus“ und „Algenib“**, en-US; im Gratiskontingent von 1 Mio. Zeichen/Monat, Code stoppt bei 950.000 Zeichen, Erzeugung per API-Schlüssel in der GitHub Action, keine Claude-Tokens. Browser-Stimmen und Kokoro getestet und abgelehnt. Umsetzung später, blockiert den Bau nicht); Seiten Members und Committees; Benachrichtigung bei fertigem Update (kleiner Code, keine Tokens; Variante noch offen); Archiv speichert Storys einzeln, gruppiert nach Ausgabe; Suche clientseitig (Pagefind).
- **Konnektoren (Entscheidung 17.10.2026, getestet 17.10.2026):** Andreas verbindet sie unter claude.ai/customize/connectors; wirksam erst in einer neu gestarteten Sitzung bzw. im Lauf, wenn sie in der Routine ausgewählt sind. Praxistest:
  | Konnektor | Test | Rolle im Lauf |
  |---|---|---|
  | Parallel Search | ✅ liefert aktuelle Treffer inkl. CRS, Congress.gov, Abgeordneten-Pressemitteilungen | Sammler, Nachsuche (R2) |
  | Tavily | ✅ Nachrichten der letzten Woche mit Datum | Gegenagent 3b (eigener Quellenpool) |
  | CourtListener | ✅ Urteile bis 15.10.2026 | Executive & Courts |
  | USAFacts | ✅ 24 Behördenquellen, u. a. Congress.gov, FEC, Treasury, USAspending | Zahlen für Haushalt/Midterms, nur mit `_citation` |
  | Firecrawl | ✅ erreichbar; Seiten-Zusammenfassung war unbrauchbar und aus dem Cache → nur Markdown-Abruf mit `maxAge: 0` nutzen | Volltexte langer Primärquellen (Faktenkarten) |
  | Gov Relations | ✅ Lobbying-Meldungen je Gesetz (LDA-Daten) – von Andreas zusätzlich verbunden | Hintergrund „wer lobbyiert“ |
  | Unsplash | ✅ Fotosuche funktioniert (nachverbunden 17.10.2026) | Ersatzbilder |
  Konnektoren liefern Orientierung und Rohmaterial; Fakten weiterhin nur aus Primärquellen (Abschnitt 6). Keine Konnektoren mit persönlichen Daten (Gmail, Kalender, Drive, Gamma …) im Lauf.

## Projektdokumente

- Design-Leinwand (Runden 1–6, maßgeblich: Runde 6 „Federal Program, Feinschliff“ und „Sources“): https://claude.ai/artifact/YWnrQiqgwwCvrWXq7vCYh9
- Phase 3 – Kritische Prüfung (Befunde, Risikomatrix, Maßnahmen): https://claude.ai/code/artifact/1d03596c-3b3d-4af4-aedb-016de20be5c1
- **Gesamtbild v3 (aktueller Stand, maßgeblich):** https://claude.ai/code/artifact/4b7c08a1-9c52-4214-bcba-0fceb432797d
- Projektbild v2 (Vorgänger, mit Rückschleifen und Quellenstatus): https://claude.ai/code/artifact/aceb575b-e2b3-4556-8ca1-9444a4d9e085
- Architektur & Feintuning v1 (Entscheidungsgrundlage): https://claude.ai/code/artifact/aa180f36-b7f0-473c-9946-088917b173ef
- `docs/01-quellen-und-architektur.md` – erster Quellenkatalog (teilweise überholt durch Projektbild v2)
- `scripts/check_sources.sh` – Praxistest aller Quellen

## Offene Punkte

- YouTube-Kanäle der Ausschüsse (SFRC, HFAC, SASC, HASC) finden; bis dahin Videos über Ausschuss-Websites
- Washington Post war beim Test nicht erreichbar (Serverfehler) – erneut prüfen
- YouTube-Feeds und Federal-Register-API fielen am 18.10.2026 um 06:00 UTC kurz aus (404/403), um 15:20 UTC liefen alle wieder → kein Adressproblem; `collect.py` versucht ausgefallene Quellen jetzt nach 45 s ein zweites Mal
- Verbrauch eines Laufs im Abo messen – erster Lauf 17.10.2026: Pro-Sitzungslimit in Stufe 4 erreicht (`docs/05-erster-lauf.md`); Sparmaßnahmen umgesetzt (Redakteure mittleres Modell außer Leitartikel, Seiten-Speicher, Faktenkarten, Code-Vorprüfung, Code-Zusammenbau, Türsteher auf Schlagzeilen), gemessen im zweiten Lauf (`docs/08-zweiter-lauf.md`), Optimierungen danach in `docs/09-optimierung-nach-lauf-2.md`
- FEC/GovInfo-Schlüssel (api.data.gov) als Network secret hinterlegt, wird aber als ungültig abgelehnt (18.10.2026) – Andreas prüft den Wert
- Federal Register: Volltexte über GovInfo (amtliche GPO-Ausgabe), nicht über federalregister.gov
- Federal Register sperrte am 17.10.2026 nach mehreren Volltext-Abrufen diese IP („Your IP address has been blocked“): Abrufe drosseln, Volltexte nur einzeln und zwischengespeichert holen
- Design (17.10.2026): „Federal Program“; Kopf = rundes Siegel mit Plenarsaal-Emblem neben zentriertem Caslon-Namen „The Congress Terminal“ (`design/brand/`); Reihenfolge unter dem Leitartikel: Floor & Committees, Midterms (mit Karte), Foreign Policy Desk (mit Karte). Endgültige Freigabe durch Andreas steht aus.
