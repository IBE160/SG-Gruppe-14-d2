#!/usr/bin/env python3
"""
Absolute final fix for the last remaining Norwegian phrases.
"""

from pathlib import Path

# The absolute last Norwegian translations
ABSOLUTE_FINAL_TRANSLATIONS = {
    # Complete phrases (longest first)
    "Komplett Userreise - Nye Hædda Barneskole PM Simulator": "Complete User Journey - Nye Hædda School PM Simulator",
    "Kom i gang med Nye Hædda Barneskole Simulator": "Get started with Nye Hædda School Simulator",
    "Modal - Hjelp og Onboarding": "Modal - Help and Onboarding",
    "Veiledning for nye brukere - Hvordan spille simulatoren": "Guidance for new users - How to play the simulator",
    "Velkommen til Simulatoren!": "Welcome to the Simulator!",
    "Lær hvordan du planlegger Nye Hædda Barneskole prosjektet": "Learn how to plan the Nye Hædda School project",
    "Start simulatoren →": "Start simulator →",
    "\"Start simulatoren\" → Marker first_visit = false": "\"Start simulator\" → Mark first_visit = false",
    "Onboarding for nye brukere": "Onboarding for new users",
    "planleggingsfasen for Nye Hædda Barneskole.": "planning phase for Nye Hædda School.",
    "Klikk \"?\" → Hjelp/onboarding modal (nhb-18)": "Click \"?\" → Help/onboarding modal (nhb-18)",
    "Nye Hædda Barneskole PM Simulator": "Nye Hædda School PM Simulator",
    "Nye Hædda Barneskole": "Nye Hædda School",

    # Individual words
    "Komplett": "Complete",
    "Userreise": "User Journey",
    "Hjelp": "Help",
    "Veiledning": "Guidance",
    "brukere": "users",
    "Hvordan": "How",
    "spille": "play",
    "simulatoren": "simulator",
    "Velkommen": "Welcome",
    "Simulatoren": "Simulator",
    "Lær": "Learn",
    "hvordan": "how",
    "planlegger": "plan",
    "prosjektet": "project",
    "planleggingsfasen": "planning phase",
    "Barneskole": "School",
    "Klikk": "Click",
    "Marker": "Mark",
}

def absolute_final_fix(file_path: Path) -> bool:
    """Apply absolute final fixes."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content

        # Sort by length (longest first)
        sorted_trans = sorted(ABSOLUTE_FINAL_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)

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

    print(f"Absolute final fix for {len(files)} files\n")

    count = 0
    for file in files:
        if absolute_final_fix(file):
            count += 1

    print(f"\nComplete! Fixed: {count}/{len(files)} files")

if __name__ == "__main__":
    main()
