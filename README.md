# KWK Index

Custom Integration für Home Assistant, die den offiziellen EEX KWK-Index aus der XLSX-Datei liest und als Sensor in `ct/kWh` bereitstellt.

> **Status**: ✅ HACS-ready | Unterstützung für Q1 2026

## 📋 Überblick

Die KWK-Index Integration ermöglicht die automatische Integration des aktuellen KWK-Baseloadpreises in Home Assistant. Der Sensor wird alle 12 Stunden aktualisiert und liefert den Preis vom offiziellen EEX-Index in Cent pro Kilowattstunde.

## 🚀 Installation

### Option 1: HACS (empfohlen)

1. Öffne HACS in Home Assistant
2. Klicke auf das Menü (☰) oben rechts
3. Wähle **Custom repositories**
4. Füge diese URL ein: `https://github.com/JackONeill199/ha-kwk-index`
5. Wähle **Integration** als Kategorie
6. Suche nach **KWK Index** und installiere es
7. Starte Home Assistant neu
8. Gehe zu **Einstellungen → Geräte & Dienste → Integration hinzufügen**
9. Suche nach **KWK Index** und folge der Konfiguration

### Option 2: Manuelle Installation

1. Klone das Repository oder lade es herunter
2. Kopiere den Ordner `custom_components/kwk_index/` in dein Home Assistant Konfigurationsverzeichnis unter `custom_components/`
3. Starte Home Assistant neu
4. Gehe zu **Einstellungen → Geräte & Dienste → Integration hinzufügen**
5. Suche nach **KWK Index**

## ⚙️ Konfiguration

Nach der Installation wird die Integration automatisch konfiguriert. Die vorgeschlagene EEX-XLSX-URL kann übernommen oder angepasst werden.

**Standard-Sensor:** `sensor.kwk_baseloadpreis`

Dieser Sensor liefert den aktuellen KWK-Baseloadpreis in `ct/kWh`.

## 📊 Sensor-Attribute

| Attribut | Beschreibung | Beispiel |
|----------|-------------|---------|
| `quarter` | Quartal der Preisbildung | Q1 2026 |
| `price_eur_per_mwh` | Originalwert aus der EEX-Datei | 102.15 EUR/MWh |
| `source` | Verwendete XLSX-URL | https://www.eex.com/... |

## 📈 Datenquelle

Die Integration nutzt die offizielle **EEX-KWK-XLSX-Datei**. 

EEX beschreibt den KWK-Index als Durchschnitt der Final Settlement Prices für Base Day Futures in Deutschland.

**Umrechnung:**
- Input: `102.15 EUR/MWh`
- Output: `10.215 ct/kWh`

Der KWK-Index wird **quartalsweise** kurz nach Quartalsende aktualisiert. Die Integration prüft alle 12 Stunden auf neue Daten.

## 🔧 Zur HACS-Standard-Liste beitragen

Dieses Repository ist bereits für HACS vorbereitet:

- ✅ `hacs.json` im Repository-Root
- ✅ Integration unter `custom_components/kwk_index`
- ✅ `manifest.json` mit Domain, Dokumentation, Issue Tracker
- ✅ Brand-Assets unter `custom_components/kwk_index/brand`
- ✅ GitHub Actions für Validierung

Für die Aufnahme in die **HACS-Default-Liste** noch erforderlich:
- [ ] GitHub Release (z.B. `v1.0.0`)
- [ ] Pull Request in `hacs/default` (Datei: `integration`)

## 🐛 Troubleshooting

### Integration wird nicht gefunden
- Stelle sicher, dass der `custom_components` Ordner korrekt kopiert wurde
- Überprüfe die `manifest.json` auf Syntax-Fehler
- Cleere den Browser-Cache oder starte Home Assistant neu

### Sensor zeigt keine Daten
- Überprüfe, ob die EEX-XLSX-URL erreichbar ist
- Prüfe die Home Assistant Logs auf Fehlermeldungen
- Stelle sicher, dass das aktuelle Quartal verfügbar ist

## 📝 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.

## 🤝 Support

Für Fragen und Probleme bitte ein Issue auf GitHub erstellen.