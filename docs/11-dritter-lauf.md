# Dritter Lauf – Test der optimierten Pipeline (20.10.2026)

Lauf `2026-10-20-daily`, gestartet von Andreas in der Entwicklungssitzung, Ausgabe live.

## Ergebnis

| Punkt | Ergebnis |
|---|---|
| Ausgabe | Leitartikel (Russland-Sanktionsaussetzung, Folgestory: Speaker Johnson, Cramer, Turner, Fitzpatrick, Zelenskyys Videocall zu Starlink) · Plenumsnotiz (Sitzungspause) · 7 Kurzmeldungen · 2 C-SPAN-Clips · 9 Rüstungsverkaufs-Mitteilungen · ~14 min Lesezeit |
| Faktenprüfung | 59 Claims (12 Kernaussagen); B bestätigte alle 12, A lehnte 5 ab; nach R3 bestätigte A 6 von 7 |
| Feste Regel (Code) | Senats-Story → Kurzmeldung (Kernaussage CBS-Umfrage nur eine Quelle); Nebenaussage c21 samt Sätzen gestrichen |
| Maschinen-Check / Build | 0 Probleme, 0 Warnungen; Startseite im Browser geprüft |
| Quellen | Kein endgültiger Ausfall (zweiter Abrufversuch); Tavily-Konnektor nicht verbunden → Gegenagent über Firecrawl + Congress.gov API |

## Verbrauch (Subagent-Tokens)

| Stufe | Modell | Lauf 3 | Lauf 2 |
|---|---|---|---|
| Türsteher | klein | 102.766 | 78.511 |
| Sammler (1 Agent) | klein | 116.328 | 123.708 |
| Bündler | klein | 130.928 | 95.393 |
| Relevanz | mittel | 85.732 | 81.023 |
| Gegenagent | mittel | 89.326 | 95.473 |
| Schiedsrichter | groß | 136.141 | 128.732 |
| Faktenkarten | klein | 178.102 | 187.885 |
| Redakteur Leitartikel | groß | 154.989 | 153.197 |
| Redakteur Midterms + Floor (1 Agent) | mittel | 91.250 | 107.517 (nur Midterms) |
| Fachleute | – | entfallen (siehe unten) | 236.853 (2 Agenten) |
| Prüfer A (mit Prüfpaket) | groß | 137.053 (13 Aufrufe, 59 Claims) | 176.552 (29 Aufrufe, 73 Claims) |
| Prüfer B | mittel | 111.102 | 130.984 |
| R3 | groß | 99.010 | 108.559 |
| Nachprüfung A | groß | 87.660 | 108.050 |
| Nachprüfung B | mittel | entfallen (kein Kernaussagen-Text geändert) | 86.986 |
| Neutralität | mittel | 77.250 | 85.138 |
| Chefredaktion | groß | 119.020 | 94.709 |
| **Summe** | | **1.716.657** (15 Agenten) | **2.079.270** (18 Agenten) |

Rund −17 % bei deutlich mehr Rohmaterial (278 statt 29 Meldungen, 23 statt 7 Kandidaten). Je Claim: ~29 Tsd. (Lauf 2: ~28 Tsd.)
– die Ersparnis kommt aus weniger Agentenstarts, nicht aus billigeren Claims.

## Entscheidungen im Lauf (Orchestrator)

- **Fachleute ausgelassen:** Der Leitartikel ist eine Folgestory; Präzedenzfälle (CAATSA, S.J.Res. 2 von 2019) standen am 18.10.
  im Background, und der Redakteur hatte bereits einen Verfahrens-Absatz (Discharge-Regel, CRS). Vorschlag für den Skill:
  Fachleute nur bei neuen Storys oder neuen Verfahren.
- **Midterms und Floor in einem Redakteur** (CLAUDE.md 9: Rollen ohne Unabhängigkeitsbedarf bündeln).
- **Prüfer B nicht erneut**, weil R3 bei keiner Kernaussage den Wortlaut änderte (B sähe dieselbe Eingabe). Regel für den Skill.

## Gefunden und behoben

- **Satzgrenzen bei mehreren Markierungen** (`[[c9]] [[c13]] [[c7]] [[c21]]`): Prüfpaket und feste Regel trennten jede
  Markierung als eigenen „Satz“ ab → das Paket zeigte leere Sätze, und das Streichen von c21 hätte den falschen Text
  stehen lassen. Behoben in `packets.py` und `apply_verdicts.py`. Gefunden von Prüfer A in der Nachprüfung.
- Der Schiedsrichter entlarvte die „neue“ 5-Mrd.-$-Saudi-Mitteilung im Federal Register per GovInfo-Primärtext als
  Veröffentlichung einer Mitteilung an den Kongress vom 1.9. (S.J.Res. 216/217 seit September im Ausschuss).

## Offene Frage an Andreas

- **Umfragen von Medien:** CBS ist bei der eigenen Umfrage selbst die Quelle (wie Cook bei eigenen Ratings). Soll eine
  Umfrage, die das Medium selbst durchgeführt hat, als Primärquelle für genau diese Umfrage gelten? Heute wurde die
  Senats-Story deshalb zur Kurzmeldung.
