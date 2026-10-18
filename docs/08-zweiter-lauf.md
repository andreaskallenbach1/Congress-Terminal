# Zweiter Lauf – Messlauf mit voller Pipeline (18.10.2026)

Lauf `2026-10-18-daily`, gestartet 06:00 UTC (Sonntag, Sitzungspause), veröffentlicht 06:39 UTC.
Ziel: Sparmaßnahmen (Etappe 3b) messen und die neuen Rollen (Etappe 4) zum ersten Mal im Volllauf testen.

## Ergebnis

| Punkt | Ergebnis |
|---|---|
| Ausgabe | 2 Storys (Leitartikel Russland-Sanktionen, Midterms Iran-Krieg in Wahlwerbung), 1 Also Notable, Kalender 4 Termine, ~9 min Lesezeit |
| Claims | 73 (19 Kernaussagen), alle Kernaussagen von A und B bestätigt |
| Maschinen-Check | 0 Probleme, 0 Warnungen |
| Build | bestanden, Startseite und Leitartikel im Browser (Chromium) geprüft |
| Pro-Limit | **nicht** erreicht (erster Lauf: in Stufe 4 erreicht) |

Nur 2 Storys sind kein Fehler der Pipeline: Sonntag, beide Kammern in der Pause, keine Abstimmungen, nur ein Ausschusstermin.
Der Gegenagent hat 5 Einwände erhoben, der Schiedsrichter alle angenommen (u. a. War-Powers-Meldung stammte vom April, Bildungsanhörung nur Kalender). Aufgefüllt wurde nicht: lieber kurz als dünn.

## Verbrauch je Stufe (Subagent-Tokens)

| Stufe | Rolle | Modell | Lauf 2 | Lauf 1 (17.10.) |
|---|---|---|---|---|
| 0 | Türsteher (nur Schlagzeilen) | klein | 78.511 | – (neu) |
| 1 | Sammler (alle 8 Bereiche in **einem** Agenten) | klein | 123.708 | – (neu) |
| 2 | Bündler | klein | 95.393 | 181.976 |
| 3a | Relevanz | mittel | 81.023 | nicht erfasst |
| 3b | Gegenagent | mittel | 95.473 | nicht erfasst |
| 3c | Schiedsrichter | groß | 128.732 | 136.778 |
| 4 | Faktenkarten (beide Storys, ein Agent) | klein | 187.885 | – (neu) |
| 4 | Redakteur Leitartikel | groß | 153.197 | 328.695 (Top, 4 Storys) |
| 4 | Redakteur Midterms | mittel | 107.517 | 170.943 (groß) |
| 4 | Redakteure Foreign/Floor | – | entfallen (keine Story) | 418.689 |
| 4 | Historiker | mittel | 92.745 | – (neu) |
| 4 | Verfahrens-Erklärer | klein | 144.108 | – (neu) |
| 5a | Prüfer A (alle Claims) | groß | 176.552 | 302.427 (zwei Agenten) |
| 5b | Prüfer B (blind, Kernaussagen) | mittel | 130.984 | 293.791 |
| R3 | Überarbeitung | groß | 108.559 | 163.001 |
| R3 | Nachprüfung A / B | groß / mittel | 108.050 / 86.986 | 116.683 / 140.439 |
| 5c | Neutralität | mittel | 85.138 | nicht erfasst |
| 6 | Chefredaktion (nur `editor.json`) | groß | 94.709 | 151.197 (Zusammenbau von Hand) |
| | **Summe** | | **2.079.270** | ≥ 2.400.000 (ohne 3a, 3b, 5c) |

Nach Modell: klein 630 Tsd. · mittel 680 Tsd. · groß 770 Tsd. (Lauf 1: fast alles groß).

**Vergleich pro Claim** (Lauf 1: 88 Claims, ~10 Storys · Lauf 2: 73 Claims, 2 Storys):

| Block | Lauf 1 | Lauf 2 |
|---|---|---|
| Schreiben (+ Faktenkarten) | ~10.400 je Claim | ~6.200 je Claim |
| Prüfen inkl. R3 und Nachprüfung | ~13.100 je Claim | ~8.300 je Claim |
| Chefredaktion | 151 Tsd. | 95 Tsd. |

Die Einsparung liegt damit bei rund einem Drittel je Claim, dazu kommt die Verschiebung zu kleineren Modellen, die das
Pro-Kontingent weniger belastet. Weil Lauf 2 nur 2 Storys hatte, ist der Vergleich grob: Ein Lauf mit 10 Storys wird
die Fixkosten besser verteilen, aber deutlich mehr Claims haben.

## Wichtigster Befund: Fixkosten je Agent

Jeder Subagent kostet **rund 70–80 Tsd. Tokens, bevor er etwas tut** (Projekt-Prompt, Werkzeuge, Skills). Neutralität mit nur
3 Werkzeugaufrufen: 85 Tsd.; Prüfer B nach Korrektur einer Prämisse: 87 Tsd. Daraus folgt:

- **Agenten bündeln, wo die Rolle es erlaubt:** Die 8 Sammler liefen als **ein** Agent (spart rechnerisch ~500 Tsd.);
  Faktenkarten für alle Storys in einem Agenten. Abweichung von der Architektur (8 parallele Sammler) – dokumentiert,
  der Skill ist angepasst.
- **Nicht bündeln**, wo Unabhängigkeit der Zweck ist: Prüfer A und B bleiben getrennt, B bleibt blind (Andreas' Entscheidung).
- Größter Hebel für weitere Einsparung: weniger Agentenstarts (z. B. Relevanz + Neutralität in bestehende Agenten
  einhängen) – nur nach Rücksprache, weil es Gegenproben schwächen kann.

## Was die Gegenproben gefunden haben

- **Schiedsrichter:** ABC-Meldung zur War-Powers-Frist war vom 30. April (Frist 1. Mai) → gestrichen.
- **Prüfer A:** 9 Ablehnungen – Überdehnungen („most of the Act was waived“), falsche Zuschreibungen (AP-Erzählung als
  Zitat eines Strategen; CRS-Zitat, das eigentlich Attorney General Cushing 1854 wiedergibt), „multiple“ mit nur einer Quelle
  für den ganzen Satz, eigene Rechnung („would run past Nov. 3“), unbelegte Dek-Zeile.
- **Prüfer B:** lehnte in der Nachprüfung c5 ab, weil es „keine Senatorin Darline Graham“ gebe – **falsch**: Congress.gov
  führt Darline Graham (G000608, Senat seit 2026). B hatte nur den Datensatz von Lindsey Graham gelesen. Nach Hinweis auf
  den Primärdatensatz bestätigt. **Abweichung:** eine zusätzliche Runde für B, nur zur Korrektur einer falschen Prämisse
  (Namen sind harte Fakten aus Primärdaten, Abschnitt 7). Lehre: Prüfer-B-Auftrag nennt künftig `data/members.json` als
  Primärquelle für Namen.
- **Maschinen-Check:** CRS-PDFs galten pauschal als „nicht prüfbar“, obwohl sie im Seiten-Speicher lagen → behoben.

## Im Lauf behoben (Code)

| Problem | Lösung |
|---|---|
| PDF-Quellen (Senatorenbrief) waren Binärmüll im Seiten-Speicher | `pages.py` extrahiert PDFs mit `pdftotext` |
| Ohne Floor-Story kein Kalender und keine „Today“-Zeilen | `pipeline/agenda.py` (Code): Termine aus Vorausgabe + Ausschussterminen, Notizen zu fehlenden Abstimmungen und ausgefallenen Primärquellen |
| Ausgabeformat der Fachleute war nicht festgelegt | `expert-<rolle>.json` + `pipeline/merge_experts.py` (Präfix h/p, nur Nebenaussagen) |
| Nachprüfung nach R3 überschrieb die ersten Urteile nicht verlässlich | `apply_verdicts.py` liest `checkA-recheck.json`/`checkB-recheck.json` zuletzt |
| Glossar nahm ein Satzfragment als „Definition“ an | `glossary_add.py` verlangt einen ganzen Satz |
| Bildunterschrift „(symbolic image)“ doppelt | `assemble.py` entfernt den Zusatz, die App setzt ihn |
| `process-facts.json` | per Code aus Auswahl, Eingaben und Entwurf |

## Ausfälle und Grenzen

- **Federal Register API:** 403 → keine Arms-Sales-Prüfung heute (in „Today“ vermerkt). GovInfo funktioniert.
- **YouTube-Feeds** (C-SPAN, Speaker, Senate Democrats): 404 → keine Clips. Offen: neue Feed-Adressen finden.
- **Wikimedia Commons:** 429 beim Titelbild → Unsplash-Symbolbild (Kapitol bei Nacht).
- **Gesperrt/403:** Politico, The Hill, NYT, WJTV, congress.gov-Webseiten (die API funktioniert).
- **Washington Post:** wieder nicht erreichbar → Umfrage-Meldung entfallen.
- **Dünner Sonntag:** 29 Feed-Meldungen seit der letzten Ausgabe; 11 nach dem Türsteher.
- Lesezeit 9 statt 40 Minuten – an Pausentagen erwartbar; die 40 Minuten sind Obergrenze, kein Soll.
