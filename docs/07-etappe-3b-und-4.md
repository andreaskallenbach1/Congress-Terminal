# Etappe 3b (Sparmaßnahmen) und Etappe 4 (volle Pipeline) – Bau 17./18.10.2026

## Was gebaut wurde

| Teil | Wer | Was es spart oder bringt |
|---|---|---|
| Seiten-Speicher (`pipeline/pages.py`) | Code | Jede Quelle einmal pro Tag abgerufen; Redakteure, Prüfer und Maschinen-Check lesen daraus. Maschinen-Check: 47 s / 98 Abrufe → 0,2 s / 0 Abrufe |
| Türsteher | kleines Modell | Liest nur Schlagzeilen (`headlines.txt`, ~10 Tsd. Tokens statt ~180 Tsd. beim Bündeln aller Rohdaten) |
| Faktenkarten (`prefetch.py`, `cards_check.py`) | kleines Modell + Code | Quellen werden einmal in Aussagen mit wörtlichem Zitat zerlegt; Code verwirft Karten, deren Zitat nicht in der Quelle steht. Redakteure schreiben aus Karten |
| Redakteure | mittleres Modell, Leitartikel großes Modell | Andreas' Entscheidung 18.10.2026 |
| Status-Vorprüfung (`precheck.py`) | Code | Status, Wörter, Lesezeit, Story-Status vor den Prüfern; senkt zu starke Status. Im Entwurf des ersten Laufs fand sie die 3 maschinell erkennbaren Fehler |
| Zusammenbau (`assemble.py`) | Code | Chefredaktion liefert nur Urteile (`editor.json`); Test mit Lauf 1: identische Ausgabe |
| Waffenverkäufe | Code | Volltext über GovInfo (amtliche GPO-Ausgabe) statt federalregister.gov: Käufer, Wert, Rüstungsgut |
| Abgeordneten-Profile, Ausschüsse (`reference.py`) | Code | congress-legislators + Voteview (DW-NOMINATE); neue Seite Committees |
| Watchlist (`watchlist.py`, FT 5) | Code | Fortschritt je Gesetz aus den LoC-Aktionscodes der Congress.gov-API, bei jedem Lauf neu |
| Feedback (`feedback.py`, FT 8) | Code | Offene Feedback-Issues → Relevanz (Dimension 7) und Schiedsrichter (Korrekturen) |
| Sammler (8 Bereiche) | kleines Modell | Höchstens 5 Suchen und 8 Hinweise je Bereich; Code führt zusammen (`leads.py`) |
| Verfahrens-Erklärer | kleines Modell | Background zu Verfahren; neue Glossarbegriffe nur mit wörtlicher amtlicher Definition (`glossary_add.py`) |
| Historiker | mittleres Modell | Präzedenzfälle nur für Leitartikel/Top Stories, jede Aussage mit Beleg |
| Wochenausgabe (FT 10) | Anleitung + App | „The week in review“ und ein Deep-Dive (neue Säule `deep`) |

## Grenzen

- Die Einsparung ist geschätzt (ein Drittel bis knapp die Hälfte), gemessen wird sie im nächsten vollen Lauf (`docs/08-…`).
- Neue Rollen (Sammler, Historiker, Verfahrens-Erklärer) kosten zusätzlich; ihre Kosten werden im selben Lauf je Stufe ausgewiesen.
- Video-Startzeiten: nur aus Kapitelmarken oder Beschreibungen, sonst 0 (Videos werden nicht angesehen).
- FEC und GovInfo-API: Schlüssel wird angehängt, aber als ungültig abgelehnt (Andreas prüft).
