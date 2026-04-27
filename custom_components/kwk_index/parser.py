"""Parser for EEX KWK Index XLSX files."""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
import re
import zipfile
from xml.etree import ElementTree

_NS = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
_QUARTER_RE = re.compile(r"^Q([1-4])\s+(\d{4})$")


@dataclass(frozen=True, slots=True)
class KwkIndexValue:
    """A parsed KWK index value."""

    price_ct_per_kwh: float
    price_eur_per_mwh: float
    quarter: str
    quarter_number: int
    year: int


def parse_kwk_xlsx(content: bytes) -> KwkIndexValue:
    """Parse the latest KWK index from an EEX XLSX file."""
    rows = _read_rows(content)

    for row in rows:
        if len(row) < 2:
            continue

        quarter = row[0].strip()
        match = _QUARTER_RE.match(quarter)
        if not match:
            continue

        try:
            price_eur_per_mwh = float(row[1])
        except ValueError:
            continue

        quarter_number = int(match.group(1))
        year = int(match.group(2))

        return KwkIndexValue(
            price_ct_per_kwh=round(price_eur_per_mwh / 10, 3),
            price_eur_per_mwh=round(price_eur_per_mwh, 3),
            quarter=quarter,
            quarter_number=quarter_number,
            year=year,
        )

    raise ValueError("No KWK quarter rows found")


def _read_rows(content: bytes) -> list[list[str]]:
    """Read string values from the first worksheet in an XLSX document."""
    try:
        with zipfile.ZipFile(BytesIO(content)) as archive:
            shared_strings = _read_shared_strings(archive)
            sheet = ElementTree.fromstring(archive.read("xl/worksheets/sheet1.xml"))
    except (KeyError, zipfile.BadZipFile, ElementTree.ParseError) as err:
        raise ValueError("Invalid XLSX document") from err

    rows: list[list[str]] = []
    for row in sheet.findall(".//x:row", _NS):
        values: list[str] = []
        for cell in row.findall("x:c", _NS):
            values.append(_read_cell(cell, shared_strings))
        rows.append(values)

    return rows


def _read_shared_strings(archive: zipfile.ZipFile) -> list[str]:
    """Read XLSX shared strings."""
    try:
        root = ElementTree.fromstring(archive.read("xl/sharedStrings.xml"))
    except KeyError:
        return []

    strings: list[str] = []
    for item in root.findall("x:si", _NS):
        text = "".join(node.text or "" for node in item.findall(".//x:t", _NS))
        strings.append(text)
    return strings


def _read_cell(cell: ElementTree.Element, shared_strings: list[str]) -> str:
    """Read a single XLSX cell value."""
    value = cell.find("x:v", _NS)
    if value is None or value.text is None:
        return ""

    if cell.attrib.get("t") == "s":
        try:
            return shared_strings[int(value.text)]
        except (IndexError, ValueError):
            return ""

    return value.text
