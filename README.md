# KWK Index

Custom Integration fuer Home Assistant, die den offiziellen EEX KWK-Index aus der XLSX-Datei liest und als Sensor in `ct/kWh` bereitstellt.

## Installation ueber HACS

### Als Custom Repository

1. In HACS oben rechts das Menue oeffnen.
2. **Custom repositories** auswaehlen.
3. Repository-URL eintragen: `https://github.com/JackONeill199/ha-kwk-index`
4. Kategorie **Integration** waehlen und hinzufuegen.
5. **KWK Index** in HACS installieren.
6. Home Assistant neu starten.
7. Unter **Einstellungen > Geraete & Dienste > Integration hinzufuegen** nach **KWK Index** suchen.

### Manuell

1. Den Ordner `custom_components/kwk_index` in die Home-Assistant-Konfiguration kopieren.
2. Home Assistant neu starten.
3. Unter **Einstellungen > Geraete & Dienste > Integration hinzufuegen** nach **KWK Index** suchen.
4. Die vorgeschlagene EEX-XLSX-URL uebernehmen.

Der Sensor heisst standardmaessig `sensor.kwk_baseloadpreis` und liefert den aktuellen KWK Baseloadpreis in `ct/kWh`.

## HACS-Veröffentlichung

Dieses Repository ist fuer HACS vorbereitet:

- `hacs.json` liegt im Repository-Root.
- Die Integration liegt unter `custom_components/kwk_index`.
- `manifest.json` enthaelt Domain, Dokumentation, Issue Tracker, Codeowners, Name und Version.
- Brand-Assets liegen unter `custom_components/kwk_index/brand`.
- GitHub Actions fuer HACS Validation und Hassfest liegen unter `.github/workflows/validate.yml`.

Vor dem ersten Release sollten Repository-Beschreibung, Topics und Issues in GitHub gesetzt werden.

Fuer eine Aufnahme in die HACS-Default-Liste braucht das GitHub-Repository zusaetzlich:

- Public GitHub repository
- Beschreibung und Topics
- Issues aktiviert
- Gruene HACS- und Hassfest-Actions
- Einen GitHub Release, zum Beispiel `v0.1.0`
- Pull Request in `hacs/default` in der Datei `integration`, alphabetisch einsortiert

## Datenquelle

Die Integration nutzt die offizielle EEX-KWK-XLSX-Datei. EEX beschreibt den KWK-Index als Durchschnitt der Final Settlement Prices fuer Base Day Futures in Deutschland. Die XLSX-Datei enthaelt den Preis in `EUR/MWh`; die Integration rechnet nach `ct/kWh` um.

Beispiel: `102.15 EUR/MWh` wird zu `10.215 ct/kWh`.

## Attribute

- `quarter`: Quartal der Preisbildung, zum Beispiel `Q1 2026`
- `price_eur_per_mwh`: Originalwert aus der EEX-Datei
- `source`: verwendete XLSX-URL

## Hinweise

Der KWK-Index wird quartalsweise kurz nach Quartalsende aktualisiert. Die Integration fragt standardmaessig alle 12 Stunden ab, damit eine neue EEX-Datei zeitnah uebernommen wird.
