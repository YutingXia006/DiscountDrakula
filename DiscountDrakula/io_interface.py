def parse_txt(dateipfad: str) -> dict:
    result = {}
    kategorie = None
    with open(dateipfad, "r", encoding="utf-8") as f:
        for zeile in f:
            zeile = zeile.strip()
            if not zeile:
                continue
            if zeile.startswith("[") and zeile.endswith("]"):
                kategorie = zeile[1:-1]
                result[kategorie] = []
            elif kategorie:
                result[kategorie].append(zeile)
    return result

def format_kategorien(daten: dict) -> str:
    lines = []
    for kategorie, eintraege in daten.items():
        lines.append(f"\n[{kategorie}]")
        lines.extend(f"  - {e}" for e in eintraege)
    return "\n".join(lines)

def format_angebote(angebote: dict, preise: bool) -> str:
    lines = []
    if preise:
        for markt, items in angebote.items():
            lines.append(f"\n{markt}:")
            for item in items:
                lines.append(f"  - {item['name']}: {item['price_eur']}€")
        return "\n".join(lines)
    else:
        for markt, items in angebote.items():
            lines.append(f"\n{markt}:")
            for item in items:
                lines.append(f"  - {item['name']}")
        return "\n".join(lines)