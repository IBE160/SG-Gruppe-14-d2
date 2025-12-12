#!/usr/bin/env python3
"""
Complete final translation - handles all remaining Norwegian text.
"""

from pathlib import Path

# All remaining translations
COMPLETE_TRANSLATIONS = {
    # Typo fix
    "volumee": "volume",

    # Full sentences
    "Save regelmessig med \"Export session\" for å ikke miste fremgangen din": "Save regularly with \"Export session\" to not lose your progress",
    "Sjekk kritisk sti i Gantt Chartmet for å identifisere flaskehalser": "Check critical path in Gantt chart to identify bottlenecks",
    "Hopp over": "Skip",
    "Start simulatoren →": "Start simulator →",
    "Når vises denne modalen?": "When does this modal appear?",
    "Første gang brukeren logger inn (localStorage: first_visit = true)": "First time user logs in (localStorage: first_visit = true)",
    "Manuelt via \"?\" ikon i navigasjonsfeltet": "Manually via \"?\" icon in navigation bar",
    "Interaksjoner:": "Interactions:",
    "\"Hopp over\" → Lukk modal → Dashboard": "\"Skip\" → Close modal → Dashboard",
    "\"Start simulatoren\" → Marker first_visit = false": "\"Start simulator\" → Mark first_visit = false",
    "→ Lukk modal → Dashboard": "→ Close modal → Dashboard",
    "Marker": "Mark",
    "Lukk modal": "Close modal",
    "logger inn": "logs in",
    "brukeren": "user",
    "Første gang": "First time",
    "regelmessig": "regularly",
    "for å ikke": "to not",
    "miste": "lose",
    "fremgangen din": "your progress",
    "Sjekk": "Check",
    "kritisk sti": "critical path",
    "Gantt Chartmet": "Gantt chart",
    "for å": "to",
    "identifisere": "identify",
    "flaskehalser": "bottlenecks",
    "vises": "appear",
    "modalen": "modal",
    "ikon": "icon",
    "navigasjonsfeltet": "navigation bar",
}

def complete_translation(file_path: Path) -> bool:
    """Apply complete final translation."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content

        # Sort by length (longest first)
        sorted_trans = sorted(COMPLETE_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)

        for norwegian, english in sorted_trans:
            content = content.replace(norwegian, english)

        if content != original:
            file_path.write_text(content, encoding='utf-8')
            print(f"[OK] Translated: {file_path.name}")
            return True
        else:
            print(f"[--] No changes: {file_path.name}")
            return False
    except Exception as e:
        print(f"[ERROR] {file_path.name}: {e}")
        return False

def main():
    ux_dir = Path(__file__).parent
    files = sorted(ux_dir.glob("nhb-*.svg"))

    print(f"Complete translation of {len(files)} files\n")

    count = 0
    for file in files:
        if complete_translation(file):
            count += 1

    print(f"\nAll translations complete! Fixed: {count}/{len(files)} files")

if __name__ == "__main__":
    main()
