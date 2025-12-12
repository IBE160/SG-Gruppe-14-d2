#!/usr/bin/env python3
"""
Final comprehensive fix for all remaining Norwegian text.
This ensures every Norwegian word is translated to English.
"""

from pathlib import Path

# Comprehensive final translations
FINAL_TRANSLATIONS = {
    # Remaining Norwegian words and phrases
    "Velg": "Select",
    "velg": "select",
    "oppgaver fra prosjektering til ferdigstillelse": "tasks from design to completion",
    "Negotiate med AI-leverandører": "Negotiate with AI suppliers",
    "Chat med 5 unike leverandør-personligheter": "Chat with 5 unique supplier personalities",
    "Bruk strategier som partnerskap, volum, or fleksibilitet": "Use strategies like partnership, volume, or flexibility",
    "unike leverandør-personligheter": "unique supplier personalities",
    "leverandør-personligheter": "supplier personalities",
    "fra prosjektering til ferdigstillelse": "from design to completion",
    "prosjektering": "design",
    "ferdigstillelse": "completion",
    "med AI-leverandører": "with AI suppliers",
    "strategier som partnerskap": "strategies like partnership",
    "volum": "volume",
    "fleksibilitet": "flexibility",
    "som partnerskap": "like partnership",
    "volum eller fleksibilitet": "volume or flexibility",

    # More task-related
    "å forhandle": "to negotiate",
    "til ferdigstillelse": "to completion",
    "unike": "unique",

    # Date formats
    "15. May 2026": "May 15, 2026",
    "1. apr 2025": "Apr 1, 2025",
    "15. jan 2025": "Jan 15, 2025",
    "10. april 2026": "April 10, 2026",
    "20. mai 2026": "May 20, 2026",

    # Common remaining Norwegian words
    "med": "with",
    "eller": "or",
    "til": "to",
    "fra": "from",
    "og": "and",
    "for": "for",
    "på": "on",
    "i": "in",
    "av": "of",
    "som": "like",
    "ved": "at",
    "etter": "after",
    "før": "before",
    "under": "under",
    "over": "over",
    "mellom": "between",
    "gjennom": "through",
    "rundt": "around",
    "om": "about",
    "når": "when",
    "hvor": "where",
    "hvordan": "how",
    "hvorfor": "why",
    "hva": "what",
    "hvem": "who",
    "hvis": "if",
    "fordi": "because",
    "men": "but",
    "så": "so",
    "da": "then",
    "nå": "now",
    "her": "here",
    "der": "there",
    "dette": "this",
    "det": "that",
    "disse": "these",
    "de": "those",
    "alle": "all",
    "noen": "some",
    "mange": "many",
    "få": "few",
    "flere": "more",
    "mest": "most",
    "minst": "least",
    "ny": "new",
    "gammel": "old",
    "stor": "large",
    "liten": "small",
    "god": "good",
    "dårlig": "bad",
    "høy": "high",
    "lav": "low",
    "første": "first",
    "siste": "last",
    "neste": "next",
    "forrige": "previous",
    "annen": "other",
    "samme": "same",
    "forskjellig": "different",
    "lik": "similar",
    "viktig": "important",
    "nødvendig": "necessary",
    "mulig": "possible",
    "umulig": "impossible",
    "enkel": "simple",
    "kompleks": "complex",
    "lett": "easy",
    "vanskelig": "difficult",
    "rask": "fast",
    "langsom": "slow",
    "tidlig": "early",
    "sen": "late",
}

def final_fix_file(file_path: Path) -> bool:
    """Apply final translation fixes."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content

        # Sort by length (longest first) to avoid partial replacements
        sorted_translations = sorted(FINAL_TRANSLATIONS.items(),
                                    key=lambda x: len(x[0]), reverse=True)

        for norwegian, english in sorted_translations:
            content = content.replace(norwegian, english)

        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            print(f"[OK] Fixed: {file_path.name}")
            return True
        else:
            print(f"[--] No changes: {file_path.name}")
            return False

    except Exception as e:
        print(f"[ERROR] Error: {file_path.name}: {e}")
        return False

def main():
    ux_dir = Path(__file__).parent
    svg_files = sorted(ux_dir.glob("nhb-*.svg"))

    print(f"Final fix for {len(svg_files)} files\n")

    fixed = 0
    for svg_file in svg_files:
        if final_fix_file(svg_file):
            fixed += 1

    print(f"\nComplete! Fixed: {fixed}/{len(svg_files)} files")

if __name__ == "__main__":
    main()
