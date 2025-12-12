#!/usr/bin/env python3
"""
Smart final fix using regex word boundaries to avoid corrupting English words.
Only translates complete Norwegian words/phrases, not substrings.
"""

from pathlib import Path
import re

# Phrase-level translations (exact matches only)
PHRASE_TRANSLATIONS = [
    # Complete phrases that should be replaced as whole units
    ("Kritisk beslutningspunkt: Godkjenne tilbud and oppdatere plan", "Critical decision point: Approve offer and update plan"),
    ("Gemini 2.0 Flash strategyes for prisreduksjon and varighet optimalisering", "Gemini 2.0 Flash strategies for price reduction and duration optimization"),
    ("Click X (lukk) → Back to Dashboard (plan fortsatt godkjent)", "Click X (close) → Back to Dashboard (plan still approved)"),
    ("Click \"Confirm\" → Plan oppdateres (localStorage)", "Click \"Confirm\" → Plan updates (localStorage)"),
    ("Forhandlingsstrategy? (partnership, kvalitet, volumee)", "Negotiation strategy? (partnership, quality, volume)"),
    ("Hva kan dere tilby når det gjelder kostnad and varighet?", "What can you offer regarding cost and duration?"),
    ("Kan dere gå ned i pris if vi er fleksible på timeline?", "Can you go down in price if we are flexible on timeline?"),
    ("Min pris: cost * 0.85 | Max varighet: +20%", "Min price: cost * 0.85 | Max duration: +20%"),
    ("Er nytt tilbud innenfor grenser?", "Is new offer within limits?"),
    ("Forhandl lavere pris → Accept → Prøv validering igjen", "Negotiate lower price → Accept → Try validation again"),
    ("Start-dato: Basert på dependencies", "Start date: Based on dependencies"),
    ("Slutt-dato: Start + varighet (months)", "End date: Start + duration (months)"),
    ("Budget: Sum alle current_plan.cost", "Budget: Sum all current_plan.cost"),
    ("Forventet dato: Max end_date fra plan", "Expected date: Max end_date from plan"),
    ("Chat: System message \"✅ Tilbud godtatt...\"", "Chat: System message \"✅ Offer accepted...\""),
    ("are not completed (vis tooltip med årsak)", "are not completed (show tooltip with reason)"),
    ("Tidsfokus? (\"for lang tid\", \"raskere\")", "Time focus? (\"too long time\", \"faster\")"),
    ("Før frist (15. May 2026) ✓", "Before deadline (15. May 2026) ✓"),
    ("Effekt: 5-10% prisreduksjon (Bjørn)", "Effect: 5-10% price reduction (Bjørn)"),
    ("Effekt: 3-7% prisreduksjon (Olav)", "Effect: 3-7% price reduction (Olav)"),
    ("Effekt: 2-5% prisreduksjon, +10% tid", "Effect: 2-5% price reduction, +10% time"),
    ("Effekt: -10% tid, +2% pris (Sofia)", "Effect: -10% time, +2% price (Sofia)"),
    ("Effekt: 0-3% (Emma blir utålmodig)", "Effect: 0-3% (Emma becomes impatient)"),
    ("if det gir bedre pris.", "if it gives better price."),
    ("Kvalitet er viktigst for oss,", "Quality is most important for us,"),
    ("kan dere redusere tid?", "can you reduce time?"),
    ("Direkte prispress (Risiko)", "Direct price pressure (Risk)"),
    ("Jeg har ikke mer tid", "I don't have more time"),
    ("FEIL → Error-modal appear", "ERROR → Error-modal appears"),
    ("kvalitet and fremdrift.", "quality and progress."),
    ("Modal - Success (Plan Godkjent)", "Modal - Success (Plan Approved)"),
    ("Plan Godkjent!", "Plan Approved!"),
    ("Confirm Forpliktelse", "Confirm Commitment"),
    ("Forhandlingsstrategyes for Bruker", "Negotiation strategies for User"),
    ("Status-indikator farger:", "Status indicator colors:"),
    ("Beregn Nytt Tilbud", "Calculate New Offer"),
    ("Send nytt tilbud", "Send new offer"),
    ("Bruker sender", "User sends"),
    ("Vurder bruker strategy:", "Evaluate user strategy:"),
    ("AI Prosess", "AI Process"),
    ("Registrering / Innlandging", "Registration / Login"),
    ("Confirm → Plan oppdatert", "Confirm → Plan updated"),
    ("Feil funnet:", "Errors found:"),
    ("Etter feil:", "After error:"),
    ("Frist:", "Deadline:"),
    ("Forventet ferdig:", "Expected completion:"),
    ("Tid spent:", "Time spent:"),
    ("Tid Brukt:", "Time Spent:"),
    ("Kostnad:", "Cost:"),
    ("Varighet:", "Duration:"),
    ("Siste tilbud:", "Latest offer:"),
    ("Tilbud mottatt:", "Offer received:"),
    ("Passord:", "Password:"),
    ("Feil:", "Error:"),
    ("Bruker åpner app", "User opens app"),
    ("Fyll inn passord (min 6)", "Fill in password (min 6)"),
    ("Fyll inn passord", "Fill in password"),
    ("Registrering:", "Registration:"),
    ("Innlogging:", "Login:"),
    ("Start Nytt Spill", "Start New Game"),
    ("Validateing kjøres:", "Validation runs:"),
    ("Confirmelsesdialog", "Confirmation dialog"),
    ("Feil (vist: Confirm)", "Error (shown: Confirm)"),
    ("Passord styrke-meter", "Password strength meter"),
    ("Vis/skjul passord", "Show/hide password"),
    ("vis tooltip med årsak", "show tooltip with reason"),
    ("plan fortsatt godkjent", "plan still approved"),
    ("fokusert på kvalitet", "focused on quality"),
]

# Word-level translations with word boundaries (only standalone words)
WORD_TRANSLATIONS = [
    (r'\bRegistrering\b', 'Registration'),
    (r'\bInnlogging\b', 'Login'),
    (r'\bInnlandging\b', 'Login'),
    (r'\bForpliktelse\b', 'Commitment'),
    (r'\bprisreduksjon\b', 'price reduction'),
    (r'\boptimalisering\b', 'optimization'),
    (r'\bstrategyes\b', 'strategies'),
    (r'\bForhandlingsstrategyes\b', 'Negotiation strategies'),
    (r'\bForhandlingsstrategy\b', 'Negotiation strategy'),
    (r'\bBruker\b', 'User'),
    (r'\bVurder\b', 'Evaluate'),
    (r'\bBeregn\b', 'Calculate'),
    (r'\binnenfor\b', 'within'),
    (r'\bgrenser\b', 'limits'),
    (r'\bEffekt\b', 'Effect'),
    (r'\bProsess\b', 'Process'),
    (r'\bTidsfokus\b', 'Time focus'),
    (r'\braskere\b', 'faster'),
    (r'\bkvalitet\b', 'quality'),
    (r'\bKvalitet\b', 'Quality'),
    (r'\bvolumee\b', 'volume'),
    (r'\bprispress\b', 'price pressure'),
    (r'\bRisiko\b', 'Risk'),
    (r'\butålmodig\b', 'impatient'),
    (r'\bDirekte\b', 'Direct'),
    (r'\bviktigst\b', 'most important'),
    (r'\bredusere\b', 'reduce'),
    (r'\bbedre\b', 'better'),
    (r'\blukk\b', 'close'),
    (r'\bfortsatt\b', 'still'),
    (r'\bgodkjent\b', 'approved'),
    (r'\bGodkjent\b', 'Approved'),
    (r'\bgodkjenne\b', 'approve'),
    (r'\bGodkjenne\b', 'Approve'),
    (r'\boppdatere\b', 'update'),
    (r'\boppdateres\b', 'updates'),
    (r'\boppdatert\b', 'updated'),
    (r'\bbeslutningspunkt\b', 'decision point'),
    (r'\bKritisk\b', 'Critical'),
    (r'\bBasert\b', 'Based'),
    (r'\bmåneder\b', 'months'),
    (r'\bårsak\b', 'reason'),
    (r'\bstyrke\b', 'strength'),
    (r'\bskjul\b', 'hide'),
    (r'\bvist\b', 'shown'),
    (r'\bFør\b', 'Before'),
    (r'\bfrist\b', 'deadline'),
    (r'\bFrist\b', 'Deadline'),
    (r'\bForventet\b', 'Expected'),
    (r'\bferdig\b', 'completion'),
    (r'\bBrukt\b', 'Spent'),
    (r'\bbrukt\b', 'spent'),
    (r'\bKostnad\b', 'Cost'),
    (r'\bkostnad\b', 'cost'),
    (r'\bVarighet\b', 'Duration'),
    (r'\bvarighet\b', 'duration'),
    (r'\bSiste\b', 'Latest'),
    (r'\bmottatt\b', 'received'),
    (r'\bFeil\b', 'Error'),
    (r'\bfeil\b', 'error'),
    (r'\bfunnet\b', 'found'),
    (r'\bEtter\b', 'After'),
    (r'\blavere\b', 'lower'),
    (r'\bpris\b', 'price'),
    (r'\bPrøv\b', 'Try'),
    (r'\bvalidering\b', 'validation'),
    (r'\bigjen\b', 'again'),
    (r'\bPassord\b', 'Password'),
    (r'\bpassord\b', 'password'),
    (r'\bFyll\b', 'Fill'),
    (r'\binn\b', 'in'),
    (r'\bkjøres\b', 'runs'),
    (r'\båpner\b', 'opens'),
    (r'\bapp\b', 'app'),
    (r'\bStart\b', 'Start'),
    (r'\bSpill\b', 'Game'),
    (r'\bdato\b', 'date'),
    (r'\bDato\b', 'Date'),
    (r'\bSum\b', 'Sum'),
    (r'\balle\b', 'all'),
    (r'\bMax\b', 'Max'),
    (r'\bgjelder\b', 'regarding'),
    (r'\bdere\b', 'you'),
    (r'\btilby\b', 'offer'),
    (r'\bned\b', 'down'),
    (r'\bhvis\b', 'if'),
    (r'\bvi\b', 'we'),
    (r'\ber\b', 'are'),
    (r'\bfleksible\b', 'flexible'),
    (r'\blang\b', 'long'),
    (r'\btid\b', 'time'),
    (r'\bTid\b', 'Time'),
    (r'\bHva\b', 'What'),
    (r'\bKan\b', 'Can'),
    (r'\bikke\b', 'not'),
    (r'\bhar\b', 'have'),
    (r'\bmer\b', 'more'),
    (r'\boss\b', 'us'),
    (r'\bfokusert\b', 'focused'),
    (r'\bgir\b', 'gives'),
    (r'\bblir\b', 'becomes'),
    (r'\bnytt\b', 'new'),
    (r'\bNytt\b', 'New'),
    (r'\btilbud\b', 'offer'),
    (r'\bTilbud\b', 'Offer'),
    (r'\bSend\b', 'Send'),
    (r'\bfremdrift\b', 'progress'),
]

def smart_final_fix(file_path: Path) -> bool:
    """Apply smart final fixes using word boundaries."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content

        # First, apply phrase-level translations (exact matches)
        for norwegian, english in PHRASE_TRANSLATIONS:
            content = content.replace(norwegian, english)

        # Then, apply word-level translations with regex word boundaries
        for pattern, replacement in WORD_TRANSLATIONS:
            content = re.sub(pattern, replacement, content)

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

    print(f"Smart final fix for {len(files)} files\n")

    count = 0
    for file in files:
        if smart_final_fix(file):
            count += 1

    print(f"\nComplete! Fixed: {count}/{len(files)} files")

if __name__ == "__main__":
    main()
