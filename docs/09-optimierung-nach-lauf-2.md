# Optimierung nach dem zweiten Lauf (18.10.2026)

Grundlage: Messlauf `2026-10-18-daily` (`docs/08-zweiter-lauf.md`). Entscheidungen von Andreas am 18.10.2026:
Historiker und Verfahrens-Erklärer zusammenlegen (Türsteher + Bündler bleiben getrennt) · Kernaussagen brauchen mindestens
`multiple reports` · CLAUDE.md verschlanken · Knopf „Update now“ mit einem Token, das nur in Andreas' Browser liegt.

## Bewertung des zweiten Laufs

| Bereich | Was gut lief | Was nicht gut lief |
|---|---|---|
| Durchlauf | Volle Pipeline in 39 Minuten, Pro-Limit nicht erreicht | Abläufe für Fachleute, Kalender und Nachprüfung mussten während des Laufs erfunden werden (jetzt Code und Skill) |
| Gegenproben | Schiedsrichter fing eine veraltete War-Powers-Meldung ab; A fand 9 echte Ungenauigkeiten | B lehnte eine richtige Aussage ab (Name aus dem Gedächtnis statt aus den Daten) |
| Code-Stufen | Faktenkarten 63/63 im Quelltext gefunden, Vorprüfung und Maschinen-Check ohne Befund, Zusammenbau fehlerfrei | CRS-PDFs pauschal als „nicht prüfbar“ markiert (behoben) |
| Quellen | GovInfo, Congress.gov API, Senats-PDFs funktionieren | Kurze Ausfälle (YouTube, Federal Register, Wikimedia) führten zu leeren Bereichen; 4 vom Schiedsrichter gewählte Quellen antworteten den Redakteuren mit 403 |
| Inhalt | Leitartikel genau belegt, beide Seiten zitiert | Midterms-Story ruhte nur auf einer AP-Analyse (jetzt Regel: Kurzmeldung) |
| Verbrauch | ~1/3 weniger je Claim als im ersten Lauf, Verschiebung zu kleinen Modellen | ~60 % des Verbrauchs sind Fixkosten der 18 Agentenstarts |

## Umgesetzt

| Maßnahme | Wirkung | Art |
|---|---|---|
| Zweiter Versuch für ausgefallene Quellen nach 45 s (`collect.py`); „Today“-Hinweis nur bei endgültigem Ausfall (`failedSources`) | Keine leeren Video-/Rüstungsbereiche mehr durch kurze Ausfälle | Qualität, 0 Tokens |
| Erreichbarkeit der Kandidaten-Quellen vor dem Schiedsrichter (`prefetch.py --candidates` → `reach.json`) | Schiedsrichter plant nur mit Quellen, die antworten; Seiten liegen danach schon im Seiten-Speicher | Qualität, weniger Nachsuche |
| Prüfpaket für Prüfer A (`packets.py`): je Claim die Sätze mit Marker und die Zitate mit Umgebungstext | A muss Seiten kaum noch öffnen (im Lauf 2: 29 Werkzeugaufrufe) | Tokens (geschätzt −40 bis −60 Tsd. je Prüfdurchgang) |
| Fehlerkatalog im Redakteurs-Brief (Überdehnung, falsche Zuschreibung, eigene Rechnung, Agentur-Kennung, Dek) | Weniger Ablehnungen → kleinere Rückschleife (R3 + Nachprüfung kosteten 304 Tsd. für 9 Claims) | Tokens + Qualität |
| Briefs verweisen nicht mehr auf das Lesen von CLAUDE.md (ist ohnehin geladen) | Ein Werkzeugaufruf weniger je Agent | Tokens |
| Namen von Abgeordneten: `data/members.json` als Quelle für Redakteure und Prüfer B | Kein „Korrigieren“ richtiger Namen mehr | Qualität |
| Kernaussagen mindestens `multiple`: R3 sucht einmal eine zweite Quelle, sonst wird die Story per Code zur Kurzmeldung (`apply_verdicts.py`, `demoted.json`, `assemble.py`); Maschinen-Check prüft es | Keine vollen Storys auf einer einzigen Quelle | Qualität |
| Feste Regel nach der Nachprüfung jetzt Code: Story fällt bei ungeprüfter Kernaussage, abgelehnte Nebenaussagen samt Satz entfernt | Kein Handeingriff des Orchestrators mehr | Ablauf |
| Historiker + Verfahrens-Erklärer = ein Agent | −1 Agentenstart (~70–80 Tsd.) | Tokens |
| CLAUDE.md um ~20 % gekürzt (Details nach `docs/00-projektstand.md`), Pipeline-Regeln aktualisiert | Weniger Kontext in jedem Agentenschritt | Tokens |
| Erneutes Zusammenbauen behält die ursprüngliche Erstellungszeit | Korrekturen ändern die angezeigte Uhrzeit nicht | Korrektheit |

Die Ausgabe vom 18.10. wurde nach der neuen Regel neu zusammengebaut: Die Midterms-Story steht jetzt als zugeschriebene
Kurzmeldung unter Also Notable.

## Erwartung für den nächsten Lauf (Schätzung, noch nicht gemessen)

- Gleicher Umfang wie Lauf 2: etwa 1,7–1,8 statt 2,1 Mio. Tokens (−1 Agentenstart, kleinere Prüfdurchgänge, seltener R3).
- In der Routine fehlen die persönlichen Konnektoren dieser Entwicklungssitzung (Gamma, Drive, Moda …); jeder Agent
  startet dort mit weniger Werkzeugbeschreibungen. Wie viel das spart, zeigt erst ein Lauf in der Routine.
- Nicht gemessen ist der Verbrauch des Orchestrators selbst (die Sitzung, die die Agenten startet).

## Bewusst nicht gemacht

- Prüfer A und B zusammenlegen oder Prüfungen bündeln (Andreas' Entscheidung; die Gegenproben fanden in beiden Läufen Fehler).
- Türsteher + Bündler zusammenlegen (Andreas' Entscheidung 18.10.2026).
- Gegenagent streichen: Er fand in Lauf 2 die veraltete War-Powers-Meldung.
