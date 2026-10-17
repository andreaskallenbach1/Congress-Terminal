# Phase 4 · Etappe 2b – Karten, Unterseiten, Glossar, Suche (17.10.2026)

| Teil | Umsetzung | Grenze |
|---|---|---|
| Titelbild | Wechselt je Ausgabe; Feld `hero` mit `relation` (story/symbolic) und Bildunterschrift; Symbolbilder werden gekennzeichnet | Auswahl der Bilder übernimmt die Pipeline (Etappe 3) |
| Karten | Weltkarte (Natural Earth, world-atlas) und US-Karte (US Census, us-atlas), beim Bau als SVG erzeugt, nummerierte Marker passend zu den Storys | Kleinstaaten fehlen in der 110m-Weltkarte → Story erscheint ohne Marker |
| Porträts | Offizielle Porträts über unitedstates/images (GPO, gemeinfrei), per Bioguide-ID | Externe Bildquelle; fällt sie aus, bleibt ein grauer Platzhalter |
| Watchlist | Jedes Gesetz aus den Storys einmal, im zuletzt bekannten Stand | Noch keine eigene, laufend gepflegte Watchlist-Datei (kommt mit der Pipeline) |
| Kalender, Archiv, Sources, Members | Eigene Seiten, ehrliche Leerseiten ohne Ausgabe | Ausschuss-Seiten folgen mit den Ausschussdaten der Pipeline |
| Glossar (FT 7) | 22 Begriffe, Definitionen wörtlich aus dem Senats-Glossar (senate.gov, abgerufen 17.10.2026); Tooltip beim ersten Vorkommen je Story; Eigennamen wie „Continuing Appropriations Act“ werden nicht markiert | House-Begriffe (Discharge Petition, Suspension of the Rules) fehlen noch: congress.gov sperrt direkte Abrufe (403), Quelle wird in der Pipeline über CRS/API ergänzt |
| Suche | Pagefind, Index nach jedem Bau, durchsucht Storys, Watchlist, Abgeordnete, Glossar | – |

Getestet (Chromium): alle Seiten 1440 und 390 px, keine Konsolenfehler, kein seitliches Scrollen, Suche liefert Treffer, Tooltip erscheint beim Darüberfahren.

Offen: Vorlesen (Stimme Google Chirp 3 HD, später), Update-Knöpfe (Etappe 5), Committees-Seite.
