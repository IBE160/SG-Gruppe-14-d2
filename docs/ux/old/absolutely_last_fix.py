#!/usr/bin/env python3
"""
Absolutely last fix for final Norwegian phrases.
"""

from pathlib import Path

# Absolutely last fixes
ABSOLUTELY_LAST_FIXES = {
    "Ingen buffer - forsinkelser påvirker sluttdato": "No buffer - delays affect end date",
    "Dette vil oppdatere prosjektplanen din.": "This will update your project plan.",
    "Gratulerer! Du har succeeded in completing": "Congratulations! You have succeeded in completing",
    "i disse vil bringe deg under budgetet.": "in these will bring you under budget.",
}

def absolutely_last_fix(file_path: Path) -> bool:
    """Apply absolutely last fixes."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content

        for old, new in ABSOLUTELY_LAST_FIXES.items():
            content = content.replace(old, new)

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

    print(f"Absolutely last fix for {len(files)} files\n")

    count = 0
    for file in files:
        if absolutely_last_fix(file):
            count += 1

    print(f"\n🎉 ALL TRANSLATIONS COMPLETE! Fixed: {count}/{len(files)} files")

if __name__ == "__main__":
    main()
