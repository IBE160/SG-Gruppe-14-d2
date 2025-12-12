#!/usr/bin/env python3
"""
Final cleanup to translate remaining Norwegian words in mixed content.
Only translates standalone Norwegian words, preserving all XML structure.
"""

from pathlib import Path
import re

# Remaining word-by-word translations with word boundaries
WORD_TRANSLATIONS = [
    (r'\bBudsjett:', 'Budget:'),
    (r'\bmai\b', 'May'),
    (r'\bapril\b', 'April'),
    (r'\bjan\b', 'Jan'),
    (r'\bfeb\b', 'Feb'),
    (r'\bmar\b', 'Mar'),
    (r'\bjuni\b', 'June'),
    (r'\bjuli\b', 'July'),
    (r'\baug\b', 'Aug'),
    (r'\bsep\b', 'Sep'),
    (r'\bokt\b', 'Oct'),
    (r'\bnov\b', 'Nov'),
    (r'\bdes\b', 'Dec'),
    (r'\bDesember\b', 'December'),
    (r'\bjanuar\b', 'January'),
    (r'\bfebruar\b', 'February'),
    (r'\bmars\b', 'March'),
    (r'\bjuni\b', 'June'),
    (r'\bjuli\b', 'July'),
    (r'\baugust\b', 'August'),
    (r'\bseptember\b', 'September'),
    (r'\boktober\b', 'October'),
    (r'\bnovember\b', 'November'),
    (r'\beller\b', 'or'),
    (r'\bog\b', 'and'),
    (r'\båpne\b', 'open'),
    (r'\bmåneder\b', 'months'),
    (r'\bmåned\b', 'month'),
    (r'\buker\b', 'weeks'),
    (r'\buke\b', 'week'),
    (r'\bdager\b', 'days'),
    (r'\bdag\b', 'day'),
    (r'\bårstid\b', 'season'),
    (r'\bminutter\b', 'minutes'),
    (r'\bminutt\b', 'minute'),
    (r'\btimer\b', 'hours'),
    (r'\btime\b', 'hour'),
    (r'\bår\b', 'years'),
]

def final_cleanup(file_path: Path) -> bool:
    """Final cleanup of remaining Norwegian words."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content

        # Apply word-by-word translations using regex with word boundaries
        for pattern, replacement in WORD_TRANSLATIONS:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

        if content != original:
            file_path.write_text(content, encoding='utf-8')
            print(f"[OK] Cleaned: {file_path.name}")
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

    print(f"Final cleanup of {len(files)} files\n")

    count = 0
    for file in files:
        if final_cleanup(file):
            count += 1

    print(f"\nComplete! Cleaned: {count}/{len(files)} files")

if __name__ == "__main__":
    main()
