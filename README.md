#  Planer – Einfaches Aufgabenplanungstool mit Python & Flask

Dieses Projekt ist ein einfacher Wochenplaner mit Drag & Drop, Filterung und Statistikansicht.

##  Features

- Aufgaben erstellen, verschieben, bearbeiten, löschen
- Filter nach Verantwortlichen, Priorität und Thema
- Wochenbasierte Ansicht
- Themenstatistiken (mit Chart.js)
- Datenspeicherung via CSV

##  Tech Stack

- Python + Flask (Backend)
- HTML + CSS + JavaScript (Frontend)
- Chart.js (Diagramme)
- pandas (CSV-Verarbeitung)


## Voraussetzungen

- Python 3.9+
- pip
- Virtuelle Umgebung empfohlen


##  Lokale Installation

```bash
# Repository klonen
git clone https://github.com/vickyola/planer-projekt.git
cd planer-projekt

# Virtuelle Umgebung (optional aber empfohlen)
python -m venv venv
source venv/bin/activate    # oder: .\venv\Scripts\activate auf Windows

# Abhängigkeiten installieren
pip install -r requirements.txt

```

## Projekt Starten

```bash
# Starte den Flask-Entwicklungsserver:
flask --app app run
```