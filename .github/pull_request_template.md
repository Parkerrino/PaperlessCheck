<!-- Nicht zutreffende Abschnitte und Prüfpunkte entfernen. Keine Secrets oder personenbezogenen Daten eintragen. -->

## Zusammenfassung

<!-- Welches Problem löst dieser PR? Was ändert sich für Nutzer? Bei Bugs: Verhalten vorher → nachher. -->


## Issue / Roadmap

<!-- Beispiel: Closes #123. Bei Teilumsetzung: Refs #123. -->


## Art der Änderung

- [ ] Bugfix
- [ ] Feature
- [ ] Refactoring
- [ ] Dokumentation
- [ ] Abhängigkeiten / Security
- [ ] CI/CD / Docker
- [ ] Breaking Change

## Änderungen

<!-- Wichtigste Änderungen und gegebenenfalls die Begründung der Lösung. -->

- 

## Tests und Nachweise

<!-- Tatsächlich ausgeführte Tests nennen. Übersprungene oder fehlgeschlagene Checks begründen. -->

| Prüfung | Ergebnis / Nachweis |
| --- | --- |
| Backend: Ruff / Black | |
| Backend: pytest | |
| Integration mit PostgreSQL | |
| Frontend: Build / relevante Tests | |
| Docker: Build / Start | |
| Blackbox-Test des betroffenen Nutzerablaufs | |

### Manuelle Prüfung

<!-- Reproduzierbare Schritte, erwartetes und tatsächliches Ergebnis. Bei Bugfixes auch den ursprünglichen Fehler prüfen. -->

1. 
2. 
3. 

### Screenshots

<!-- Bei sichtbaren UI-Änderungen Vorher/Nachher ergänzen; sonst entfernen. -->


## Sicherheit und Daten

<!-- Nur für den Änderungsumfang relevante Punkte behalten. -->

- [ ] Eingaben werden validiert; Fehler werden ohne sensible Details ausgegeben.
- [ ] Berechtigungen werden serverseitig geprüft, einschließlich Zugriff auf fremde Aufgaben/Daten.
- [ ] Keine Secrets oder personenbezogenen Daten in Code, Testdaten, Logs oder Screenshots.
- [ ] Geänderte Abhängigkeiten auf bekannte Schwachstellen geprüft; offene Befunde unten dokumentiert.

**Offene Befunde / Einschränkungen:**

<!-- Bei Security-Fixes keine Details zu noch nicht öffentlich behobenen Schwachstellen veröffentlichen. -->


## Kompatibilität und Deployment

<!-- Bei reinen Dokumentationsänderungen entfernen. -->

- **API-/Verhaltensänderungen:** Keine / Beschreibung
- **Datenbankmigrationen:** Keine / Durchführung und Auswirkungen auf Bestandsdaten
- **Neue oder geänderte Konfiguration:** Keine / Variablennamen und sichere Defaults
- **Deployment-Schritte:** Standard / zusätzliche Schritte
- **Rollback:** Vorgehen; bei Migrationen mögliche Grenzen oder Datenverlust nennen

## Review-Checkliste

- [ ] Änderung ist auf den beschriebenen Zweck begrenzt.
- [ ] Code ist verständlich; gemeinsame Logik ist sinnvoll gekapselt.
- [ ] Relevante Fehlerfälle und Regressionen sind geprüft.
- [ ] Dokumentation und Konfigurationsbeispiele sind bei Bedarf aktualisiert.
- [ ] Relevante CI-Checks sind erfolgreich; Ausnahmen sind oben begründet.
- [ ] Breaking Changes und notwendige Deployment-Schritte sind beschrieben.

## Hinweise für Reviewer

<!-- Kritische Stellen, bewusste Abwägungen und verbleibende Arbeit. -->
