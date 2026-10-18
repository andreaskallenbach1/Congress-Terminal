# Nachtarbeit 17./18.10.2026 – Plan und Fortschritt (Auftrag von Andreas: 3b, dann 4, ohne Unterbrechung)

Wird nach jedem Schritt aktualisiert. Eine Sitzung, die nach einem Limit neu startet, macht beim ersten offenen Punkt weiter.

## Etappe 3b – Sparmaßnahmen
- [x] 3b.1 Seiten-Speicher: jede Quelle einmal abrufen (`pipeline/pages.py`), quote_check/check_edition/merge lesen daraus
- [x] 3b.2 Faktenkarten (kleines Modell) je Story; Redakteure schreiben aus Karten
- [x] 3b.3 Status-Vorprüfung per Code vor Prüfer A (Status deterministisch korrigieren)
- [x] 3b.4 Ausgabe per Code zusammenbauen (`pipeline/assemble.py`); Chefredaktion liefert nur Urteile
- [x] 3b.5 Eingaben verdichten (Dubletten, kurze Zusammenfassungen) für Bündeln/Türsteher
- [ ] 3b.6 Zweiter Lauf zum Messen – zusammengelegt mit 4.7 (ein Lauf misst Einsparung je bestehender Stufe und Kosten der neuen Rollen; spart einen ganzen Lauf). Start nach dem Bau von Etappe 4, mit Nachrichtenfenster seit der letzten Ausgabe

## Etappe 4 – volle Pipeline (Rollen einzeln, jeweils gemessen)
- [x] 4.1 Türsteher (klein) nur auf Titeln (vorgezogen, da größter Hebel beim Bündeln)
- [x] 4.2 Sammler-Agenten (klein, begrenzte Suchen) inkl. Executive & Courts (CourtListener)
- [x] 4.3 Abgeordneten-Profile per Code (Ausschüsse, Voteview) + Committees-Seite
- [x] 4.4 Verfahrens-Erklärer und Historiker (in Background, Glossar-Vorschläge mit Primärquelle)
- [x] 4.5 Watchlist-Datei per Code (FT 5), Feedback-Issues einlesen (FT 8)
- [x] 4.6 Wochenausgabe (FT 10): Lauf-Art „weekly“ + Deep-Dive in App und Anleitung
- [ ] 4.7 Volllauf testen, messen, dokumentieren

## Offen für Andreas
- FEC/GovInfo-Schlüssel: wird angehängt, aber als ungültig abgelehnt (API_KEY_INVALID) → Schlüssel neu kopieren bzw. Freischalt-Mail prüfen
