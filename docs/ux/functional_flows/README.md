# Flow Diagrams - Nye Hædda Barneskole POC

**Opprettet:** 2025-12-12
**Formål:** Detaljerte flytdiagrammer for regellogikk, beregninger, og brukerflyter
**Målgruppe:** Frontend utviklere, backend utviklere, systemarkitekter

---

## 📁 FILSTRUKTUR

```
/docs/ux/flows/
├── flow-01-validation-rules.svg           # Valideringsregler (budsjett + tid)
├── flow-02-budget-calculation.svg         # 3-tier budsjettberegning
├── flow-03-ai-agent-negotiation.svg       # AI agent forhandlingslogikk
├── flow-04-commitment-uncommitment.svg    # Eksplisitt accept/reject flyt
├── flow-05-state-management.svg           # Frontend/Backend state sync
├── flow-06-error-handling.svg             # Feilhåndtering og brukermeldinger
├── flow-07-critical-path-timeline.svg     # Kritisk sti og CPM beregning
├── visualization-01-gantt-chart.svg       # Gantt-diagram (15 WBS pakker)
├── visualization-02-precedence-diagram.svg # Precedence diagram (AON format)
└── README.md                               # Denne filen
```

---

## 🎯 OVERSIKT

Disse flytdiagrammene gir **komplett teknisk dokumentasjon** for:
- **Regellogikk**: Hva er tillatt/ikke tillatt i systemet
- **Beregningsformler**: Hvordan budsjett, tid, og validering beregnes
- **Brukerflyter**: Hvordan bruker interagerer med systemet (commitment, reforhandling)
- **Teknisk implementering**: Konkrete kodeeksempler og API-struktur

---

## 📋 FLOW DIAGRAMMER

### 1. flow-01-validation-rules.svg
**Valideringsregler - Komplett Logikk**

**Dekker:**
- Budsjettvalidering: `total ≤ 700 MNOK`
- Tidsfristvalidering: `project_end ≤ 15 Mai 2026`
- Ufullstendig plan advarsel
- Feilmeldinger og handlingsforslag

**Viktige regler:**
- Total budsjett = Locked (390) + Committed (sum)
- Kritisk sti beregning for prosjektslutt
- Eier kan ALDRI forlenge tid

**For utviklere:**
- Frontend validering (UI feedback)
- Backend validering (API)
- Error response format

---

### 2. flow-02-budget-calculation.svg
**Budsjettberegning - 3-Tier Modell**

**Dekker:**
- **Tier 1**: Tilgjengelig (0-310 MNOK, dynamisk)
- **Tier 2**: Låst (390 MNOK, konstant)
- **Tier 3**: Totalt (390 + used, dynamisk)
- Echtidsoppdatering ved commitment
- Budsjettstatuser (god, advarsel, kritisk, over budsjett)

**Formler:**
```javascript
tier1_used = sum(committed_wbs_costs)
tier1_remaining = 310 - tier1_used
tier3_total = 390 + tier1_used
```

**For utviklere:**
- React state struktur (`BudgetState` interface)
- Progressbar fargekodning (grønn/gul/rød)
- API endpoints for budsjettoppdatering

---

### 3. flow-03-ai-agent-negotiation.svg
**AI-Agent Forhandlingslogikk**

**Dekker:**
- **3 Leverandører** (Bjørn, Kari, Per)
  - Forhandlingsmuligheter: Pris, kvalitet, tid
  - Skjulte parametere (min pris, concession rate)
  - Eksempler på forhandlingsrunder
- **1 Eier** (Anne-Lise Berg)
  - Budsjettøkning: Maks 15% (47 MNOK total)
  - Scope-reduksjon: Godkjenning påkrevd
  - **Tidsforlengelse: ALDRI tillatt**

**Viktige regler:**
- Leverandører har minimum pris (85-88% av baseline)
- Eier krever STERK begrunnelse for budsjettøkning
- AI agents blir mer fastlåst etter 3-4 forhandlingsrunder

**For utviklere:**
- Google Gemini API system prompts
- Agent state tracking (rounds, current offer)
- Negotiation history persistence

---

### 4. flow-04-commitment-uncommitment.svg
**Commitment & Uncommitment Flyt**

**Dekker:**
- **Commitment**: Bruker godtar tilbud → Bekreftelsesmodal → State update → Budsjett recalculate
- **Uncommitment**: Bruker reforhandler → Advarselsmodal → Fjern commitment → Frigjør budsjett
- WBS pakke statuser: `pending` → `negotiating` → `committed`
- Eksplisitt accept/reject (ingen automatisk commitment)

**Datamodell:**
```typescript
interface WBSItem {
  status: 'pending' | 'negotiating' | 'committed'
  committed_cost?: number
  committed_duration?: number
}
```

**For utviklere:**
- Modal design (bekreftelse, advarsel)
- API endpoints: `POST /api/wbs/:id/commit`, `DELETE /api/wbs/:id/uncommit`
- Optimistic UI updates

---

### 5. flow-05-state-management.svg
**State Management Arkitektur**

**Dekker:**
- **Frontend State**: React state (wbsItems, budget, timeline, activeChat)
- **Backend State**: Session state (commitments, negotiation history, AI agent state)
- **Database**: PostgreSQL (persistent storage)
- Synkronisering mellom frontend ↔ backend ↔ database

**State struktur:**
```typescript
interface AppState {
  user: User
  wbsItems: WBSItem[]
  budget: BudgetState
  timeline: TimelineState
  activeChat: ChatState
}
```

**For utviklere:**
- Optimistic updates pattern
- Single source of truth (database)
- Error handling og retry logic

---

### 6. flow-06-error-handling.svg
**Feilhåndtering og Brukermeldinger**

**Dekker:**
- **Kritiske feil**: `OVER_BUDGET`, `PAST_DEADLINE` (blokkerer fortsettelse)
- **Advarsler**: `INCOMPLETE_PLAN` (tillater fortsettelse)
- **Nettverksfeil**: `NETWORK_ERROR`, `AI_AGENT_ERROR`
- Feilmodal design og brukermelding format

**Feilmodal struktur:**
- Header (tittel med ikon)
- Body (problem, detaljer, foreslåtte handlinger)
- Footer (knapper: "Til Dashboard", "Reforhandle", "Kontakt Eier")

**For utviklere:**
- Error handling function (`handleError(error)`)
- Modal component props
- User-friendly error messages i norsk

---

### 7. flow-07-critical-path-timeline.svg
**Kritisk Sti og Tidslinjeberegning**

**Dekker:**
- **Prosjekttidslinje**: Start 15 Feb 2025, Frist 15 Mai 2026 (455 dager)
- **Kritisk sti**: WBS 1.3.1 → 1.3.2 → 1.4.1 (sekvensiell, finish-to-start)
- **Parallelle pakker**: 12 låste pakker (ikke på kritisk sti)
- CPM beregning (Critical Path Method)

**Baseline scenario:**
- WBS 1.3.1: 60 dager
- WBS 1.3.2: 45 dager
- WBS 1.4.1: 90 dager
- **Total**: 195 dager (6.5 måneder)
- **Buffer**: 260 dager ✅ God margin

**For utviklere:**
- `calculateProjectEnd(wbsItems)` funksjon
- Tidsfristvalidering (`endDate <= DEADLINE`)
- Gantt chart data preparation

---

### 8. visualization-01-gantt-chart.svg
**Gantt-Diagram - Prosjekttidslinje**

**Dekker:**
- **15 WBS pakker** visualisert over tidslinje (Feb 2025 - Mai 2026)
- **Kritisk sti** (3 forhandlingsbare pakker - rød)
- **12 låste pakker** (parallelle aktiviteter - grå)
- Milepæler og frist (15 Mai 2026)
- Interaktive funksjoner (zoom, klikk på pakke, vis/skjul)

**Tidslinje:**
- Start: 15 Februar 2025
- Baseline slutt: 30 August 2025 (195 dager)
- Frist: 15 Mai 2026 (ufravikelig)
- Buffer: 260 dager ✅

**For utviklere:**
- Gantt chart component design
- Data format: `{ id, name, start, duration, cost, critical, status }`
- Bar positioning algorithm
- Real-time update på commitment

---

### 9. visualization-02-precedence-diagram.svg
**Precedence Diagram (AON) - Nettverksdiagram**

**Dekker:**
- **Activity-on-Node (AON)** format
- **Kritisk sti** fremhevet (rød)
- **Finish-to-Start (FS)** avhengigheter
- **Float beregning** (Total Float for hver node)
- ES, EF, LS, LF verdier

**Nøkkelkonsepter:**
- Kritisk sti: Float = 0 (ingen slakk tid)
- Ikke-kritiske aktiviteter: Float > 0
- CPM algoritme (Forward Pass, Backward Pass)
- Parallelle aktiviteter visualisert

**For utviklere:**
- Network diagram layout algorithm
- CPM calculation implementation
- Interactive hover (vis ES/EF/LS/LF)
- Critical path highlighting

---

## 🔧 IMPLEMENTERINGSGUIDE

### Hvordan Bruke Disse Diagrammene

1. **Frontend Utviklere:**
   - Se `flow-02-budget-calculation.svg` for UI-komponenter og progressbarer
   - Se `flow-04-commitment-uncommitment.svg` for modal design og brukerinteraksjon
   - Se `flow-05-state-management.svg` for React state struktur
   - Se `flow-06-error-handling.svg` for feilmeldinger og error modals

2. **Backend Utviklere:**
   - Se `flow-01-validation-rules.svg` for API validering
   - Se `flow-03-ai-agent-negotiation.svg` for Google Gemini integration
   - Se `flow-05-state-management.svg` for session state og database schema
   - Se `flow-07-critical-path-timeline.svg` for CPM beregning

3. **Systemarkitekter:**
   - Se alle flyter for fullstendig forståelse av regellogikk
   - Bruk som referanse ved design review
   - Valider at implementering følger spesifikasjoner

---

## 💡 VIKTIGE KONSEPTER

### Budsjettmodell (3-Tier):
```
Tier 1: Tilgjengelig (0-310 MNOK)     [Dynamisk]
Tier 2: Låst (390 MNOK)               [Konstant]
Tier 3: Totalt (390 + used)           [Dynamisk]
```

### Kritiske Regler:
1. **Budsjett**: Maks 700 MNOK total (390 låst + 310 tilgjengelig)
2. **Tid**: UFRAVIKELIG frist 15 Mai 2026 (Eier kan ALDRI forlenge)
3. **Kritisk sti**: WBS 1.3.1 → 1.3.2 → 1.4.1 (sekvensiell)
4. **Eksplisitt valg**: Bruker må aktivt godta/avslå tilbud (ingen auto-commit)

### AI Agent Regler:
- **Leverandører**: Min pris 85-88% av baseline, blir fastere etter 3-4 runder
- **Eier**: Maks budsjettøkning 15% (47 MNOK), krever sterk begrunnelse
- **Tid**: Eier kan ALDRI godkjenne tidsforlengelse (hard-kodet)

---

## 📊 DATAFLYT

```
User Action (Frontend)
    ↓
React State Update (Optimistic)
    ↓
API Call (Backend)
    ↓
Business Logic + Validation
    ↓
Database Update (Supabase)
    ↓
Response → Frontend
    ↓
Confirm State Update (or Rollback if error)
```

---

## ✅ KVALITETSKONTROLL

Alle flytdiagrammer er:
- ✅ Konsistente med PRD.md (390/310/700 MNOK budsjettmodell)
- ✅ Viser 35 MNOK deficit fra start
- ✅ Inkluderer konkrete kodeeksempler
- ✅ Dokumenterer ALLE kritiske regler
- ✅ Norsk språk for brukermeldinger
- ✅ Engelsk for kode/interfaces

---

## 🔗 RELATERTE FILER

**Mockups:**
- `/docs/ux/final-screen-02-dashboard-main.svg` - Dashboard med 3-tier budget display
- `/docs/ux/final-screen-03-chat-interface.svg` - Chat interface med accept/reject knapper
- `/docs/ux/final-flow-03-negotiation-strategies.svg` - 3 forhandlingsstrategier

**Dokumentasjon:**
- `/docs/PRD.md` - Product Requirements Document
- `/docs/AI_AGENT_SYSTEM_PROMPTS.md` - AI agent system prompts (med 35 MNOK deficit context)
- `/docs/ux-design-specification.md` - UX design spesifikasjoner

**Implementering:**
- `/docs/IMPLEMENTATION_PLAN_DEC_9-15.md` - Sprint 1-2 plan
- `/docs/REVISED_IMPLEMENTATION_PLAN_DEC_12-18.md` - Revidert Sprint 1-4 plan

---

## 📝 ENDRINGSLOGG

**2025-12-12:**
- Opprettet alle 7 flow diagrammer
- Konsistent budsjettmodell (390/310/700 MNOK)
- 35 MNOK deficit inkludert i alle relevante flyter
- Komplette kodeeksempler og API design
- Norske brukermeldinger

---

## 🎯 KONKLUSJON

Disse flytdiagrammene gir **komplett teknisk dokumentasjon** for implementering av Nye Hædda Barneskole POC.

**Bruk disse diagrammene til:**
- ✅ Forstå regellogikk og forretningsregler
- ✅ Implementere frontend komponenter (UI, state, validation)
- ✅ Implementere backend API (validation, AI integration, database)
- ✅ Debugge og feilsøke under utvikling
- ✅ Onboarding av nye utviklere

**Alle flyter er produksjonsklare og kan brukes direkte i Sprint 1-4 implementering.**
