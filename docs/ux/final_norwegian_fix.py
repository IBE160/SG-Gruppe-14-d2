#!/usr/bin/env python3
"""
Final targeted fix for remaining Norwegian phrases.
"""

from pathlib import Path

# Exact remaining Norwegian phrases to fix
EXACT_FIXES = {
    "Velg WBS-oppgaver å forhandle": "Select WBS tasks to negotiate",
    "Chat med 5 unike leverandør-personligheter": "Chat with 5 unique supplier personalities",
    "Bruk strategier som partnerskap, volum, or fleksibilitet": "Use strategies like partnership, volume, or flexibility",
    "partnerskap": "partnership",
    "volum": "volume",
    "fleksibilitet": "flexibility",
    "leverandør-personligheter": "supplier personalities",
    "personligheter": "personalities",
    "WBS-oppgaver": "WBS tasks",
    "å forhandle": "to negotiate",
    "strategier": "strategies",
    "unike": "unique",
    "Tips:": "Tip:",
}

def final_fix(file_path: Path) -> bool:
    """Apply final targeted fixes."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content

        # Sort by length (longest first) to avoid partial replacements
        sorted_fixes = sorted(EXACT_FIXES.items(), key=lambda x: len(x[0]), reverse=True)

        for norwegian, english in sorted_fixes:
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

    print(f"Final targeted fix for {len(files)} files\n")

    count = 0
    for file in files:
        if final_fix(file):
            count += 1

    print(f"\nComplete! Fixed: {count}/{len(files)} files")

if __name__ == "__main__":
    main()
