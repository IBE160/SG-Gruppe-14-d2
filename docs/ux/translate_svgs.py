#!/usr/bin/env python3
"""
Batch translation script for SVG mockups
Translates Norwegian text to English in all nhb-*.svg files
"""

import os
import re
from pathlib import Path

# Comprehensive Norwegian to English translation mapping
TRANSLATIONS = {
    # Titles and headers
    "Gantt-diagram - Prosjektoversikt": "Gantt Chart - Project Overview",
    "Interaktiv tidslinjevisning med kritisk sti og avhengigheter": "Interactive timeline view with critical path and dependencies",
    "Presedensdiagram - Aktiviteter og Avhengigheter": "Precedence Diagram - Activities and Dependencies",
    "AON-diagram (Activity-on-Node) med kritisk sti fremhevet": "AON diagram (Activity-on-Node) with critical path highlighted",
    "Historikk - Prosjektendringer og Beslutninger": "History - Project Changes and Decisions",
    "Kronologisk tidslinje med diff-visning og tilbakestilling": "Chronological timeline with diff view and rollback",
    "Registreringsside - Ny Bruker": "Registration Page - New User",
    "Supabase autentisering med validering og feilhåndtering": "Supabase authentication with validation and error handling",
    "Modal - Leverandørvalg": "Modal - Supplier Selection",
    "Velg leverandør for WBS-oppgave før forhandling starter": "Select supplier for WBS task before negotiation starts",
    "Modal - Forpliktelsesbekreftelse": "Modal - Commitment Confirmation",
    "Kritisk beslutningspunkt: Godkjenne tilbud og oppdatere plan": "Critical decision point: Accept offer and update plan",
    "Modal - Hjelp og Onboarding": "Modal - Help and Onboarding",
    "Veiledning for nye brukere - Hvordan spille simulatoren": "Guidance for new users - How to play the simulator",
    "Modal - Suksess (Plan Godkjent)": "Modal - Success (Plan Approved)",
    "Gratulerer! Brukeren har fullført simuleringen": "Congratulations! User has completed the simulation",
    "Modal - Valideringsfeil": "Modal - Validation Error",
    "Planen oppfyller ikke kravene - vis spesifikke feil og forslag": "Plan does not meet requirements - show specific errors and suggestions",
    "Komponent - WBS Oppgavekort": "Component - WBS Task Card",
    "Ulike tilstander og interaksjoner for Work Breakdown Structure kort": "Various states and interactions for Work Breakdown Structure cards",
    "Komponent - Navigasjonsfelt": "Component - Navigation Bar",
    "Toppnavigasjon med brukerinfo, hjelpikon og handlinger": "Top navigation with user info, help icon and actions",
    "Chat-grensesnitt - AI Forhandling": "Chat Interface - AI Negotiation",
    "Sanntids forhandling med AI-leverandør (Gemini 2.0 Flash)": "Real-time negotiation with AI supplier (Gemini 2.0 Flash)",
    "Dashbord - Hovedoversikt": "Dashboard - Main Overview",
    "Budsjettstyring, WBS-liste og handlingsknapper": "Budget management, WBS list and action buttons",
    "Forhandlingsstrategi - AI Logikk og Beslutningstaking": "Negotiation Strategy - AI Logic and Decision Making",
    "Gemini 2.0 Flash strategier for prisreduksjon og varighet optimalisering": "Gemini 2.0 Flash strategies for price reduction and duration optimization",

    # Navigation and tabs
    "Dashbord": "Dashboard",
    "Gantt-diagram": "Gantt Chart",
    "Presedensdiagram": "Precedence Diagram",
    "Historikk": "History",
    "Leverandører": "Suppliers",

    # Common UI elements
    "Tilbake til Oversikt": "Back to Overview",
    "Tilbake til Planlegging": "Back to Planning",
    "Visning:": "View:",
    "Zoom:": "Zoom:",
    "Filter:": "Filter:",
    "Vis kritisk sti": "Show critical path",
    "Vis fullførte": "Show completed",
    "Vis tidligste starttider": "Show earliest start times",
    "Vis flyt": "Show flow",
    "Layout:": "Layout:",
    "Hierarkisk": "Hierarchical",
    "Måned": "Month",
    "Uke": "Week",
    "Dag": "Day",

    # Months
    "Jan 2025": "Jan 2025",
    "Feb": "Feb",
    "Mar": "Mar",
    "Apr": "Apr",
    "Mai": "May",
    "Juni": "Jun",
    "Juli": "Jul",
    "Aug": "Aug",
    "Sept": "Sep",
    "Okt": "Oct",
    "Nov": "Nov",
    "Des": "Dec",
    "... 2025 ...": "... 2025 ...",
    "Apr 2026": "Apr 2026",
    "Mai 2026": "May 2026",

    # Status and states
    "Fullført": "Completed",
    "Pågår": "In Progress",
    "Planlagt": "Planned",
    "Ikke startet": "Not Started",
    "Forhandler": "Negotiating",
    "Forpliktet": "Committed",
    "Pending": "Pending",
    "Standard": "Default",
    "Fokus": "Focus",
    "Feil": "Error",
    "Hover": "Hover",

    # Buttons and actions
    "Forhandle": "Negotiate",
    "Fortsett chat": "Continue chat",
    "Reforhandle": "Renegotiate",
    "Se detaljer": "View details",
    "Godta": "Accept",
    "Godta tilbud": "Accept offer",
    "Avbryt": "Cancel",
    "Bekreft": "Confirm",
    "Lukk": "Close",
    "Send": "Send",
    "Send Inn Plan": "Submit Plan",
    "Eksporter": "Export",
    "Eksporter Gantt (PNG)": "Export Gantt (PNG)",
    "Eksporter logg": "Export log",
    "Eksporter økt": "Export session",
    "Eksporter Økt (JSON)": "Export Session (JSON)",
    "Eksporter økt (JSON)": "Export session (JSON)",
    "Start simulatoren": "Start simulator",
    "Start Nytt Spill": "Start New Game",
    "Start nytt spill": "Start new game",
    "Hopp over": "Skip",
    "Logg Inn": "Log In",
    "Logg ut": "Log out",
    "Registrer deg": "Sign up",
    "Opprett konto": "Create account",
    "Tilbake": "Back",
    "Neste": "Next",
    "Forrige": "Previous",
    "Avbryt forhandling": "Cancel negotiation",

    # Form fields and labels
    "E-post": "Email",
    "E-postadresse": "Email address",
    "Passord": "Password",
    "Bekreft passord": "Confirm password",
    "Fullt navn": "Full name",
    "Navn": "Name",
    "Bruker": "User",
    "Brukernavn": "Username",
    "din.epost@eksempel.no": "your.email@example.com",
    "Skriv melding...": "Type message...",
    "Husk meg": "Remember me",

    # Validation and errors
    "Feil e-post eller passord": "Invalid email or password",
    "Passordene stemmer ikke overens": "Passwords do not match",
    "Logger inn...": "Logging in...",
    "Planvalidering Mislyktes": "Plan Validation Failed",
    "Feil funnet:": "Errors found:",
    "Budsjett overskredet med": "Budget exceeded by",
    "Prosjektet forsinket til": "Project delayed until",
    "Forslag til løsning:": "Suggested solutions:",
    "Vurder å reforhandle disse kostbare oppgavene:": "Consider renegotiating these expensive tasks:",
    "Tips:": "Tip:",
    "Fokuser på de tre dyreste oppgavene først": "Focus on the three most expensive tasks first",
    "En reduksjon på": "A reduction of",
    "i disse vil bringe deg under budsjettet": "in these will bring you under budget",

    # Success messages
    "Plan Godkjent!": "Plan Approved!",
    "Gratulerer! Du har lykkes med å fullføre": "Congratulations! You have successfully completed",
    "planleggingsfasen for Nye Hædda Barneskole.": "the planning phase for Nye Hædda School.",
    "Gratulerer!": "Congratulations!",

    # Project info
    "Prosjektoversikt": "Project Overview",
    "Prosjektstatus": "Project Status",
    "Prosjektbeskrivelse": "Project Description",
    "Forventet ferdig:": "Expected completion:",
    "Budsjett brukt:": "Budget used:",
    "Kritisk sti:": "Critical path:",
    "Forventet dato:": "Expected date:",
    "Total kostnad:": "Total cost:",
    "Total Kostnad:": "Total Cost:",
    "Fullføringsdato:": "Completion Date:",
    "Tid Brukt:": "Time Spent:",
    "Forhandlinger:": "Negotiations:",
    "Reforhandlinger:": "Renegotiations:",
    "Under budsjett": "Under budget",
    "Før frist": "Before deadline",
    "måneder": "months",
    "mnd": "mo",
    "dager": "days",
    "minutter": "minutes",

    # WBS and tasks
    "WBS-oppgave:": "WBS task:",
    "WBS-oppgaver": "WBS tasks",
    "Avhengigheter:": "Dependencies:",
    "Krav:": "Requirements:",
    "Leverandør:": "Supplier:",
    "Kostnad:": "Cost:",
    "Varighet:": "Duration:",
    "Tidsperiode:": "Time period:",
    "Start → Slutt:": "Start → End:",
    "Siste tilbud:": "Latest offer:",
    "Meldinger:": "Messages:",
    "Tålmodighet:": "Patience:",
    "Status:": "Status:",

    # Task names (keep Norwegian supplier names but translate task descriptions)
    "Prosjektering": "Design",
    "Grunnarbeid": "Foundation Work",
    "Masseutskifting, grunnmur, drenering, fundamenter": "Excavation, foundation wall, drainage, foundations",
    "Råbygg": "Shell Construction",
    "Vinduer/Dører": "Windows/Doors",
    "Vinduer og Dører": "Windows and Doors",
    "Installasjon av vinduer og ytterdører": "Installation of windows and exterior doors",
    "VVS-installasjon": "Plumbing Installation",
    "VVS": "Plumbing",
    "Elektrisk": "Electrical",
    "Maling": "Painting",
    "Maling og Overflatebehandling": "Painting and Surface Treatment",
    "Gulv": "Flooring",
    "Inspeksjon": "Inspection",

    # Supplier info
    "Totalentreprenør": "General Contractor",
    "Byggeleder": "Construction Manager",
    "Graveentreprenør": "Excavation Contractor",
    "Prosjektleder": "Project Manager",
    "Spesialiteter:": "Specialties:",
    "Leverandørinformasjon": "Supplier Information",
    "Tilgjengelige leverandører": "Available suppliers",
    "Anbefalte match for denne oppgaven": "Recommended match for this task",

    # Descriptions and quotes
    '"Pragmatisk og erfaren, fokusert på kvalitet"': '"Pragmatic and experienced, focused on quality"',
    '"Strukturert og detaljorientert, streng på kvalitet"': '"Structured and detail-oriented, strict on quality"',
    '"Kostnadsbevisst, fleksibel, fokus på fremdrift"': '"Cost-conscious, flexible, focus on progress"',
    '"Ambisiøs og konkurransedyktig, utålmodig"': '"Ambitious and competitive, impatient"',

    # Help and onboarding
    "Velkommen til Simulatoren!": "Welcome to the Simulator!",
    "Velkommen til simulatoren!": "Welcome to the simulator!",
    "Lær hvordan du planlegger Nye Hædda Barneskole prosjektet": "Learn how to plan the Nye Hædda School project",
    "Kom i gang med Nye Hædda Barneskole Simulator": "Get started with Nye Hædda School Simulator",
    "Forstå budsjettet og tidsfristen": "Understand the budget and deadline",
    "Budsjett: 700 MNOK | Frist: 15. mai 2026": "Budget: 700 MNOK | Deadline: May 15, 2026",
    "Du må holde deg innenfor disse grensene for å lykkes": "You must stay within these limits to succeed",
    "Velg WBS-oppgaver å forhandle": "Select WBS tasks to negotiate",
    "oppgaver fra prosjektering til ferdigstillelse": "tasks from design to completion",
    "Start med avhengige oppgaver (grunnarbeid først)": "Start with dependent tasks (foundation work first)",
    "Forhandle med AI-leverandører": "Negotiate with AI suppliers",
    "Chat med 5 unike leverandør-personligheter": "Chat with 5 unique supplier personalities",
    "Bruk strategier som partnerskap, volum, eller fleksibilitet": "Use strategies like partnership, volume, or flexibility",
    "Send inn planen din": "Submit your plan",
    "Valider at planen oppfyller kravene": "Validate that the plan meets requirements",
    "Hvis feil oppstår, reforhandle de dyreste oppgavene": "If errors occur, renegotiate the most expensive tasks",
    "Lagre regelmessig med": "Save regularly with",
    "for å ikke miste fremgangen din": "to not lose your progress",
    "Sjekk kritisk sti i Gantt-diagrammet for å identifisere flaskehalser": "Check critical path in Gantt chart to identify bottlenecks",

    # History and timeline
    "Økt opprettet": "Session created",
    "Bruker registrert og autentisert via Supabase": "User registered and authenticated via Supabase",
    "Forhandling godtatt:": "Negotiation accepted:",
    "Budsjettvarsel": "Budget warning",
    "Total:": "Total:",
    "Grense:": "Limit:",
    "oppgaver gjenstår": "tasks remaining",
    "Reforhandlet:": "Renegotiated:",
    "Pris redusert:": "Price reduced:",
    "Validering feilet": "Validation failed",
    "Tidslinje OK": "Timeline OK",
    "Sammenligning:": "Comparison:",
    "Attributt": "Attribute",
    "Før": "Before",
    "Etter": "After",
    "Påvirkning på prosjekt:": "Impact on project:",
    "Budget:": "Budget:",
    "Nytt totalbudsjett:": "New total budget:",
    "Under budsjettgrense:": "Under budget limit:",
    "buffer": "buffer",
    "Tidslinje:": "Timeline:",
    "Uendret": "Unchanged",
    "Forhandlingssammenheng:": "Negotiation context:",
    "Årsak:": "Reason:",
    "Budsjett i faresonen": "Budget at risk",
    "Strategi brukt:": "Strategy used:",
    "Appellert til langsiktig partnerskap": "Appealed to long-term partnership",
    "Leverandør reaksjon:": "Supplier reaction:",
    "Aksepterte": "Accepted",
    "prisreduksjon": "price reduction",
    "Forrige hendelse": "Previous event",
    "Neste hendelse": "Next event",
    "Tilbakestill til dette punktet": "Restore to this point",

    # Registration
    "Opprett konto": "Create account",
    "Kom i gang med": "Get started with",
    "Jeg godtar": "I accept",
    "brukervilkårene": "terms of service",
    "personvernpolicyen": "privacy policy",
    " og ": " and ",
    "Har du allerede en konto?": "Already have an account?",
    "Logg inn her": "Log in here",
    "Passordkrav:": "Password requirements:",
    "Minst 8 tegn": "At least 8 characters",
    "Ett tall": "One number",
    "Ett stort bokstav": "One uppercase letter",
    "Sterkt passord": "Strong password",
    "Validering:": "Validation:",
    "Påkrevd": "Required",
    "Gyldig format": "Valid format",
    "Match": "Match",
    "Må aksepteres": "Must be accepted",

    # Commitment confirmation
    "Bekreft Forpliktelse": "Confirm Commitment",
    "Dette vil oppdatere prosjektplanen din.": "This will update your project plan.",
    "Fortsette?": "Continue?",
    "Interaksjoner:": "Interactions:",
    "Klikk": "Click",
    "Modal vises": "Modal appears",
    "Plan oppdateres (localStorage)": "Plan updates (localStorage)",
    "Toast notification:": "Toast notification:",
    "lagt til i plan": "added to plan",
    "System message": "System message",
    "Tilbud godtatt...": "Offer accepted...",
    "Redirect til Dashboard etter 1 sekund": "Redirect to Dashboard after 1 second",
    "Beregninger:": "Calculations:",
    "Start-dato:": "Start date:",
    "Basert på avhengigheter": "Based on dependencies",
    "Hvis ingen:": "If none:",
    "prosjektstart": "project start",
    "Hvis avhengig:": "If dependent:",
    "Siste end_date + 1 dag": "Last end_date + 1 day",
    "Slutt-dato:": "End date:",
    "Start + varighet": "Start + duration",
    "Sum alle current_plan.cost": "Sum all current_plan.cost",
    "Max end_date fra plan": "Max end_date from plan",

    # Supplier selection
    "Velg Leverandør for Forhandling": "Select Supplier for Negotiation",
    "Anbefalte matches vises øverst": "Recommended matches shown first",
    "Klikk kort = velg (blå ramme + checkmark)": "Click card = select (blue border + checkmark)",
    "Start forhandling med": "Start negotiation with",
    "Start forhandling": "Start negotiation",
    "Vis alle": "Show all",
    "leverandører": "suppliers",
    "Når vises denne modalen?": "When does this modal appear?",
    "på en WBS-oppgave uten leverandør": "on a WBS task without supplier",
    "Eller klikk": "Or click",
    "for å bytte leverandør": "to change supplier",
    "Logikk:": "Logic:",
    "Filtrer leverandører etter WBS-spesialiteter": "Filter suppliers by WBS specialties",

    # Navigation component
    "Innstillinger": "Settings",
    "Navigasjonsfelt": "Navigation bar",
    "Navigasjonslogikk:": "Navigation logic:",
    "Aktiv side:": "Active page:",
    "Blå tekst + underline": "Blue text + underline",
    "Lysere grå bakgrunn": "Lighter gray background",
    "Ikoner:": "Icons:",
    "Grå → Blå på hover": "Gray → Blue on hover",
    "Avatar:": "Avatar:",
    "Initialer fra brukerens navn": "Initials from user's name",
    "Bruker-meny handlinger:": "User menu actions:",
    "Download JSON": "Download JSON",
    "Bekreft modal": "Confirm modal",
    "Supabase.auth.signOut()": "Supabase.auth.signOut()",
    "Redirect til login": "Redirect to login",

    # WBS Card component
    "tilstander:": "states:",
    "Hver kort viser:": "Each card shows:",
    "Handlinger:": "Actions:",
    "Status-indikator:": "Status indicator:",
    "Farget sirkel": "Colored circle",
    "Grå:": "Gray:",
    "Gul:": "Yellow:",
    "Grønn + ✓:": "Green + ✓:",
    "Blå ramme, fremhev knapper": "Blue border, highlight buttons",
    "Komponenten brukes i:": "Component used in:",
    "Liste av alle": "List of all",
    "Filtrerbar og sorterbar liste": "Filterable and sortable list",
    "Real-time oppdatering ved forpliktelse": "Real-time update on commitment",
    "knapp deaktivert hvis avhengigheter": "button disabled if dependencies",
    "ikke er fullført (vis tooltip med årsak)": "are not completed (show tooltip with reason)",
    "Vis advarsel hvis budsjett/tidslinje i fare": "Show warning if budget/timeline at risk",
    "ikke fullført": "not completed",
    "fullført ✓": "completed ✓",
    "venter": "waiting",

    # Gantt chart
    "Idag ↓": "Today ↓",
    "total": "total",
    "Kritisk": "Critical",
    "Se diff": "View diff",
    "Se detaljer →": "View details →",
    "Nå": "Now",
    "Endring:": "Change:",
    "Vis suksess-data": "View success data",

    # Precedence diagram
    "Forklaring:": "Legend:",
    "AI Prosess": "AI Process",
    "Beslutning": "Decision",
    "Handling": "Action",
    "Data/State": "Data/State",
    "Valgt oppgave:": "Selected task:",
    "Påvirker:": "Affects:",
    "oppgaver venter": "tasks waiting",
    "Lengste vei gjennom nettverket:": "Longest path through network:",
    "Total varighet:": "Total duration:",
    "Flyt (slack):": "Float (slack):",
    "Ingen buffer - forsinkelser påvirker sluttdato": "No buffer - delays affect end date",

    # Negotiation strategy flow
    "Bruker sender": "User sends",
    "motbud / melding": "counter-offer / message",
    "via chat-grensesnitt": "via chat interface",
    "Analyser meldingen for:": "Analyze message for:",
    "Prisfokus?": "Price focus?",
    "Tidsfokus?": "Time focus?",
    "Forhandlingsstrategi?": "Negotiation strategy?",
    "partnerskap": "partnership",
    "kvalitet": "quality",
    "volum": "volume",
    "Leverandør-personlighet": "Supplier personality",
    "Vurder bruker strategi:": "Evaluate user strategy:",
    "Reduser": "Reduce",
    "Vurder forhold:": "Evaluate relationship:",
    "Jeg har ikke mer tid": "I don't have more time",
    "Beregn Nytt Tilbud": "Calculate New Offer",
    "Avhenger av:": "Depends on:",
    "market_factor, constraints, patience": "market_factor, constraints, patience",
    "Er nytt tilbud innenfor grenser?": "Is new offer within limits?",
    "Min pris:": "Min price:",
    "Max varighet:": "Max duration:",
    "Send nytt tilbud": "Send new offer",
    "Avslå": "Reject",
    "Beklager, jeg kan ikke": "Sorry, I cannot",
    "gå lavere enn...": "go lower than...",
    "Oppdater Tilstand": "Update State",
    "Forhandlingsstrategier for Bruker": "Negotiation Strategies for User",
    "Langsiktig partnerskap": "Long-term partnership",
    "Eksempel melding:": "Example message:",
    "Vi ønsker en langsiktig partner for": "We want a long-term partner for",
    "fremtidige prosjekter.": "future projects.",
    "Effekt:": "Effect:",
    "Volumargument": "Volume argument",
    "Vi har flere oppgaver som passer": "We have multiple tasks that fit",
    "deres spesialiteter.": "your specialties.",
    "Tidsfleksibilitet": "Time flexibility",
    "Vi kan være fleksible på tidslinje": "We can be flexible on timeline",
    "hvis det gir bedre pris.": "if it gives better price.",
    "Kvalitetsfokus": "Quality focus",
    "Kvalitet er viktigst for oss,": "Quality is most important to us,",
    "kan dere redusere tid?": "can you reduce time?",
    "Direkte prispress (Risiko)": "Direct price pressure (Risk)",
    "Det er for dyrt. Kan dere": "That's too expensive. Can you",
    "gå ned til": "go down to",
    "blir utålmodig": "becomes impatient",
    "Bruk": "Use",
    "mykere": "softer",
    "strategier først": "strategies first",
    "Match strategi med leverandørpersonlighet": "Match strategy with supplier personality",
    "For mange forsøk reduserer effektivitet": "Too many attempts reduce effectiveness",

    # Specifications
    "Tilstander:": "States:",
    "Ren skjema": "Clean form",
    "Blå ramme": "Blue border",
    "Rød tekst under": "Red text below",
    "Spesifikasjoner:": "Specifications:",
    "Kortbredde:": "Card width:",
    "fast": "fixed",
    "Bakgrunn:": "Background:",
    "Input høyde:": "Input height:",
    "Knapp høyde:": "Button height:",
    "inni kort": "inside card",
    "kort": "card",
    "Tab-navigasjon:": "Tab navigation:",
    "i passord-felt → Submit": "in password field → Submit",
    "Redirect til /dashboard": "Redirect to /dashboard",

    # Chat interface
    "Hei! Jeg er": "Hi! I'm",
    "fra": "from",
    "Jeg har mottatt": "I have received",
    "Dette inkluderer": "This includes",
    "Hei": "Hi",
    "Jeg trenger et pristilbud for denne oppgaven.": "I need a price quote for this task.",
    "Hva kan dere tilby når det gjelder kostnad og varighet?": "What can you offer in terms of cost and duration?",
    "Basert på spesifikasjonene og nåværende markedspriser, estimerer jeg": "Based on specifications and current market prices, I estimate",
    "for": "for",
    "Dette dekker alle krav i": "This covers all requirements in",
    "og sikrer": "and ensures",
    "kvalitet og fremdrift.": "quality and progress.",
    "Takk for tilbudet.": "Thank you for the offer.",
    "er litt høyt for vårt budsjett.": "is a bit high for our budget.",
    "Kan dere gå ned i pris hvis vi er fleksible på tidslinje?": "Can you reduce the price if we are flexible on timeline?",
    "krever kun standard": "only requires standard",
    "ser gjennom spesifikasjonene...": "is reviewing specifications...",
    "Dokumenter": "Documents",
    "Detaljer": "Details",
    "Kravspesifikasjon": "Requirements Specification",
    "Forhandlingsstatus": "Negotiation Status",
    "utvekslet": "exchanged",

    # Dashboard
    "Budsjettrammer": "Budget Constraints",
    "Tidsfrist": "Deadline",
    "Forventet fullføring": "Expected Completion",
    "margin": "margin",
    "WBS Oppgaver": "WBS Tasks",
    "Alle": "All",
    "Fullførte": "Completed",
    "Gjenstående": "Remaining",
    "Handlinger": "Actions",
    "Eksporter til JSON": "Export to JSON",
    "Tilbakestill Simulering": "Reset Simulation",
    "Nyttige Tips": "Useful Tips",
    "Planlegg de dyreste oppgavene nøye": "Plan the most expensive tasks carefully",
    "Sjekk avhengigheter før forhandling": "Check dependencies before negotiation",
    "Bruk historikken til å spore endringer": "Use history to track changes",
    "Fremdrift": "Progress",
    "Auto-lagring aktivert": "Auto-save enabled",

    # Common footer text patterns
    "mockup med tilstander": "mockup with states",
    "Interaktiv": "Interactive",
    "med": "with",
    "og": "and",
}

def translate_file(filepath):
    """Translate a single SVG file from Norwegian to English"""
    print(f"Translating: {filepath.name}")

    content = filepath.read_text(encoding='utf-8')
    original_content = content

    # Sort translations by length (longest first) to avoid partial replacements
    sorted_translations = sorted(TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)

    # Apply translations
    for norwegian, english in sorted_translations:
        content = content.replace(norwegian, english)

    # Write back if changed
    if content != original_content:
        filepath.write_text(content, encoding='utf-8')
        print(f"  [OK] Translated {filepath.name}")
        return True
    else:
        print(f"  [-] No changes for {filepath.name}")
        return False

def main():
    """Main translation function"""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent

    # Find all nhb-*.svg files
    svg_files = sorted(script_dir.glob('nhb-*.svg'))

    if not svg_files:
        print("No nhb-*.svg files found in current directory")
        return

    print(f"Found {len(svg_files)} SVG files to translate\n")

    translated_count = 0
    for svg_file in svg_files:
        if translate_file(svg_file):
            translated_count += 1

    print(f"\n{'='*60}")
    print(f"Translation complete!")
    print(f"Translated: {translated_count}/{len(svg_files)} files")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
