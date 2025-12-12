#!/usr/bin/env python3
"""
Truly final fix for the last few Norwegian phrases.
"""

from pathlib import Path

# The truly last Norwegian translations
TRULY_FINAL_TRANSLATIONS = {
    "Toppnavigasjon med brukerinfo, hjelpikon og handlinger": "Top navigation with user info, help icon and actions",
    "Gratulerer! Brukeren have fullført simuleringen": "Congratulations! The user has completed the simulation",
    "Prosjektet forsinket til 20. mai 2026": "Project delayed until 20. May 2026",
    "Gratulerer!": "Congratulations!",
    "Brukeren": "The user",
    "fullført": "completed",
    "simuleringen": "simulation",
    "Prosjektet": "Project",
    "forsinket": "delayed",
    "Toppnavigasjon": "Top navigation",
    "brukerinfo": "user info",
    "hjelpikon": "help icon",
    "handlinger": "actions",
    "mai": "May",
}

def truly_final_fix(file_path: Path) -> bool:
    """Apply truly final fixes."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content

        # Sort by length (longest first)
        sorted_trans = sorted(TRULY_FINAL_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)

        for norwegian, english in sorted_trans:
            content = content.replace(norwegian, english)

        if content != original:
            file_path.write_text(content, encoding='utf-8')
            print(f"[OK] Fixed: {file_path.name}")
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

    print(f"Truly final fix for {len(files)} files\n")

    count = 0
    for file in files:
        if truly_final_fix(file):
            count += 1

    print(f"\nComplete! Fixed: {count}/{len(files)} files")

if __name__ == "__main__":
    main()
