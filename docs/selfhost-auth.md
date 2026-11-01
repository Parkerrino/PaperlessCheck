# Selfhost-Anmeldung

Alle Konten arbeiten im selben gemeinsamen Arbeitsbereich und können alle
Checklisten lesen und ändern. Es gibt in dieser Version keine privaten Listen,
Mandanten, Leserrolle oder öffentliche Registrierung. `create-admin` erstellt ein
solches voll berechtigtes Konto; weitere Konten werden ebenfalls lokal angelegt.

## Bestehende Installation aktualisieren

Vor dem Update Datenbank sichern. Das bisherige `database/init.sql` **nicht erneut
auf eine bestehende Datenbank anwenden**; es enthält Beispieldaten. Die folgende
Auth-Migration ist dagegen wiederholbar und verändert keine Checklisten:

```powershell
docker compose up -d --build
docker compose exec backend flask --app app init-auth
docker compose exec backend flask --app app create-admin admin
```

Die Passwortabfrage erfolgt verdeckt mit Bestätigung. Passwörter müssen 15–128
Zeichen lang sein. Benutzernamen bestehen aus 3–64 ASCII-Buchstaben, Zahlen,
Unterstrich, Punkt oder Bindestrich und werden kleingeschrieben gespeichert.
Keine Passwörter in CLI-Argumente, Git, VITE-Variablen oder Build-Args schreiben.
Neue Installationen benötigen ebenfalls `init-auth` und das erste Konto.
Ohne Migration/Konto ist die API nicht offen, sondern die Anmeldung nicht nutzbar.

## HTTPS und lokale Entwicklung

Für den Betrieb HTTPS am Reverse Proxy einrichten. `AUTH_COOKIE_SECURE=true`
ist der Standard. Frontend und API über denselben Ursprung bereitstellen (`/api`)
und Cookies/Header am Proxy durchreichen. Der direkte Backend-Port sollte für
Clients nicht öffentlich erreichbar sein. Keine pauschale CORS-Freigabe aktivieren.
Der bisherige Flask-Entwicklungsserver bleibt separat unter #61 zu ersetzen.

**Nur für lokale HTTP-Tests** in `.env` `AUTH_COOKIE_SECURE=false` setzen und den
Backend-Container neu erstellen. Für die Produktion wieder `true` verwenden.
Bei manuellem Backend-Start gilt dieselbe Umgebungsvariable; Vite verwendet `/api`.
Ein Secure-Cookie wird bei unverschlüsseltem Zugriff möglicherweise nicht gesendet.

## Sitzungen und Passwortwechsel

Passwörter werden mit Werkzeug/scrypt gehasht. Ein zufälliger Sitzungsschlüssel
liegt nur im HttpOnly-/SameSite=Strict-Cookie; PostgreSQL speichert seinen SHA-256-
Hash. Sitzungen laufen nach acht Stunden ab, werden beim Logout widerrufen und
bei einem Passwortwechsel vollständig gelöscht. Schreibzugriffe benötigen den
sitzungsgebundenen `X-CSRF-Token`; Login verlangt JSON und `X-Paperless-Login: 1`.
Der CSRF-Token liegt im Frontend nur im Arbeitsspeicher. Nach Neuladen liefert
`GET /api/auth/session` ihn erneut. Keine Auth-Tokens im Local Storage.

```powershell
docker compose exec backend flask --app app reset-password admin
```

Login-Versuche werden in PostgreSQL pro Benutzername (10) und Quell-IP (50) pro
15-Minuten-Fenster begrenzt, auch über mehrere Worker. Erfolgreiche Versuche
zählen mit. Proxy-Header werden nicht blind vertraut: hinter einem gemeinsamen
Proxy teilen Clients ggf. das IP-Limit. Ein Angreifer kann ein bekanntes Konto
vorübergehend blockieren; für größere Installationen ist zusätzlich abgestimmtes
Rate-Limiting am Proxy nötig. Öffentliche Health-Endpunkte geben nur Status zurück.

## Tests und Scan

Die CI führt einen echten PostgreSQL-Auth-Lifecycle aus: Migration wiederholen,
Login, anonyme Sperre, CSRF, Logout/Replay, Passwortwechsel, Ablauf und Rate-Limit.
Bestehende Route-Unit-Tests mocken ausschließlich die Sitzungsauflösung; es gibt
keinen Auth-Bypass-Schalter in der Anwendung.

ZAP verwendet ein ausschließlich im Wegwerf-Stack angelegtes Testkonto. Der Runner
prüft den Zugriff ohne Sitzung, führt einen HTTP-Login aus, prüft CSRF und reicht
Cookie/CSRF an ZAP weiter. Ein Hook setzt den CSRF-Header nur für `backend:5000`.
Nach dem Scan muss die Sitzung noch gültig sein. Berichte werden vor dem Upload
von den bekannten temporären Zugangsdaten bereinigt. Der Scanvertrag enthält nur
geschützte Checklist-Operationen; Login/Logout und öffentliche Health-Endpunkte
werden separat getestet. Der Scan beweist keine vollständige Zugriffskontrolle.
