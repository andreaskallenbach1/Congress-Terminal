# Phase 4 · Etappe 2a – Ausgabe-Layout und Datenformat (17.10.2026)

## Datenformat (Schema v1)

Festgelegt in `app/src/content.config.ts`. Jede Datei in `briefings/` muss dem Schema entsprechen, sonst bricht der Bau ab
(Maschinen-Check, Stufe 7, für die Struktur). Kernpunkte:

| Feld | Inhalt |
|---|---|
| `stories[]` | Säule, Headline, Dek, What's new, Why it matters, What's next, Background (optional), Wörter, Lesezeit, Gesamtstatus, Relevanz mit Begründung und Einwand des Gegenagenten |
| `stories[].claims[]` | Aussage, Gewicht (Kern/Neben), Status, Herkunft (Code/Agent), Beleg-Zitate mit Quelle und Link, Urteil Prüfer A/B |
| Absätze | Klartext; `[[c3]]` hinter einem Satz hängt Claim c3 an und zeigt seinen Prüfstatus mit Link zum Beleg |
| `floor.votes[]` | Roll Call mit Stimmen je Partei – nur aus Primärdaten (Code) |
| `agenda[]`, `overnight[]`, `today[]` | Rechte Spalte und Kalender |
| `armsSales[]`, `watch[]`, `notable[]` | Waffenverkäufe, Clips mit Startzeit, Kurzmeldungen |
| `sources[]`, `process` | Quellenliste mit Abrufzeit; Kennzahlen „How this edition was made“ |
| `sample` | Nur für Testdaten. Ein normaler Bau mit `sample: true` bricht ab |

## Gebaut

- Startseite: Titelbild, „In this edition“ mit Lesezeit-Balken, Leitartikel im vollen Story-Format, weitere Top Stories, rechte Spalte (Overnight, Today, Next 7 days, Countdown zur Wahl), Floor & Committees mit Sitzplan-Grafik des Roll Calls, Midterms, Foreign Policy Desk mit Waffenverkäufen, Watch, Also notable, „How this edition was made“
- Story-Seite je Story (`/stories/<id>/`) mit allen Aussagen, Gewicht, Prüfstatus und wörtlichem Beleg-Zitat
- Gesetzes-Fortschritt (FT 5) als Stufenleiste, Rückschläge (Veto, Waiver) rot
- Feedback (FT 8): „Flag an error“ und „Less of this“ öffnen ein vorausgefülltes GitHub-Issue; „Set aside“ merkt sich der Browser
- Testausgabe `app/test/fixtures/briefings/` (deutlich als Testdaten markiert, Bau mit `npm run build:sample`); getrennter Zwischenspeicher, damit Testdaten nie in den echten Bau geraten

## Getestet

Chromium, 1440 px und 390 px, hell und dunkel: keine Konsolenfehler, kein seitliches Scrollen. Normaler Bau ohne Ausgabe zeigt weiterhin die ehrliche Leerseite.

## Offen für Etappe 2b

Karten (Welt, USA), Porträts in den Midterms, Watchlist-, Kalender-, Archiv-, Sources- und Suchseite, Glossar-Tooltips, Members und Committees, Vorlesen.
