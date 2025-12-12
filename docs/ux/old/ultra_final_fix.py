#!/usr/bin/env python3
"""
Ultra comprehensive final fix for ALL remaining Norwegian text.
"""

from pathlib import Path

# ALL remaining Norwegian translations
ULTRA_FINAL_TRANSLATIONS = {
    # Longest phrases first
    "Kritisk beslutningspunkt: Godkjenne tilbud and oppdatere plan": "Critical decision point: Approve offer and update plan",
    "Gemini 2.0 Flash strategyes for prisreduksjon and varighet optimalisering": "Gemini 2.0 Flash strategies for price reduction and duration optimization",
    "Interactive timeline view with critical path and avhengigheter": "Interactive timeline view with critical path and dependencies",
    "Kronologisk tidslinje med diff-view and tilbakestilling": "Chronological timeline with diff view and reset",
    "History with diff-view and tilbakestilling": "History with diff view and reset",
    "Click X (lukk) → Back to Dashboard (plan fortsatt godkjent)": "Click X (close) → Back to Dashboard (plan still approved)",
    "Click \"Confirm\" → Plan oppdateres (localStorage)": "Click \"Confirm\" → Plan updates (localStorage)",
    "Forhandlingsstrategy? (partnership, kvalitet, volumee)": "Negotiation strategy? (partnership, quality, volume)",
    "Hva kan dere tilby når det gjelder kostnad and varighet?": "What can you offer regarding cost and duration?",
    "Kan dere gå ned i pris if vi er fleksible på timeline?": "Can you go down in price if we are flexible on timeline?",
    "Min pris: cost * 0.85 | Max varighet: +20%": "Min price: cost * 0.85 | Max duration: +20%",
    "Er nytt tilbud innenfor grenser?": "Is new offer within limits?",
    "Forhandl lavere pris → Accept → Prøv validering igjen": "Negotiate lower price → Accept → Try validation again",
    "Start-dato: Basert på dependencies": "Start date: Based on dependencies",
    "Slutt-dato: Start + varighet (months)": "End date: Start + duration (months)",
    "Budget: Sum alle current_plan.cost": "Budget: Sum all current_plan.cost",
    "Forventet dato: Max end_date fra plan": "Expected date: Max end_date from plan",
    "Chat: System message \"✅ Tilbud godtatt...\"": "Chat: System message \"✅ Offer accepted...\"",
    "are not completed (vis tooltip med årsak)": "are not completed (show tooltip with reason)",
    "Tidsfokus? (\"for lang tid\", \"raskere\")": "Time focus? (\"too long time\", \"faster\")",
    "Før frist (15. May 2026) ✓": "Before deadline (15. May 2026) ✓",
    "Effekt: 5-10% prisreduksjon (Bjørn)": "Effect: 5-10% price reduction (Bjørn)",
    "Effekt: 3-7% prisreduksjon (Olav)": "Effect: 3-7% price reduction (Olav)",
    "Effekt: 2-5% prisreduksjon, +10% tid": "Effect: 2-5% price reduction, +10% time",
    "Effekt: -10% tid, +2% pris (Sofia)": "Effect: -10% time, +2% price (Sofia)",
    "Effekt: 0-3% (Emma blir utålmodig)": "Effect: 0-3% (Emma becomes impatient)",
    "if det gir bedre pris.": "if it gives better price.",
    "Kvalitet er viktigst for oss,": "Quality is most important for us,",
    "kan dere redusere tid?": "can you reduce time?",
    "Direkte prispress (Risiko)": "Direct price pressure (Risk)",
    "Jeg har ikke mer tid": "I don't have more time",
    "FEIL → Error-modal appear": "ERROR → Error-modal appears",
    "kvalitet and fremdrift.": "quality and progress.",
    "fokusert på kvalitet": "focused on quality",

    # Titles and headers
    "Modal - Success (Plan Godkjent)": "Modal - Success (Plan Approved)",
    "Plan Godkjent!": "Plan Approved!",
    "Confirm Forpliktelse": "Confirm Commitment",
    "Forhandlingsstrategyes for Bruker": "Negotiation strategies for User",
    "Status-indikator farger:": "Status indicator colors:",
    "Beregn Nytt Tilbud": "Calculate New Offer",
    "Send nytt tilbud": "Send new offer",
    "Bruker sender": "User sends",
    "Vurder bruker strategy:": "Evaluate user strategy:",
    "AI Prosess": "AI Process",
    "Registrering / Innlandging": "Registration / Login",
    "Confirm → Plan oppdatert": "Confirm → Plan updated",

    # Labels
    "Feil funnet:": "Errors found:",
    "Etter feil:": "After error:",
    "Frist:": "Deadline:",
    "Forventet ferdig:": "Expected completion:",
    "Tid spent:": "Time spent:",
    "Tid Brukt:": "Time Spent:",
    "Kostnad:": "Cost:",
    "Varighet:": "Duration:",
    "Siste tilbud:": "Latest offer:",
    "Tilbud mottatt:": "Offer received:",
    "Passord:": "Password:",
    "Feil:": "Error:",
    "Forpliktelse": "Commitment",

    # Phrases
    "Bruker åpner app": "User opens app",
    "Fyll inn passord (min 6)": "Fill in password (min 6)",
    "Fyll inn passord": "Fill in password",
    "Registrering:": "Registration:",
    "Innlogging:": "Login:",
    "Start Nytt Spill": "Start New Game",
    "Validateing kjøres:": "Validation runs:",
    "Confirmelsesdialog": "Confirmation dialog",
    "Feil (vist: Confirm)": "Error (shown: Confirm)",
    "Passord styrke-meter": "Password strength meter",
    "Vis/skjul passord": "Show/hide password",
    "vis tooltip med årsak": "show tooltip with reason",
    "plan fortsatt godkjent": "plan still approved",

    # Common words
    "Registrering": "Registration",
    "Innlogging": "Login",
    "Innlandging": "Login",
    "forpliktelse": "commitment",
    "Forpliktelse": "Commitment",
    "prisreduksjon": "price reduction",
    "varighet": "duration",
    "optimalisering": "optimization",
    "strategyes": "strategies",
    "Forhandlingsstrategyes": "Negotiation strategies",
    "Forhandlingsstrategy": "Negotiation strategy",
    "strategy": "strategy",
    "Bruker": "User",
    "bruker": "user",
    "sender": "sends",
    "Vurder": "Evaluate",
    "vurder": "evaluate",
    "Beregn": "Calculate",
    "beregn": "calculate",
    "nytt": "new",
    "Nytt": "New",
    "tilbud": "offer",
    "Tilbud": "Offer",
    "innenfor": "within",
    "grenser": "limits",
    "Send": "Send",
    "sender": "sends",
    "Effekt": "Effect",
    "effekt": "effect",
    "Prosess": "Process",
    "prosess": "process",
    "Tidsfokus": "Time focus",
    "tidsfokus": "time focus",
    "raskere": "faster",
    "kvalitet": "quality",
    "Kvalitet": "Quality",
    "volumee": "volume",
    "prispress": "price pressure",
    "Risiko": "Risk",
    "risiko": "risk",
    "utålmodig": "impatient",
    "Direkte": "Direct",
    "direkte": "direct",
    "viktigst": "most important",
    "redusere": "reduce",
    "bedre": "better",
    "lukk": "close",
    "fortsatt": "still",
    "godkjent": "approved",
    "Godkjent": "Approved",
    "godkjenne": "approve",
    "Godkjenne": "Approve",
    "oppdatere": "update",
    "oppdateres": "updates",
    "oppdatert": "updated",
    "beslutningspunkt": "decision point",
    "Kritisk": "Critical",
    "kritisk": "critical",
    "Basert": "Based",
    "basert": "based",
    "dependencies": "dependencies",
    "måneder": "months",
    "months": "months",
    "årsak": "reason",
    "tooltip": "tooltip",
    "styrke": "strength",
    "meter": "meter",
    "skjul": "hide",
    "vist": "shown",
    "Før": "Before",
    "før": "before",
    "frist": "deadline",
    "Frist": "Deadline",
    "Forventet": "Expected",
    "forventet": "expected",
    "ferdig": "completion",
    "spent": "spent",
    "Brukt": "Spent",
    "brukt": "spent",
    "Kostnad": "Cost",
    "kostnad": "cost",
    "Varighet": "Duration",
    "varighet": "duration",
    "Siste": "Latest",
    "siste": "latest",
    "mottatt": "received",
    "Feil": "Error",
    "feil": "error",
    "funnet": "found",
    "Etter": "After",
    "etter": "after",
    "lavere": "lower",
    "pris": "price",
    "Prøv": "Try",
    "prøv": "try",
    "validering": "validation",
    "igjen": "again",
    "Passord": "Password",
    "passord": "password",
    "Fyll": "Fill",
    "fyll": "fill",
    "inn": "in",
    "kjøres": "runs",
    "appear": "appears",
    "åpner": "opens",
    "app": "app",
    "Start": "Start",
    "start": "start",
    "Spill": "Game",
    "spill": "game",
    "dato": "date",
    "Dato": "Date",
    "Sum": "Sum",
    "alle": "all",
    "Max": "Max",
    "fra": "from",
    "plan": "plan",
    "Plan": "Plan",
    "når": "when",
    "det": "it",
    "gjelder": "regarding",
    "dere": "you",
    "kan": "can",
    "tilby": "offer",
    "gå": "go",
    "ned": "down",
    "hvis": "if",
    "vi": "we",
    "er": "are",
    "fleksible": "flexible",
    "på": "on",
    "timeline": "timeline",
    "lang": "long",
    "tid": "time",
    "Tid": "Time",
    "for": "too",
    "Hva": "What",
    "hva": "what",
    "Kan": "Can",
    "ikke": "not",
    "har": "have",
    "mer": "more",
    "oss": "us",
    "Vær": "Be",
    "fokusert": "focused",
    "gir": "gives",
    "blir": "becomes",
    "Min": "Min",
    "min": "min",
    "bli": "become",
    "avhengigheter": "dependencies",
}

def ultra_final_fix(file_path: Path) -> bool:
    """Apply ultra comprehensive final fixes."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content

        # Sort by length (longest first)
        sorted_trans = sorted(ULTRA_FINAL_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)

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

    print(f"Ultra final fix for {len(files)} files\n")

    count = 0
    for file in files:
        if ultra_final_fix(file):
            count += 1

    print(f"\nComplete! Fixed: {count}/{len(files)} files")

if __name__ == "__main__":
    main()
