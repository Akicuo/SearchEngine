# Projekt-Einrichtung

Um dieses Projekt erfolgreich einzurichten, befolgen Sie bitte die nachfolgenden Schritte:

## Voraussetzungen

Stellen Sie sicher, dass Python und Git auf Ihrem System installiert sind. Falls nicht, können Sie die neuesten Versionen hier herunterladen:

- [Python herunterladen](https://www.python.org/downloads/)
- [Git herunterladen](https://git-scm.com/downloads)

## Projekt klonen

Klonen Sie das GitHub-Repository auf Ihren lokalen Rechner:

```bash
git clone https://github.com/ihr-repository-link.git
```

## Virtuelle Umgebung einrichten

Navigieren Sie in das geklonte Verzeichnis und erstellen Sie eine virtuelle Python-Umgebung:

```bash
cd ihr-repository-verzeichnis
python -m venv venv
```

Aktivieren Sie die virtuelle Umgebung:

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

## Abhängigkeiten installieren

Installieren Sie die erforderlichen Abhängigkeiten mit pip:

```bash
pip install -r requirements.txt
```

## Konfigurationsdatei einrichten

Erstellen Sie eine `config.json`-Datei im Stammverzeichnis des Projekts und fügen Sie die folgenden sensiblen Daten hinzu:

```json
{
    "SERPER_DEV_API_KEY": "x",
    "DB_HOST_URL": "x",
    "DB_USER": "x",
    "DB_PASSWORD": "x"
}
```

### API-Schlüssel von Serper.dev erhalten

Um den `SERPER_DEV_API_KEY` zu erhalten, gehen Sie wie folgt vor:

1. Besuchen Sie [serper.dev](https://serper.dev) und erstellen Sie ein Konto.
2. Kopieren Sie den API-Schlüssel aus Ihrem Dashboard.
3. Fügen Sie den kopierten Schlüssel in die `config.json`-Datei ein.

## Fertig!

Sie haben das Projekt erfolgreich eingerichtet und können nun mit der Nutzung beginnen. Bei Fragen oder Problemen wenden Sie sich bitte an den Projektbetreuer.

Viel Erfolg! 🚀