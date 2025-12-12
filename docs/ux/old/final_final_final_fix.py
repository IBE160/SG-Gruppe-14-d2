#!/usr/bin/env python3
"""
Final final final fix for ALL remaining Norwegian text.
"""

from pathlib import Path

# The final final final Norwegian translations
FINAL_FINAL_FINAL_TRANSLATIONS = {
    # Complete phrases (longest first)
    "Lagre regelmessig med \"Eksporter økt\" for å not miste fremgangen din": "Save regularly with \"Export session\" to not lose your progress",
    "Sjekk kritisk sti i Gantt-diagrammet for å identifisere flaskehalser": "Check critical path in Gantt chart to identify bottlenecks",
    "Ingen buffer - forsinkelser påvirker sluttdato": "No buffer - delays affect end date",
    "Dette vil update prosjektplanen din.": "This will update your project plan.",
    "Congratulations! Du have lykkes med å fullføre": "Congratulations! You have succeeded in completing",
    "Budsjett overskredet med 50 MNOK": "Budget exceeded by 50 MNOK",
    "Tips: Fokuser på de tre dyreste oppgavene først. En reduksjon på 10-15%": "Tip: Focus on the three most expensive tasks first. A reduction of 10-15%",
    "i disse vil bringe deg under budsjettet.": "in these will bring you under budget.",
    "Tilbake til Planlegging": "Back to Planning",
    "Har du allerede en konto?": "Already have an account?",
    "Pragmatisk og erfaren,": "Pragmatic and experienced,",
    "⟲ Tilbakestill til dette punktet": "⟲ Reset to this point",

    # Individual words/phrases
    "Lagre": "Save",
    "regelmessig": "regularly",
    "Eksporter økt": "Export session",
    "miste": "lose",
    "fremgangen": "progress",
    "Sjekk": "Check",
    "kritisk sti": "critical path",
    "Gantt-diagrammet": "Gantt chart",
    "identifisere": "identify",
    "flaskehalser": "bottlenecks",
    "Ingen": "No",
    "buffer": "buffer",
    "forsinkelser": "delays",
    "påvirker": "affect",
    "sluttdato": "end date",
    "Dette": "This",
    "vil": "will",
    "prosjektplanen": "project plan",
    "din": "your",
    "lykkes": "succeeded",
    "fullføre": "completing",
    "overskredet": "exceeded",
    "Tips": "Tip",
    "Fokuser": "Focus",
    "tre": "three",
    "dyreste": "most expensive",
    "oppgavene": "tasks",
    "først": "first",
    "reduksjon": "reduction",
    "disse": "these",
    "vil bringe": "will bring",
    "deg": "you",
    "under": "under",
    "budsjettet": "budget",
    "Planlegging": "Planning",
    "allerede": "already",
    "konto": "account",
    "Pragmatisk": "Pragmatic",
    "erfaren": "experienced",
    "Tilbakestill": "Reset",
    "punktet": "point",
}

def final_final_final_fix(file_path: Path) -> bool:
    """Apply final final final fixes."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content

        # Sort by length (longest first)
        sorted_trans = sorted(FINAL_FINAL_FINAL_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)

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

    print(f"Final final final fix for {len(files)} files\n")

    count = 0
    for file in files:
        if final_final_final_fix(file):
            count += 1

    print(f"\nTranslation COMPLETE! Fixed: {count}/{len(files)} files")

if __name__ == "__main__":
    main()
