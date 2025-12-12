#!/usr/bin/env python3
"""
Proper XML-aware translation that only translates text content,
not XML tags, attributes, or CSS class names.
"""

from pathlib import Path
import re

# Only the most important, unambiguous translations
TRANSLATIONS = {
    # Complete phrases first (to avoid partial matches)
    "Modal - Leverandørvalg": "Modal - Supplier Selection",
    "Modal - Valideringsfeil": "Modal - Validation Error",
    "Modal - Hjelp og Onboarding": "Modal - Help and Onboarding",
    "Modal - Suksess": "Modal - Success",
    "Modal - Bekreft Forpliktelse": "Modal - Confirm Commitment",
    "Registreringsside - Ny Bruker": "Registration Page - New User",
    "Innloggingsside - Autentisering": "Login Page - Authentication",
    "Dashboard - Hovedoversikt": "Dashboard - Main Overview",
    "Chat-grensesnitt - Forhandling": "Chat Interface - Negotiation",
    "Gantt-diagram - Tidsplan": "Gantt Chart - Timeline",
    "Presedensdiagram - Avhengigheter": "Precedence Diagram - Dependencies",
    "Historikk - Tidslinje": "History - Timeline",
    "Komponent - WBS Oppgavekort": "Component - WBS Task Card",
    "Komponent - Navigasjonsfelt": "Component - Navigation Bar",
    "Flyt - Komplett Brukerreise": "Flow - Complete User Journey",
    "Flyt - Autentisering": "Flow - Authentication",
    "Flyt - Forhandlingsstrategi": "Flow - Negotiation Strategy",

    # Multi-word descriptions
    "Veiledning for nye brukere - Hvordan spille simulatoren": "Guidance for new users - How to play the simulator",
    "Velg leverandør for WBS-oppgave før forhandling starter": "Select supplier for WBS task before negotiation starts",
    "Planen oppfyller ikke kravene - vis spesifikke feil og forslag": "Plan does not meet requirements - show specific errors and suggestions",
    "Supabase autentisering med validering og feilhåndtering": "Supabase authentication with validation and error handling",
    "Sentral kontrollpanel med budsjettsporing og WBS-oversikt": "Central control panel with budget tracking and WBS overview",
    "Ulike tilstander og interaksjoner for Work Breakdown Structure kort": "Various states and interactions for Work Breakdown Structure cards",
    "Toppnavigasjon med brukerinfo, hjelpikon og handlinger": "Top navigation with user info, help icon and actions",

    # Common phrases
    "Velkommen til Simulatoren!": "Welcome to the Simulator!",
    "Lær hvordan du planlegger Nye Hædda Barneskole prosjektet": "Learn how to plan the Nye Hædda School project",
    "Forstå budsjettet og tidsfristen": "Understand the budget and deadline",
    "Du må holde deg innenfor disse grensene for å lykkes": "You must stay within these limits to succeed",
    "Velg WBS-oppgaver å forhandle om": "Select WBS tasks to negotiate",
    "oppgaver fra prosjektering til ferdigstillelse": "tasks from design to completion",
    "Start med avhengige oppgaver (grunnarbeid først)": "Start with dependent tasks (foundation work first)",
    "Forhandle med AI-leverandører": "Negotiate with AI suppliers",
    "Chat med 5 unike leverandørpersonligheter": "Chat with 5 unique supplier personalities",
    "Bruk strategier som partnerskap, volum eller fleksibilitet": "Use strategies like partnership, volume or flexibility",
    "Send inn planen din": "Submit your plan",
    "Valider at planen oppfyller kravene": "Validate that the plan meets requirements",
    "Hvis feil oppstår, reforhandle de dyreste oppgavene": "If errors occur, renegotiate the most expensive tasks",
    "Lagre regelmessig med \"Eksporter økt\" for ikke å miste fremgangen din": "Save regularly with \"Export session\" to not lose your progress",
    "Sjekk kritisk sti i Gantt-diagram for å identifisere flaskehalser": "Check critical path in Gantt chart to identify bottlenecks",

    # Project management
    "Arbeidsnedbrytningsstruktur (WBS)": "Work Breakdown Structure (WBS)",
    "Arbeidsnedbrytningsstruktur": "Work Breakdown Structure",
    "Prosjektledelsessimulator": "Project Management Simulator",
    "Prosjektbegrensninger": "Project Constraints",

    # UI labels
    "Logg Inn": "Log In",
    "Logg inn her": "Log in here",
    "Logg ut": "Log out",
    "Opprett konto": "Create account",
    "Glemt passord?": "Forgot password?",
    "Husk meg": "Remember me",
    "Avbryt": "Cancel",
    "Godta": "Accept",
    "Bekreft": "Confirm",
    "Send Inn": "Submit",
    "Send Inn Plan": "Submit Plan",
    "Lagre": "Save",
    "Eksporter Økt": "Export Session",
    "Eksporter økt": "Export session",
    "Hjelp": "Help",
    "Innstillinger": "Settings",
    "Kontakt Leverandør": "Contact Supplier",
    "Se detaljer": "View details",
    "Reforhandle": "Renegotiate",
    "Forhandle →": "Negotiate →",
    "Fortsett chat →": "Continue chat →",
    "Avbryt forhandling": "Cancel negotiation",
    "Tilbake til Planlegging": "Back to Planning",
    "Start simulator →": "Start simulator →",
    "Start nytt spill": "Start new game",
    "Vis alle 5 leverandører ↓": "Show all 5 suppliers ↓",
    "Start forhandling med Bjørn Eriksen →": "Start negotiation with Bjørn Eriksen →",

    # Form fields
    "Fullt navn *": "Full name *",
    "E-postadresse *": "Email address *",
    "Passord *": "Password *",
    "Bekreft passord *": "Confirm password *",
    "Jeg godtar": "I accept",
    "brukervilkårene": "terms of service",
    "personvernpolicyen": "privacy policy",
    "Har du allerede en konto?": "Already have an account?",

    # Password requirements
    "Passordkrav:": "Password requirements:",
    "Minst 8 tegn": "At least 8 characters",
    "Ett tall": "One number",
    "Ett stort bokstav": "One uppercase letter",
    "Sterkt passord": "Strong password",
    "Passordene stemmer ikke overens": "Passwords do not match",

    # Status and labels
    "Tilstand 1: Standard (Dashboard)": "State 1: Default (Dashboard)",
    "Tilstand 2: Bruker-meny åpen": "State 2: User menu open",
    "Tilstand 1: Ikke startet (Pending)": "State 1: Not started (Pending)",
    "Tilstand 2: Forhandler (Negotiating)": "State 2: Negotiating",
    "Tilstand 3: Forpliktet (Committed)": "State 3: Committed",
    "Tilstand 4: Hover (Pending)": "State 4: Hover (Pending)",

    # Task names
    "1.3.1 - Grunnarbeid": "1.3.1 - Foundation Work",
    "1.1 - Prosjektering": "1.1 - Design",
    "2.1 - Råbygg": "2.1 - Shell Construction",
    "2.2 - Vinduer og Dører": "2.2 - Windows and Doors",
    "3.1 - VVS-installasjon": "3.1 - Plumbing Installation",
    "3.4 - Maling og Overflatebehandling": "3.4 - Painting and Surface Treatment",

    # Task descriptions
    "Masseutskifting, grunnmur, drenering, fundamenter": "Excavation, foundation wall, drainage, foundations",
    "Installasjon av vinduer og ytterdører": "Installation of windows and exterior doors",

    # Common words (only when standalone)
    " Budsjett": " Budget",
    " Frist:": " Deadline:",
    " Forventet ferdig:": " Expected completion:",
    " Kritisk sti:": " Critical path:",
    " Fremdrift:": " Progress:",
    " måneder": " months",
    " fullført": " completed",
    " forhandlinger": " negotiations",
    " reforhandlinger": " renegotiations",
    " Handlinger": " Actions",
    " Øktstatus": " Session Status",
    " Opprettet:": " Created:",
    " Tid brukt:": " Time spent:",
    " Lagringsplass:": " Storage:",
    " minutter": " minutes",
    " Avhengigheter:": " Dependencies:",
    " Krav:": " Requirements:",
    " Siste tilbud:": " Latest offer:",
    " Meldinger:": " Messages:",
    " Kostnad:": " Cost:",
    " Varighet:": " Duration:",
    " Tidsperiode:": " Time period:",
    " Leverandør:": " Supplier:",
    " Start:": " Start:",
    " Slutt:": " End:",
    " utvekslet": " exchanged",
    " Grunnlag:": " Baseline:",
    " Avhenger av:": " Depends on:",
    " Krever 15/15 fullført": " Requires 15/15 completed",
    " flere oppgaver": " more tasks",

    # Supplier specialties
    " Totalentreprenør": " General Contractor",
    " Byggeleder": " Construction Manager",
    " Graveentreprenør": " Excavation Contractor",
    " Prosjektleder": " Project Manager",
    " Spesialiteter:": " Specialties:",
    " Grunnarbeid": " Foundation Work",
    " Råbygg": " Shell Construction",
    " Prosjektledelse": " Project Management",
    " Koordinering": " Coordination",
    " Kvalitet": " Quality",
    " Graving": " Excavation",

    # Personas
    "\"Pragmatisk og erfaren, fokusert på kvalitet\"": "\"Pragmatic and experienced, focused on quality\"",
    "\"Strukturert og detaljorientert, streng på kvalitet\"": "\"Structured and detail-oriented, strict on quality\"",
    "\"Kostnadsbevisst, fleksibel, fokus på fremdrift\"": "\"Cost-conscious, flexible, focus on progress\"",
    "\"Ambisiøs og konkurransedyktig, utålmodig\"": "\"Ambitious and competitive, impatient\"",
    "⭐ Anbefalte match for denne oppgaven": "⭐ Recommended match for this task",

    # Annotations
    " Når vises denne modalen?": " When does this modal appear?",
    " Logikk:": " Logic:",
    " Interaksjoner:": " Interactions:",
    " Validering:": " Validation:",
    " Feil:": " Error:",
    " Tilstander:": " States:",
    " Standard": " Default",
    " Fokus": " Focus",
    " Feil (vist: Bekreft)": " Error (shown: Confirm)",
    " Deaktivert (knapp)": " Disabled (button)",
    " Navigasjonslogikk:": " Navigation logic:",
    " Aktiv side:": " Active page:",
    " Blå tekst + underline": " Blue text + underline",
    " Bruker-meny handlinger:": " User menu actions:",
    " Status-indikator farger:": " Status indicator colors:",
    " Grå: Ikke startet (pending)": " Gray: Not started (pending)",
    " Gul: Forhandler (negotiating)": " Yellow: Negotiating",
    " Grønn + ✓: Forpliktet (committed)": " Green + ✓: Committed",
    " Komponenten brukes i:": " Component used in:",
    " Liste av alle 15 WBS-oppgaver": " List of all 15 WBS tasks",
    " Filtrerbar og sorterbar liste": " Filterable and sortable list",
    " Real-time oppdatering ved forpliktelse": " Real-time update on commitment",
    " Valideringslogikk:": " Validation Logic:",
    " Etter feil:": " After error:",
    " Tilgjengelige leverandører (5):": " Available suppliers (5):",
    " WBS-oppgave:": " WBS task:",
    " Velg Leverandør for Forhandling": " Select Supplier for Negotiation",

    # Validation
    " Feil funnet:": " Errors found:",
    " Budsjett overskredet med 50 MNOK": " Budget exceeded by 50 MNOK",
    " Prosjektet forsinket til 20. mai 2026": " Project delayed until May 20, 2026",
    " Grense:": " Limit:",
    " Overskridelse:": " Delay:",
    " Planvalidering Mislyktes": " Plan Validation Failed",
    " Forslag til løsning:": " Suggested solutions:",
    " Vurder å reforhandle disse kostbare oppgavene:": " Consider renegotiating these expensive tasks:",

    # Navigation
    " Dashbord": " Dashboard",
    " Gantt-diagram": " Gantt Chart",
    " Presedensdiagram": " Precedence Diagram",
    " Historikk-side": " History page",
    " Chat-side": " Chat page",

    # Footer descriptions
    " med budsjettsporing og WBS-liste": " with budget tracking and WBS list",
    " Leverandørvalg før forhandling": " Supplier selection before negotiation",
    " Valideringsfeil med konkrete forslag": " Validation error with concrete suggestions",
    " Onboarding for nye brukere": " Onboarding for new users",
    " Registreringsside med Supabase auth": " Registration page with Supabase auth",
    " Navigasjonsfelt med bruker-meny": " Navigation bar with user menu",
    " WBS oppgavekort komponenter og tilstander": " WBS task card components and states",
}

def translate_text_content(content: str) -> str:
    """Translate only text content, preserving XML structure."""
    # Sort translations by length (longest first)
    sorted_translations = sorted(TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)

    for norwegian, english in sorted_translations:
        content = content.replace(norwegian, english)

    return content

def translate_file(file_path: Path) -> bool:
    """Translate a single SVG file."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content

        translated = translate_text_content(content)

        if translated != original:
            file_path.write_text(translated, encoding='utf-8')
            print(f"[OK] Translated: {file_path.name}")
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

    print(f"Translating {len(files)} files\n")

    count = 0
    for file in files:
        if translate_file(file):
            count += 1

    print(f"\nDone! Translated: {count}/{len(files)} files")

if __name__ == "__main__":
    main()
