# Erster echter Lauf – Ausgabe 2026-10-17-daily (schlanke Pipeline)

Veröffentlicht 17.10.2026, 23:1x MESZ: https://andreaskallenbach1.github.io/Congress-Terminal/

## Ablauf und Zahlen

| Stufe | Wer | Ergebnis |
|---|---|---|
| 1 Sammeln | Code (`pipeline/collect.py`) | 71 Gesetze mit echter Aktion, 445 Feed-Meldungen aus 43 Feeds, 0 Abstimmungen (Kongress in Wahlpause seit 30.9.), 40 s |
| 2 Bündeln | kleines Modell | 30 Kandidaten, keine eingeschleusten Anweisungen |
| 3a Relevanz | mittleres Modell | 23 ausgewählt |
| 3b Gegenagent | mittleres Modell, Tavily | 8 Einwände, 6 fehlende Storys (u. a. Frist 11.12., NDAA, Iran-War-Powers) |
| 3c Schiedsrichter | großes Modell | 11 Storys + 6 Kurzmeldungen; korrigierte falsche Gesetzesnummer der Relevanzstufe |
| 4 Schreiben | 4 × großes Modell | 11 Storys, 222 Aussagen, 96 Kernaussagen, ~300 Beleg-Zitate wörtlich geprüft |
| 5a Prüfer A | großes Modell | 208 bestätigt, 14 abgelehnt |
| 5b Prüfer B (blind) | mittleres Modell | 93 von 96 Kernaussagen bestätigt |
| R3 Überarbeitung | großes Modell | 17 Aussagen korrigiert; 2. Runde: A 17/17, B 8/9 → Omar-Story nach FT 2 gestrichen (nur als Kurzmeldung) |
| 5c Neutralität + R4 | mittleres Modell | 31 Formulierungen geglättet, u. a. Leitartikel-Überschrift |
| 6 Chefredaktion | großes Modell | Ausgabe zusammengestellt, ~30 min Lesezeit |
| 7 Maschinen-Check | Code | 1. Durchgang 10 Statusfehler gefunden; R5: Regel für Prognose-Ratings ergänzt, 2 Status gesenkt; 2. Durchgang 0 Probleme |

## Befunde

- **Verbrauch:** Das Pro-Sitzungskontingent war während Stufe 4 erschöpft (vier große Modelle parallel, dazu die lange Entwicklungssitzung am selben Tag). Ein voller Lauf mit allen 25 Rollen und Einzelprüfung jeder Kernaussage passt voraussichtlich nicht täglich in Pro. Entscheidung offen (Hebel: Redakteure mittleres Modell außer Leitartikel; weniger Storys; Lauf nach Bedarf; Max-Abo).
- **Die Gegenproben wirken:** Schiedsrichter fing falsche Bill-Nummer ab; Prüfer B fand eine falsche Einordnung (H.R. 2347), die A übersah; Maschinen-Check fand 10 Statusfehler, die alle drei Prüfer übersahen.
- **Quellen-Grenzen:** Federal Register blockiert Volltexte von der Sitzungs-IP (Waffenverkäufe ohne Käufer/Wert); FEC-API mit DEMO_KEY ausgeschöpft → **eigener kostenloser FEC-Schlüssel nötig**; www.congress.gov, NYT, Politico, CNBC, The Hill teils 403 (Ausweichen auf API, GovInfo, EveryCRSReport, Pressemitteilungen); Wikimedia 429, loc.gov Cloudflare → Titelbild aus Unsplash.
- **Regel ergänzt:** Prognose-Seiten (Cook u. a.) gelten als Primärquelle nur für ihre eigenen Ratings und nur, wenn die Aussage sie nennt.
- **Technik:** Zitate kamen teils kleingeschrieben (Normalisierung) → `merge_drafts.py` stellt Schreibweise aus der Quelle wieder her. Bill-Stufen mit Jahreszahl, wenn sie aus einem früheren Jahr stammen.
