#!/usr/bin/env python3
"""
Last minute fix for typos and remaining Norwegian.
"""

from pathlib import Path

# Last minute fixes
LAST_MINUTE_FIXES = {
    "strategyes": "strategies",
    "Forhandlingsstrategyes for Bruker": "Negotiation strategies for User",
    "AI forhandlingslogikk and strategyes": "AI negotiation logic and strategies",
    "Leverandørinformasjon": "Supplier Information",
    "Gemini 2.0 Flash strategyes for prisreduksjon and varighet optimalisering": "Gemini 2.0 Flash strategies for price reduction and duration optimization",
    "• Bruk \"mykere\" strategyes først": "• Use \"softer\" strategies first",
}

def last_minute_fix(file_path: Path) -> bool:
    """Apply last minute fixes."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content

        # Sort by length (longest first)
        sorted_fixes = sorted(LAST_MINUTE_FIXES.items(), key=lambda x: len(x[0]), reverse=True)

        for old, new in sorted_fixes:
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

    print(f"Last minute fix for {len(files)} files\n")

    count = 0
    for file in files:
        if last_minute_fix(file):
            count += 1

    print(f"\nAll translations COMPLETE! Fixed: {count}/{len(files)} files")

if __name__ == "__main__":
    main()
