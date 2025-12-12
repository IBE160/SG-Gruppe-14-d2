#!/usr/bin/env python3
"""
Comprehensive final fix for all remaining Norwegian text.
"""

from pathlib import Path

# All remaining Norwegian translations found
FINAL_TRANSLATIONS = {
    # Full phrases (longest first to avoid partial matches)
    "Forslag til løsning:": "Suggested solutions:",
    "WBS-oppgave:": "WBS task:",
    "Leverandør:": "Supplier:",
    "lagt til i plan": "added to plan",
    "Redirect til Dashboard": "Redirect to Dashboard",
    "Forpliktelsesmodal med bekreftelse": "Commitment modal with confirmation",
    "Redirect til login": "Redirect to login",
    "Kom i gang med Nye Hædda Barneskole Simulator": "Get started with Nye Hædda School Simulator",
    "Forhandler med Bjørn Eriksen...": "Negotiating with Bjørn Eriksen...",
    "Klikk \"Forhandle\" → Leverandør-valg modal": "Click \"Negotiate\" → Supplier selection modal",
    "\"Forhandle\"-knapp deaktivert hvis avhengigheter": "\"Negotiate\" button disabled if dependencies",
    "ikke er completed": "are not completed",
    "Vis advarsel hvis budsjett/tidslinje i fare": "Show warning if budget/timeline at risk",
    "med critical path fremhevet": "with critical path highlighted",
    "Valgt oppgave:": "Selected task:",
    "AON presedensdiagram med critical path": "AON precedence diagram with critical path",
    "Registrering and innlogging med JWT-basert autentisering": "Registration and login with JWT-based authentication",
    "lykkes med å fullføre": "succeeded in completing",
    "Under budsjett": "Under budget",
    "Tilbake til Dashboard": "Back to Dashboard",
    "Suksessmodal med statistikk and eksport": "Success modal with statistics and export",
    "Sanntids forhandling med AI-leverandør": "Real-time negotiation with AI supplier",
    "← Tilbake til Oversikt": "← Back to Overview",
    "Takk for tilbudet. 120 MNOK er litt høyt for vårt budsjett.": "Thanks for the offer. 120 MNOK is a bit high for our budget.",
    "AI Chat-grensesnitt med sanntids forhandling": "AI Chat interface with real-time negotiation",
    "Full gjennomføring from registrering til eksport": "Complete journey from registration to export",
    "Til Dashboard": "To Dashboard",
    "Velg Leverandør": "Select Supplier",
    "Valider": "Validate",
    "Budsjett ≤700 MNOK?": "Budget ≤700 MNOK?",
    "Budsjett": "Budget",
    "Velg Leverandør for Forhandling": "Select Supplier for Negotiation",
    "Klikk \"Forhandle\" på en WBS-oppgave uten leverandør": "Click \"Negotiate\" on a WBS task without supplier",
    "or klikk \"Renegotiate\" to bytte leverandør": "or click \"Renegotiate\" to change supplier",
    "Interaktiv tidslinjevisning med critical path and avhengigheter": "Interactive timeline view with critical path and dependencies",
    "Budsjett brukt:": "Budget spent:",
    "Interaktiv Gantt Chart med critical path": "Interactive Gantt Chart with critical path",
    "Kronologisk tidslinje med diff-visning and tilbakestilling": "Chronological timeline with diff view and reset",
    "Budsjett overskredet:": "Budget exceeded:",
    "Budsjett i faresonen": "Budget at risk",
    "Appellert til langsiktig partnership": "Appealed to long-term partnership",
    "Leverandør reaksjon:": "Supplier reaction:",
    "⟲ Tilbakestill til dette punktet": "⟲ Reset to this point",
    "Historikk med diff-visning and tilbakestilling": "History with diff view and reset",
    "Leverandør-personlighet": "Supplier personality",
    "gå ned til X MNOK?": "go down to X MNOK?",
    "Match strategi med leverandørpersonlighet": "Match strategy with supplier personality",

    # Individual words
    "innlogging": "login",
    "Forhandler": "Negotiating",
    "Forhandle": "Negotiate",
    "Klikk": "Click",
    "leverandør": "supplier",
    "oppgave": "task",
    "bytte": "change",
    "uten": "without",
    "avhengigheter": "dependencies",
    "hvis": "if",
    "tidslinje": "timeline",
    "fare": "risk",
    "lykkes": "succeeded",
    "fullføre": "completing",
    "Tilbake": "Back",
    "Oversikt": "Overview",
    "Takk": "Thanks",
    "tilbudet": "offer",
    "høyt": "high",
    "vårt": "our",
    "budsjett": "budget",
    "gjennomføring": "journey",
    "registrering": "registration",
    "eksport": "export",
    "Velg": "Select",
    "brukt": "spent",
    "overskredet": "exceeded",
    "faresonen": "at risk",
    "Appellert": "Appealed",
    "langsiktig": "long-term",
    "reaksjon": "reaction",
    "Tilbakestill": "Reset",
    "dette": "this",
    "punktet": "point",
    "personlighet": "personality",
    "strategi": "strategy",
}

def comprehensive_fix(file_path: Path) -> bool:
    """Apply comprehensive final fixes."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content

        # Sort by length (longest first)
        sorted_trans = sorted(FINAL_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)

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

    print(f"Comprehensive final fix for {len(files)} files\n")

    count = 0
    for file in files:
        if comprehensive_fix(file):
            count += 1

    print(f"\nComplete! Fixed: {count}/{len(files)} files")

if __name__ == "__main__":
    main()
