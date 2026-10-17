# Nachtarbeit 17./18.10.2026 – Plan und Fortschritt (Auftrag von Andreas: 3b, dann 4, ohne Unterbrechung)

Wird nach jedem Schritt aktualisiert. Eine Sitzung, die nach einem Limit neu startet, macht beim ersten offenen Punkt weiter.

## Etappe 3b – Sparmaßnahmen
- [ ] 3b.1 Seiten-Speicher: jede Quelle einmal abrufen (`pipeline/pages.py`), quote_check/check_edition/merge lesen daraus
- [ ] 3b.2 Faktenkarten (kleines Modell) je Story; Redakteure schreiben aus Karten
- [ ] 3b.3 Status-Vorprüfung per Code vor Prüfer A (Status deterministisch korrigieren)
- [ ] 3b.4 Ausgabe per Code zusammenbauen (`pipeline/assemble.py`); Chefredaktion liefert nur Urteile
- [ ] 3b.5 Eingaben verdichten (Dubletten, kurze Zusammenfassungen) für Bündeln/Türsteher
- [ ] 3b.6 Zweiter Lauf zum Messen (Tokens je Stufe vergleichen mit `docs/05-erster-lauf.md`)

## Etappe 4 – volle Pipeline (Rollen einzeln, jeweils gemessen)
- [ ] 4.1 Türsteher (klein) nur auf Titeln
- [ ] 4.2 Sammler-Agenten (klein, begrenzte Suchen) inkl. Executive & Courts (CourtListener)
- [ ] 4.3 Abgeordneten-Profile per Code (Ausschüsse, Voteview) + Committees-Seite
- [ ] 4.4 Verfahrens-Erklärer und Historiker (in Background, Glossar-Vorschläge mit Primärquelle)
- [ ] 4.5 Watchlist-Datei per Code (FT 5), Feedback-Issues einlesen (FT 8)
- [ ] 4.6 Wochenausgabe (FT 10): Lauf-Art „weekly“ + Deep-Dive in App und Anleitung
- [ ] 4.7 Volllauf testen, messen, dokumentieren

## Offen für Andreas
- FEC/GovInfo-Schlüssel: wird angehängt, aber als ungültig abgelehnt (API_KEY_INVALID) → Schlüssel neu kopieren bzw. Freischalt-Mail prüfen
