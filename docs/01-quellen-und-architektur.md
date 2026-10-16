# Congress Terminal – Schritt 1: Quellen & Agenten-Architektur

Stand: 16.10.2026 · Status: Entwurf zur gemeinsamen Prüfung

## Festgelegte Entscheidungen

| Thema | Entscheidung |
|---|---|
| Form | Installierbare Web-App (PWA), Zielplattform zunächst Windows; Handy später |
| Automatik | Variante A: geplante Claude-Aufgabe, jeden Morgen, mit Agenten/Sub-Agenten |
| Sprache der Inhalte | Englisch |
| Interessenprofil | Kein fester Regionen-Filter; Relevanz richtet sich nach dem Tagesgeschehen. Außenpolitik ist eigene Säule. Midterms 2026 sind eigenes Modul. |
| Umfang | Briefing für ca. 40 Minuten, gestaffelt – man muss nicht alles lesen, aber alles Wichtige ist da |
| Skills/Plugins | Anthropic-Verzeichnis + geprüfte, vertrauenswürdige Drittquellen |

---

## 1. Blocker: Netzwerkzugang der Cloud-Umgebung

Praxistest am 16.10.2026: **Alle** getesteten Quellen wurden vom Netzwerk-Proxy dieser Cloud-Umgebung
mit `403` abgewiesen (u. a. `api.congress.gov`, `www.senate.gov`, `feeds.npr.org`, `www.c-span.org`).
Nur die eingebaute Websuche funktioniert – und die lieferte für „diese Woche im Kongress“ nur veraltete
Treffer. **Websuche allein reicht also nicht**, die Agenten brauchen direkten Zugriff auf Feeds und APIs.

Da die tägliche Aufgabe in derselben Umgebung läuft, muss der Netzwerkzugang erweitert werden.
Empfehlung: Stufe **Full** – die Agenten folgen Links zu vielen wechselnden Nachrichtenseiten, eine feste
Liste würde ständig Lücken reißen. Alternative: **Custom** mit der Liste unten.

So geht es (am zuverlässigsten im Browser am Windows-Laptop, nicht in der iPhone-App):
1. claude.ai/code öffnen und diese Sitzung („US-Kongress Dashboard“) anklicken.
2. Oben auf den kleinen Pfeil (⌄) direkt hinter dem Sitzungstitel klicken → **Edit cloud environment**.
   Alternativ: Neue Sitzung → unter dem Eingabefeld das erste Bedienelement (Umgebung „Andreas Cloud“)
   → mit der Maus über die Zeile fahren → Zahnrad-Symbol rechts.
3. Im Dialog **Network access** auf **Full** stellen (oder **Custom** + Domains) → speichern.
4. Wirkt in laufenden Sitzungen nach etwa einer Minute.

Den Congress.gov-Key am besten als **Network secret** im selben Dialog hinterlegen
(Host `api.congress.gov`, Header-Name `X-Api-Key`, Präfix leeren, Wert = Key). Dann sehen ihn
weder Chat noch Repository.
Anleitung: https://code.claude.com/docs/en/cloud-environments#network-access

Danach führt `scripts/check_sources.sh` den Praxistest erneut aus.

### Domains für die Freigabeliste

```
api.congress.gov
www.congress.gov
api.govinfo.gov
www.govinfo.gov
www.senate.gov
clerk.house.gov
docs.house.gov
www.house.gov
www.foreign.senate.gov
foreignaffairs.house.gov
www.armed-services.senate.gov
armedservices.house.gov
www.intelligence.senate.gov
www.appropriations.senate.gov
appropriations.house.gov
www.federalregister.gov
www.dsca.mil
www.state.gov
www.whitehouse.gov
unitedstates.github.io
api.open.fec.gov
feeds.npr.org
www.npr.org
apnews.com
www.reuters.com
www.c-span.org
rollcall.com
thehill.com
rss.politico.com
www.politico.com
www.defensenews.com
www.justsecurity.org
www.lawfaremedia.org
news.google.com
www.youtube.com
ballotpedia.org
```

---

## 2. Quellenkatalog

Prinzip: **Primärquellen liefern Fakten, Medien liefern Orientierung und Kontext.**
Jede Aussage im Briefing trägt einen Quellenlink. Bewertung: Verlässlichkeit (V), maschinenlesbar (M).

### Stufe 1 – Primärquellen (Fakten)

| Quelle | Liefert | Zugriff | V | M | Anmerkung |
|---|---|---|---|---|---|
| Congress.gov API (Library of Congress) | Bills + Verlauf, Amendments, Committee Meetings, Hearings, Nominations, Treaties, Congressional Record | JSON-API, kostenloser Key (api.data.gov), 5.000 Req./h | sehr hoch | ja | Rückgrat der Pipeline. Verzögerung von Stunden bis 1 Tag bei manchen Daten. |
| Senate.gov Roll Call Votes | Abstimmungen Senat | XML | sehr hoch | ja | Abstimmungszahlen **per Code**, nicht per KI auslesen |
| House Clerk (clerk.house.gov) | Abstimmungen House, Floor Summary | XML | sehr hoch | ja | dito |
| docs.house.gov | Wochenplan House-Ausschüsse, Floor-Agenda | XML/HTML | sehr hoch | teilweise | „Week ahead“-Modul |
| GovInfo API | Congressional Record, Gesetzestexte, Hearing-Transkripte | JSON-API, gleicher Key | sehr hoch | ja | Hearing-Transkripte erscheinen oft erst Wochen später |
| Ausschuss-Websites (SFRC, HFAC, SASC, HASC, Intel, Approps) | Hearing-Termine, Zeugen, Statements, Videos | HTML, teils RSS | hoch | teilweise | Websites ändern sich → Scraper fragil, Agent liest statt Code |
| CRS Reports (congress.gov/crs-products) | Hintergrund-Analysen, überparteilich | HTML/PDF | sehr hoch | teilweise | Ideal für „Hintergrund“-Links |
| DSCA Major Arms Sales | Waffenverkaufs-Notifikationen an den Kongress | HTML | sehr hoch | teilweise | Außenpolitik-Säule |
| Federal Register API | Exekutivhandeln mit Kongressbezug | JSON-API | sehr hoch | ja | optional |
| FEC API | Wahlkampffinanzen 2026 | JSON-API, Key | sehr hoch | ja | Midterms-Modul |
| unitedstates/congress-legislators | Abgeordneten-Stammdaten (Partei, Staat, IDs, Fotos) | JSON | sehr hoch | ja | Personen-Verknüpfung |

**Nicht mehr verfügbar:** ProPublica Congress API (eingestellt, keine Keys mehr), GovTrack-API (beendet).
Viele Online-Tutorials nutzen diese noch – bewusst ausgeschlossen.

### Stufe 2 – Nachrichtenagenturen & Leitmedien (Orientierung: Was ist heute wichtig?)

| Quelle | Zugriff | V | Problem / Lösung |
|---|---|---|---|
| AP News | Keine offizielle öffentliche RSS (Stand unklar); Seite sperrt KI-Abrufe | sehr hoch | **Kritisch:** AP blockiert automatisierte Abrufe. Lösung: Google-News-Feed `site:apnews.com congress` liefert Schlagzeile + Link; Inhalt nicht auslesen. |
| Reuters | RSS seit Juni 2020 eingestellt; Seite sperrt KI-Abrufe | sehr hoch | wie AP, über Google-News-Feed. |
| NPR | Offizielle RSS (Politics-Feed) | hoch | gut nutzbar |
| C-SPAN | Website, Videoarchiv mit Untertitel-Transkripten | sehr hoch (Rohmaterial) | beste Video-Quelle; Einbettung teils eingeschränkt, Bot-Schutz möglich |
| Roll Call | RSS | hoch | Kongress-Fachmedium |
| The Hill | RSS je Ressort | mittel-hoch | Masse, teils boulevardesk – nur als Signal |
| Politico (frei) | RSS | hoch | Pro-Inhalte nicht zugänglich |
| Punchbowl News | Paywall | hoch | nur Schlagzeilen, wenn überhaupt |

Geklärt: Gemeint war **AP News**.

### Stufe 3 – Fachmedien für Kontext (vor allem Außen- & Sicherheitspolitik)

| Quelle | Schwerpunkt | Zugriff |
|---|---|---|
| Defense News | NDAA, Verteidigungshaushalt | RSS |
| Just Security | War Powers, Völkerrecht, Kongress vs. Exekutive | RSS |
| Lawfare | Recht & Sicherheit, Oversight | RSS |
| Foreign Policy / Foreign Affairs | Einordnung | teils Paywall – nur Links |
| Cook Political Report, Ballotpedia | Midterms: Ratings, Kandidaten | HTML, Cook teils Paywall |

### Stufe 4 – Video

| Quelle | Nutzung |
|---|---|
| YouTube-Kanäle der Ausschüsse und Fraktionen | Einbettung möglich; Kanal-RSS ohne API-Key |
| C-SPAN | Hearings/Floor in voller Länge, Transkripte → Agent sucht Zeitmarken |
| Senate/House Floor Video | Live und Archiv |

Realistisch: **1–3 ausgewählte Clips pro Tag mit Zeitmarke**, Einstieg genau an der relevanten Stelle.

---

## 3. Agenten-Architektur mit Gegenagenten

```
 ┌───────────────── STUFE 1: SAMMELN (parallel) ─────────────────┐
 │ Floor & Votes │ Legislation │ Committees │ Foreign Policy │     │
 │ Elections 2026 │ News-Scan (AP/Reuters/NPR/C-SPAN/…) │ Video  │
 └───────────────────────────────┬───────────────────────────────┘
                                 ▼
          STUFE 2: BÜNDELN – Dubletten zu „Stories“ zusammenführen (Code + Agent)
                                 ▼
 ┌──────────── STUFE 3: RELEVANZ (Agent vs. Gegenagent) ─────────┐
 │ Relevanz-Agent A: bewertet nach Rubrik (Tragweite, Außenpol., │
 │   Machtfragen, Neuigkeitswert)                                 │
 │ Relevanz-Agent B (Advocatus Diaboli): greift die Auswahl an –  │
 │   „Was ist überbewertet? Welche große Story fehlt?“            │
 │ Schiedsrichter-Agent: entscheidet bei Dissens, begründet       │
 └───────────────────────────────┬───────────────────────────────┘
                                 ▼
          STUFE 4: SCHREIBEN – Redakteur-Agent pro Säule, jede Aussage mit Quelle
                                 ▼
 ┌──────────── STUFE 5: PRÜFEN (zwei unabhängige Prüfer) ────────┐
 │ Faktenprüfer A: Aussage für Aussage gegen die Primärquelle     │
 │ Faktenprüfer B: sieht nur Text + Quellen (nicht A's Ergebnis): │
 │   Zahlen, Daten, Namen, Abstimmungsergebnisse                  │
 │ Neutralitäts-Prüfer: parteiische Sprache, einseitiges Framing  │
 │ → nicht bestätigte Aussagen werden gestrichen oder markiert    │
 └───────────────────────────────┬───────────────────────────────┘
                                 ▼
          STUFE 6: CHEFREDAKTION – Gesamtbild, Zeitbudget, Konsistenz
                                 ▼
          STUFE 7: MASCHINEN-CHECK (Code, keine KI) – Schema gültig, Links erreichbar,
                   Abstimmungszahlen = XML, Datumsangaben plausibel → Veröffentlichen
```

### Kritische Anmerkungen zu den Gegenagenten

1. **Unabhängigkeit ist begrenzt.** Zwei Agenten desselben Modells teilen dieselben blinden Flecken.
   Echte Unabhängigkeit entsteht nur durch *unterschiedliche Informationen*: Prüfer B sieht bewusst nicht,
   was Prüfer A gedacht hat, und Gegenagent B bekommt eine andere Aufgabe („angreifen“, nicht „bewerten“).
2. **Code schlägt KI, wo immer möglich.** Abstimmungsergebnisse, Daten, Bill-Nummern werden aus den
   Primärdaten per Programm übernommen – nicht von einem Agenten „abgeschrieben“. Das eliminiert eine
   ganze Fehlerklasse, statt sie nur zu prüfen.
3. **Kosten & Limits.** Rund 15–20 Agenten-Aufrufe pro Tag. Über das Claude-Abo bedeutet das: Die
   tägliche Aufgabe verbraucht spürbar Kontingent. Wir starten schlank und messen.
4. **Endlosschleifen vermeiden.** Gegenagenten dürfen nur eine Runde widersprechen; danach entscheidet
   der Schiedsrichter. Sonst diskutieren Agenten ohne Ergebnis.
5. **Modell-Vielfalt.** Wo möglich laufen Agent und Gegenagent auf *unterschiedlichen* Claude-Modellen
   (z. B. großes Modell bewertet, anderes Modell greift an). Das verringert gemeinsame blinde Flecken
   zusätzlich zu den getrennten Informationen.
6. **Nachvollziehbarkeit.** Jeder Dissens (was Gegenagent B beanstandet hat, wie der Schiedsrichter
   entschieden hat) wird im Briefing-Datensatz gespeichert und ist im Dashboard aufklappbar.

---

## 4. Aufbau des 40-Minuten-Briefings (Vorschlag)

| Bereich | Inhalt | Lesezeit |
|---|---|---|
| **Top Stories** | 4–6 wichtigste Entwicklungen, je mit „Why it matters“ und Quellen | ~12 min |
| **Foreign Policy Desk** | Außenpolitisches Handeln des Kongresses: Hearings, Resolutionen, Sanktionen, War Powers, Nominierungen, Arms Sales, CODELs | ~10 min |
| **Midterms 2026** | Rennen, Ratings, Umfragen, Finanzen; nach der Wahl: Mehrheiten, Lame Duck | ~6 min |
| **Floor & Committees** | Was passiert heute / diese Woche, Abstimmungen von gestern | ~5 min |
| **Watch** | 1–3 Clips mit Zeitmarke | ~5 min |
| **Also Notable** | Schlagzeilen-Liste zum Überfliegen, je ein Satz + Link | ~2 min |

Jeder Eintrag zeigt Lesezeit, Wichtigkeitsstufe und Prüfstatus (verified / multiple reports / unconfirmed).

---

## 5. Offene Punkte

- [ ] Netzwerkzugang der Umgebung erweitern (Blocker)
- [ ] Kostenlosen Congress.gov-API-Key beantragen (api.data.gov/signup) und als Secret hinterlegen
- [x] Klären: Was ist „NP News“? → AP News
- [ ] Nach Freigabe: `scripts/check_sources.sh` laufen lassen, Katalog mit echten Ergebnissen aktualisieren
- [ ] Weiter mit Schritt 2: Design
