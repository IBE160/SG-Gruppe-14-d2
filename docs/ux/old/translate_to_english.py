#!/usr/bin/env python3
"""
High-quality Norwegian to English translation for SVG mockup files.
This script provides comprehensive, accurate translations for all UI elements.
"""

from pathlib import Path
import re

# Comprehensive translation dictionary with accurate English equivalents
TRANSLATIONS = {
    # Page titles and headers
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

    # Subtitles and descriptions
    "Veiledning for nye brukere - Hvordan spille simulatoren": "Guidance for new users - How to play the simulator",
    "Velg leverandør for WBS-oppgave før forhandling starter": "Select supplier for WBS task before negotiation starts",
    "Planen oppfyller ikke kravene - vis spesifikke feil og forslag": "Plan does not meet requirements - show specific errors and suggestions",
    "Bekreft valg før forpliktelse": "Confirm choice before commitment",
    "Plan godkjent - prosjektet kan starte": "Plan approved - project can start",
    "Supabase autentisering med validering og feilhåndtering": "Supabase authentication with validation and error handling",
    "Sikker pålogging med e-post og passord": "Secure login with email and password",
    "Sentral kontrollpanel med budsjettsporing og WBS-oversikt": "Central control panel with budget tracking and WBS overview",
    "Sanntids forhandling med AI-leverandører": "Real-time negotiation with AI suppliers",
    "Visuell tidsplan med kritisk sti": "Visual timeline with critical path",
    "Oppgaveavhengigheter og rekkefølge": "Task dependencies and sequence",
    "Logg over alle forhandlinger og beslutninger": "Log of all negotiations and decisions",
    "Ulike tilstander og interaksjoner for Work Breakdown Structure kort": "Various states and interactions for Work Breakdown Structure cards",
    "Toppnavigasjon med brukerinfo, hjelpikon og handlinger": "Top navigation with user info, help icon and actions",

    # Common UI elements
    "Logg Inn": "Log In",
    "Logg inn": "Log in",
    "Logg inn her": "Log in here",
    "Logg ut": "Log out",
    "Opprett konto": "Create account",
    "Opprett Konto": "Create Account",
    "Registrer deg": "Sign up",
    "Registrer deg her": "Sign up here",
    "Glemt passord?": "Forgot password?",
    "Husk meg": "Remember me",
    "Lukk": "Close",
    "Avbryt": "Cancel",
    "Godta": "Accept",
    "Bekreft": "Confirm",
    "Fortsett": "Continue",
    "Tilbake": "Back",
    "Neste": "Next",
    "Forrige": "Previous",
    "Send": "Send",
    "Send Inn": "Submit",
    "Send inn": "Submit",
    "Lagre": "Save",
    "Eksporter": "Export",
    "Importer": "Import",
    "Last opp": "Upload",
    "Last ned": "Download",
    "Slett": "Delete",
    "Rediger": "Edit",
    "Endre": "Change",
    "Søk": "Search",
    "Filtrer": "Filter",
    "Sorter": "Sort",
    "Hjelp": "Help",
    "Innstillinger": "Settings",
    "Profil": "Profile",
    "Vis": "Show",
    "Skjul": "Hide",
    "Start": "Start",
    "Stopp": "Stop",
    "Pause": "Pause",
    "Hopp over": "Skip",

    # Form labels and fields
    "Fullt navn": "Full name",
    "Fornavn": "First name",
    "Etternavn": "Last name",
    "E-post": "Email",
    "E-postadresse": "Email address",
    "Passord": "Password",
    "Bekreft passord": "Confirm password",
    "Gammelt passord": "Old password",
    "Nytt passord": "New password",
    "Telefonnummer": "Phone number",
    "Adresse": "Address",
    "Postnummer": "Postal code",
    "By": "City",
    "Land": "Country",

    # Validation and errors
    "Påkrevd": "Required",
    "Valgfritt": "Optional",
    "Ugyldig": "Invalid",
    "Gyldig": "Valid",
    "Feil": "Error",
    "Advarsel": "Warning",
    "Suksess": "Success",
    "Info": "Info",
    "Feil funnet": "Errors found",
    "Ingen feil": "No errors",
    "Validering": "Validation",
    "Valideringsfeil": "Validation error",
    "Valideringslogikk": "Validation Logic",
    "Etter feil": "After error",

    # Password requirements
    "Passordkrav": "Password requirements",
    "Minst 8 tegn": "At least 8 characters",
    "Ett tall": "One number",
    "Ett stort bokstav": "One uppercase letter",
    "Sterkt passord": "Strong password",
    "Svakt passord": "Weak password",
    "Middels passord": "Medium password",
    "Passordene stemmer ikke overens": "Passwords do not match",
    "Passord styrke-meter": "Password strength meter",

    # Project management terms
    "Prosjekt": "Project",
    "Prosjekter": "Projects",
    "Oppgave": "Task",
    "Oppgaver": "Tasks",
    "Aktivitet": "Activity",
    "Aktiviteter": "Activities",
    "Milepæl": "Milestone",
    "Milepæler": "Milestones",
    "Leveranse": "Deliverable",
    "Leveranser": "Deliverables",
    "Ressurs": "Resource",
    "Ressurser": "Resources",
    "Budsjett": "Budget",
    "Kostnad": "Cost",
    "Kostnader": "Costs",
    "Tid": "Time",
    "Varighet": "Duration",
    "Frist": "Deadline",
    "Startdato": "Start date",
    "Sluttdato": "End date",
    "Fremdrift": "Progress",
    "Status": "Status",
    "Prioritet": "Priority",
    "Avhengighet": "Dependency",
    "Avhengigheter": "Dependencies",
    "Kritisk sti": "Critical path",
    "Tidsplan": "Timeline",
    "Gantt-diagram": "Gantt Chart",
    "Presedensdiagram": "Precedence Diagram",

    # WBS specific terms
    "Arbeidsnedbrytningsstruktur": "Work Breakdown Structure",
    "Arbeidsnedbrytningsstruktur (WBS)": "Work Breakdown Structure (WBS)",
    "WBS-oppgave": "WBS task",
    "WBS-oppgaver": "WBS tasks",
    "Grunnarbeid": "Foundation Work",
    "Prosjektering": "Design",
    "Råbygg": "Shell Construction",
    "Vinduer og Dører": "Windows and Doors",
    "VVS-installasjon": "Plumbing Installation",
    "Elektrisk installasjon": "Electrical Installation",
    "Maling og Overflatebehandling": "Painting and Surface Treatment",
    "Innvendige arbeider": "Interior Work",
    "Utvendige arbeider": "Exterior Work",
    "Ferdigstillelse": "Completion",

    # Supplier/negotiation terms
    "Leverandør": "Supplier",
    "Leverandører": "Suppliers",
    "Tilgjengelige leverandører": "Available suppliers",
    "Velg Leverandør for Forhandling": "Select Supplier for Negotiation",
    "Start forhandling med": "Start negotiation with",
    "Forhandle": "Negotiate",
    "Forhandling": "Negotiation",
    "Forhandlinger": "Negotiations",
    "Reforhandle": "Renegotiate",
    "Reforhandlinger": "Renegotiations",
    "Forhandler": "Negotiating",
    "Forhandler med": "Negotiating with",
    "Fortsett chat": "Continue chat",
    "Avbryt forhandling": "Cancel negotiation",
    "Totalentreprenør": "General Contractor",
    "Byggeleder": "Construction Manager",
    "Graveentreprenør": "Excavation Contractor",
    "Prosjektleder": "Project Manager",
    "Spesialiteter": "Specialties",
    "Anbefalte match for denne oppgaven": "Recommended match for this task",

    # Chat/messaging
    "Melding": "Message",
    "Meldinger": "Messages",
    "Siste tilbud": "Latest offer",
    "Siste melding": "Last message",
    "Send melding": "Send message",
    "Skriv en melding": "Type a message",
    "Utvekslet": "exchanged",

    # Status states
    "Ikke startet": "Not started",
    "Pågående": "In progress",
    "Fullført": "Completed",
    "Forpliktet": "Committed",
    "Pending": "Pending",
    "Aktiv": "Active",
    "Inaktiv": "Inactive",
    "Godkjent": "Approved",
    "Avvist": "Rejected",
    "Avventer": "Waiting",

    # Actions and buttons
    "Kontakt Leverandør": "Contact Supplier",
    "Se detaljer": "View details",
    "Vis detaljer": "Show details",
    "Eksporter Økt": "Export Session",
    "Eksporter økt": "Export session",
    "Send Inn Plan": "Submit Plan",
    "Tilbake til Planlegging": "Back to Planning",
    "Start simulator": "Start simulator",
    "Start nytt spill": "Start new game",
    "Handlinger": "Actions",

    # Dashboard/overview
    "Dashbord": "Dashboard",
    "Dashboard": "Dashboard",
    "Oversikt": "Overview",
    "Hovedoversikt": "Main Overview",
    "Prosjektledelsessimulator": "Project Management Simulator",
    "Prosjektbegrensninger": "Project Constraints",
    "Grunnlag": "Baseline",
    "Forventet ferdig": "Expected completion",
    "Øktstatus": "Session Status",
    "Opprettet": "Created",
    "Tid brukt": "Time spent",
    "Lagringsplass": "Storage",

    # Time units
    "dag": "day",
    "dager": "days",
    "uke": "week",
    "uker": "weeks",
    "måned": "month",
    "måneder": "months",
    "år": "year",
    "år": "years",
    "time": "hour",
    "timer": "hours",
    "minutt": "minute",
    "minutter": "minutes",

    # Dates
    "januar": "January",
    "februar": "February",
    "mars": "March",
    "april": "April",
    "mai": "May",
    "juni": "June",
    "juli": "July",
    "august": "August",
    "september": "September",
    "oktober": "October",
    "november": "November",
    "desember": "December",
    "jan": "Jan",
    "feb": "Feb",
    "mar": "Mar",
    "apr": "Apr",
    "jun": "Jun",
    "jul": "Jul",
    "aug": "Aug",
    "sep": "Sep",
    "okt": "Oct",
    "nov": "Nov",
    "des": "Dec",

    # States and labels
    "Tilstand": "State",
    "Tilstander": "States",
    "Standard": "Default",
    "Fokus": "Focus",
    "Deaktivert": "Disabled",
    "Aktiver": "Enable",
    "Deaktiver": "Disable",
    "Vist": "Shown",
    "Skjult": "Hidden",

    # Navigation
    "Navigasjon": "Navigation",
    "Navigasjonsfelt": "Navigation Bar",
    "Navigasjonslogikk": "Navigation logic",
    "Meny": "Menu",
    "Undermeny": "Submenu",
    "Bruker-meny": "User menu",
    "Bruker-meny handlinger": "User menu actions",
    "Bruker-meny åpen": "User menu open",

    # Interactions
    "Interaksjon": "Interaction",
    "Interaksjoner": "Interactions",
    "Klikk": "Click",
    "Dobbeltklikk": "Double click",
    "Høyreklikk": "Right click",
    "Hover": "Hover",
    "Scroll": "Scroll",
    "Dra": "Drag",
    "Slipp": "Drop",
    "Tab navigasjon": "Tab navigation",
    "Toggle": "Toggle",
    "Ekspander": "Expand",
    "Kollaps": "Collapse",

    # Modal specific
    "Når vises denne modalen": "When does this modal appear",
    "Modal": "Modal",
    "Dialog": "Dialog",
    "Vindu": "Window",
    "Popup": "Popup",

    # Validation specific terms
    "Forslag til løsning": "Suggested solutions",
    "Vurder å reforhandle disse kostbare oppgavene": "Consider renegotiating these expensive tasks",
    "Foreslåtte WBS-elementer highlightes (gul bakgrunn)": "Suggested WBS items highlighted (yellow background)",
    "Forhandl lavere pris": "Negotiate lower price",
    "Prøv validering igjen": "Try validation again",
    "Budsjett overskredet med": "Budget exceeded by",
    "Prosjektet forsinket til": "Project delayed until",
    "Grense": "Limit",
    "Overskridelse": "Delay",
    "Planvalidering Mislyktes": "Plan Validation Failed",

    # Success/confirmation
    "Gratulerer": "Congratulations",
    "Vellykket": "Successful",
    "Fullført vellykket": "Completed successfully",

    # Tips and help
    "Tips": "Tip",
    "Hjelp": "Help",
    "Onboarding": "Onboarding",
    "Veiledning": "Guidance",
    "Instruksjoner": "Instructions",

    # Steps
    "Steg": "Step",
    "Trinn": "Step",
    "Første gang brukeren logger inn": "First time user logs in",
    "Manuelt via \"?\" ikon i navigasjonsfeltet": "Manually via \"?\" icon in navigation bar",

    # Specific phrases
    "Kom i gang med Nye Hædda Barneskole Simulator": "Get started with Nye Hædda School Simulator",
    "Jeg godtar": "I accept",
    "brukervilkårene": "terms of service",
    "personvernpolicyen": "privacy policy",
    "Har du allerede en konto": "Already have an account",
    "eller": "or",

    # Annotations and documentation
    "Komponenten brukes i": "Component used in",
    "Liste av alle 15 WBS-oppgaver": "List of all 15 WBS tasks",
    "Filtrerbar og sorterbar liste": "Filterable and sortable list",
    "Real-time oppdatering ved forpliktelse": "Real-time update on commitment",
    "Status-indikator farger": "Status indicator colors",
    "Grå": "Gray",
    "Gul": "Yellow",
    "Grønn": "Green",
    "Rød": "Red",
    "Blå": "Blue",
    "knapp": "button",
    "ramme": "border",
    "Inline ved felt": "Inline at field",
    "Rød ramme": "Red border",
    "Knapp deaktivert": "Button disabled",
    "Aktiv side": "Active page",
    "Blå tekst + underline": "Blue text + underline",
    "Lysere grå bakgrunn": "Lighter gray background",
    "Grå → Blå på hover": "Gray → Blue on hover",
    "Initialer fra brukerens navn": "Initials from user's name",
    "Download JSON": "Download JSON",
    "Bekreft modal": "Confirm modal",
    "Redirect til login": "Redirect to login",
    "Real-time validering": "Real-time validation",
    "Vis/skjul passord": "Show/hide password",
    "Enter = submit": "Enter = submit",
    "Min 8 tegn": "Min 8 characters",
    "1 tall": "1 number",
    "1 stort bokstav": "1 uppercase letter",
    "Match": "Match",
    "Må aksepteres": "Must be accepted",
    "Gyldig format": "Valid format",
    "Navn": "Name",

    # Specific task names and descriptions
    "Masseutskifting, grunnmur, drenering, fundamenter": "Excavation, foundation wall, drainage, foundations",
    "Installasjon av vinduer og ytterdører": "Installation of windows and exterior doors",
    "Krav": "Requirements",
    "Fundamentering": "Foundations",
    "Kvalitet": "Quality",
    "Vinduer": "Windows",
    "Dører": "Doors",
    "fullført ✓": "completed ✓",
    "ikke fullført": "not completed",

    # Personas and quotes
    "Pragmatisk og erfaren, fokusert på kvalitet": "Pragmatic and experienced, focused on quality",
    "Strukturert og detaljorientert, streng på kvalitet": "Structured and detail-oriented, strict on quality",
    "Kostnadsbevisst, fleksibel, fokus på fremdrift": "Cost-conscious, flexible, focus on progress",
    "Ambisiøs og konkurransedyktig, utålmodig": "Ambitious and competitive, impatient",

    # Coordination terms
    "Koordinering": "Coordination",
    "Graving": "Excavation",
    "Prosjektledelse": "Project Management",

    # Logic and flow
    "Logikk": "Logic",
    "Filtrer leverandører etter WBS-spesialiteter": "Filter suppliers by WBS specialties",
    "Anbefalte matches vises øverst": "Recommended matches shown first",
    "Klikk kort = velg (blå ramme + checkmark)": "Click card = select (blue border + checkmark)",
    "Chat-side": "Chat page",
    "Vis alle 5 leverandører ↓": "Show all 5 suppliers ↓",

    # Footer and file names
    "med budsjettsporing og WBS-liste": "with budget tracking and WBS list",
    "Leverandørvalg før forhandling": "Supplier selection before negotiation",
    "Valideringsfeil med konkrete forslag": "Validation error with concrete suggestions",
    "Onboarding for nye brukere": "Onboarding for new users",
    "Registreringsside med Supabase auth": "Registration page with Supabase auth",
    "Navigasjonsfelt med bruker-meny": "Navigation bar with user menu",
    "WBS oppgavekort komponenter og tilstander": "WBS task card components and states",

    # Miscellaneous
    "flere oppgaver": "more tasks",
    "Slutt": "End",
    "Avhenger av": "Depends on",
    "Krever 15/15 fullført": "Requires 15/15 completed",
    "Tidsperiode": "Time period",
    "Total": "Total",
    "Kostnad": "Cost",
    "Varighet": "Duration",
    "Ekspander kort eller åpne modal": "Expand card or open modal",
    "Blå ramme, fremhev knapper": "Blue border, highlight buttons",
    "deaktivert hvis avhengigheter": "disabled if dependencies",
    "vis tooltip med årsak": "show tooltip with reason",
    "Vis advarsel hvis budsjett/tidslinje i fare": "Show warning if budget/timeline at risk",
    "Historikk-side": "History page",
    "Bruker": "User",
    "Brukere": "Users",
    "Brukerinfo": "User info",
    "Brukerens": "user's",
    "Utenfor meny": "outside menu",
    "Lukk meny": "Close menu",
    "Ikoner": "Icons",
    "Avatar": "Avatar",
    "Hjelpikon": "Help icon",
    "Historikk": "History",
}

def translate_svg_file(file_path: Path) -> bool:
    """Translate a single SVG file from Norwegian to English."""
    try:
        # Read the file
        content = file_path.read_text(encoding='utf-8')
        original_content = content

        # Sort translations by length (longest first) to avoid partial replacements
        sorted_translations = sorted(TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)

        # Apply translations
        for norwegian, english in sorted_translations:
            content = content.replace(norwegian, english)

        # Check if anything changed
        if content != original_content:
            # Write back the translated content
            file_path.write_text(content, encoding='utf-8')
            print(f"[OK] Translated: {file_path.name}")
            return True
        else:
            print(f"[--] No changes: {file_path.name}")
            return False

    except Exception as e:
        print(f"[ERROR] Error translating {file_path.name}: {e}")
        return False

def main():
    """Main function to translate all SVG files."""
    ux_dir = Path(__file__).parent
    svg_files = sorted(ux_dir.glob("nhb-*.svg"))

    if not svg_files:
        print("No nhb-*.svg files found!")
        return

    print(f"Found {len(svg_files)} SVG files to translate\n")

    translated = 0
    for svg_file in svg_files:
        if translate_svg_file(svg_file):
            translated += 1

    print(f"\nTranslation complete!")
    print(f"Translated: {translated}/{len(svg_files)} files")

if __name__ == "__main__":
    main()
