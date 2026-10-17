# Phase 4 · Etappe 1 – Grundgerüst (17.10.2026)

| Entscheidung | Begründung |
|---|---|
| App liegt in `app/` (Astro 5, statisch) | Trennt Web-App von Pipeline (`pipeline/`, Etappe 3) und Briefings |
| Briefings liegen in `briefings/` (eine JSON-Datei pro Ausgabe) | Einziger Ordner, in den Agenten schreiben dürfen |
| Adresse: `https://andreaskallenbach1.github.io/Congress-Terminal/` | GitHub Pages aus dem öffentlichen Repository |
| Schriften selbst gehostet (Fontsource) statt Google Fonts | Keine Abrufe bei Google (Datenschutz), funktioniert offline |
| Service Worker: Seiten zuerst aus dem Netz, sonst aus dem Speicher | Neue Ausgabe gewinnt immer; die zuletzt geöffnete bleibt offline lesbar |
| Kein Beispielinhalt | Projektregel: keine Platzhalter, die wie echte Daten aussehen; leere Seiten sagen ehrlich, was dort erscheinen wird |
| Zeitangaben in Berliner Zeit | Phase-3-Befund |
| Grau `#808080` statt `#9A9A9A` | Phase-3-Befund (Kontrast) |
| Veröffentlichung: `.github/workflows/pages.yml` bei jedem Push auf `main` und den Entwicklungs-Branch | Läufe committen auf `main`, die Seite baut sich neu |

## Getestet (Chromium, lokal)

- Build fehlerfrei, 7 Seiten (Today, Watchlist, Calendar, Archive, Sources, Search, 404)
- Installierbar: keine Installability-Fehler, Service Worker aktiv mit Scope `/Congress-Terminal/`
- Hell- und Dunkelmodus, Handybreite 390 px ohne seitliches Scrollen, keine Konsolenfehler
- Hinweis auf das Alter der Ausgabe mit einer Testdatei geprüft („2 days of news are not in it yet“), Testdatei danach entfernt

## Offen / Grenzen

- GitHub Pages muss Andreas einmal einschalten (Settings → Pages → Source: GitHub Actions)
- Branch `main` anlegen erst nach Andreas' ausdrücklicher Freigabe
- Update-Knöpfe kommen in Etappe 5; bis dahin werden sie nicht angezeigt (keine Attrappen)
- Installation unter Windows in Edge erst nach der Veröffentlichung praktisch prüfbar
