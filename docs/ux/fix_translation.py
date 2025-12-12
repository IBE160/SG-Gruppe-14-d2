#!/usr/bin/env python3
"""
Fix translation issues and complete missed translations.
This script fixes CSS class names and adds missing translations.
"""

from pathlib import Path
import re

# Fix CSS class names that were incorrectly translated
CSS_FIXES = {
    "title-Mayn": "title-main",
    "subtitle-Mayn": "subtitle-main",
    "button-priMary": "button-primary",
    "button-text-priMary": "button-text-primary",
    "card-Mayn": "card-main",
}

# Additional translations that were missed
ADDITIONAL_TRANSLATIONS = {
    # Welcome messages
    "Velkommen til Simulatoren!": "Welcome to the Simulator!",
    "Lær hvordan du planlegger Nye Hædda Barneskole prosjektet": "Learn how to plan the Nye Hædda School project",
    "Lær hvordan du planlegger Nye Hædda Skole prosjektet": "Learn how to plan the Nye Hædda School project",

    # Instructions and steps
    "Forstå budsjettet og tidsfristen": "Understand the budget and deadline",
    "Du må holde deg innenfor disse grensene for å lykkes": "You must stay within these limits to succeed",
    "Velg WBS-oppgaver å forhandle om": "Select WBS tasks to negotiate",
    "oppgaver fra design til ferdigstillelse": "tasks from design to completion",
    "Start med avhengige oppgaver (grunnarbeid først)": "Start with dependent tasks (foundation work first)",
    "Forhandle med AI-leverandører": "Negotiate with AI suppliers",
    "Chat med 5 unike leverandørpersonligheter": "Chat with 5 unique supplier personalities",
    "Bruk strategier som partnerskap, volum eller fleksibilitet": "Use strategies like partnership, volume, or flexibility",
    "Send inn planen din": "Submit your plan",
    "Valider at planen oppfyller kravene": "Validate that the plan meets requirements",
    "Hvis feil oppstår, reforhandle de dyreste oppgavene": "If errors occur, renegotiate the most expensive tasks",

    # Tips and recommendations
    "Lagre regelmessig med \"Eksporter økt\" for ikke å miste fremgangen din": "Save regularly with \"Export session\" to not lose your progress",
    "Sjekk kritisk sti i Gantt-diagram for å identifisere flaskehalser": "Check critical path in Gantt chart to identify bottlenecks",

    # Modal appearance conditions
    "Første gang brukeren logger inn": "First time user logs in",
    "første_besøk": "first_visit",

    # Interactions
    "Marker": "Mark",
    "marker": "mark",
    "klikk": "click",
    "Lukk modal": "Close modal",

    # Additional task-related terms
    "15 oppgaver fra design til ferdigstillelse": "15 tasks from design to completion",
    "5 unike leverandørpersonligheter": "5 unique supplier personalities",
    "de dyreste oppgavene": "the most expensive tasks",

    # File footer descriptions
    "Onboarding for nye brukere": "Onboarding for new users",

    # Other miscellaneous
    "første_besøk = false": "first_visit = false",
}

def fix_svg_file(file_path: Path) -> bool:
    """Fix translation issues in a single SVG file."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content

        # First, fix CSS class names
        for wrong_class, correct_class in CSS_FIXES.items():
            content = content.replace(wrong_class, correct_class)

        # Then apply additional translations (sorted by length, longest first)
        sorted_additions = sorted(ADDITIONAL_TRANSLATIONS.items(),
                                 key=lambda x: len(x[0]), reverse=True)

        for norwegian, english in sorted_additions:
            content = content.replace(norwegian, english)

        # Check if anything changed
        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            print(f"[OK] Fixed: {file_path.name}")
            return True
        else:
            print(f"[--] No changes needed: {file_path.name}")
            return False

    except Exception as e:
        print(f"[ERROR] Error fixing {file_path.name}: {e}")
        return False

def main():
    """Main function to fix all SVG files."""
    ux_dir = Path(__file__).parent
    svg_files = sorted(ux_dir.glob("nhb-*.svg"))

    if not svg_files:
        print("No nhb-*.svg files found!")
        return

    print(f"Found {len(svg_files)} SVG files to fix\n")

    fixed = 0
    for svg_file in svg_files:
        if fix_svg_file(svg_file):
            fixed += 1

    print(f"\nFix complete!")
    print(f"Fixed: {fixed}/{len(svg_files)} files")

if __name__ == "__main__":
    main()
