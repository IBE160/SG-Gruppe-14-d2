# Visualization Implementation Checklist
## Ensuring Library Implementation Matches UX Flow Designs

**Document Version:** 1.0
**Date:** December 16, 2025
**Purpose:** Verify that gantt-task-react and ReactFlow implementations match the designs in `docs/ux/functional_flows/`

---

## Overview

This checklist ensures that the library-based visualization implementation (gantt-task-react + ReactFlow) produces the exact visual output specified in the UX flow designs:
- `docs/ux/functional_flows/visualization-01-gantt-chart.svg`
- `docs/ux/functional_flows/visualization-02-precedence-diagram.svg`

All functional requirements from **PRD.md FR-9.1 and FR-9.2** must be met, only the rendering mechanism differs.

---

## 🎨 GANTT CHART CHECKLIST (gantt-task-react)

### Installation & Setup
- [ ] Install gantt-task-react: `npm install gantt-task-react`
- [ ] Install TypeScript types: `npm install --save-dev @types/gantt-task-react`
- [ ] Import CSS: `import 'gantt-task-react/dist/index.css'`
- [ ] Create component: `frontend/components/gantt-chart.tsx`

### Timeline Requirements (FR-9.1)
- [ ] Timeline spans: **February 2025 to May 2026** (project start to deadline)
- [ ] Month view mode enabled by default (`ViewMode.Month`)
- [ ] Norwegian locale configured (`locale="nb-NO"`)
- [ ] Timeline header shows months with year labels
- [ ] Today marker visible (blue vertical line)
- [ ] Deadline marker visible (May 15, 2026 - red vertical line)

### Task Bar Display (FR-9.1)
- [ ] All 15 WBS items displayed as task bars
- [ ] Task bars show:
  - WBS ID and name (e.g., "1.4.1 - Råbygg")
  - Duration visible on hover or in task bar
  - Start and end dates accessible
- [ ] Task bar positioning:
  - Positioned according to earliest start/finish dates from timeline calculation
  - Width proportional to task duration

### Color Scheme (CRITICAL - Must Match Design)
- [ ] **Critical path tasks:** Red bars (`#ef4444`)
- [ ] **Negotiable tasks:** Green bars (`#22c55e`)
- [ ] **Locked tasks:** Gray bars (`#9ca3af`)
- [ ] **Committed tasks:** Solid fill (100% progress)
- [ ] **Uncommitted tasks:** Outlined/dashed appearance (0% progress)

### Dependencies & Critical Path (FR-9.1)
- [ ] Dependency arrows visible between tasks
- [ ] Normal dependencies: Gray arrows
- [ ] Critical path dependencies: Red arrows (or differentiated styling)
- [ ] Critical path tasks have distinct red coloring

### Legend (FR-9.1)
- [ ] Legend displayed below chart
- [ ] Legend items:
  - Red box: "Kritisk sti" (Critical path)
  - Green box: "Forhandlet" (Negotiable)
  - Gray box: "Låst" (Locked)
  - Dashed box: "Ikke forpliktet" (Not committed)

### Interactive Controls (FR-9.1)
- [ ] View modes available: Month / Week / Day
- [ ] Zoom controls functional (gantt-task-react built-in)
- [ ] Scroll horizontally for full timeline
- [ ] Task click/hover shows details

### Real-time Updates (FR-9.1)
- [ ] Chart re-renders when new commitment added
- [ ] Chart re-renders when commitment removed (renegotiation)
- [ ] Budget updates trigger chart refresh
- [ ] Timeline recalculation triggers chart refresh

### Data Integration
- [ ] WBS items loaded from `wbs.json` or database
- [ ] Commitments loaded from `wbs_commitments` table
- [ ] Timeline data (ES/EF) loaded from validation endpoint
- [ ] Critical path data loaded from validation endpoint

---

## 🔀 PRECEDENCE DIAGRAM CHECKLIST (ReactFlow)

### Installation & Setup
- [ ] Install ReactFlow: `npm install reactflow`
- [ ] Import CSS: `import 'reactflow/dist/style.css'`
- [ ] Create component: `frontend/components/precedence-diagram.tsx`
- [ ] Import required ReactFlow components: `Node`, `Edge`, `Controls`, `Background`, `useNodesState`, `useEdgesState`

### Node Requirements (FR-9.2)
- [ ] All 15 WBS items displayed as nodes (rectangular boxes)
- [ ] Node content displays:
  - WBS ID (e.g., "1.4.1") - bold, top
  - Task name (e.g., "Råbygg") - below ID, truncated if >20 chars
  - Duration in days - middle section
  - **ES (Earliest Start)** - bottom left
  - **EF (Earliest Finish)** - bottom left
  - **LS (Latest Start)** - bottom right
  - **LF (Latest Finish)** - bottom right
  - **Slack time** - bottom right (e.g., "Slack: 15d" or "KRITISK")

### Node Styling (CRITICAL - Must Match Design)
- [ ] **Critical path nodes:**
  - Background: Light red (`#fee2e2`)
  - Border: Red, 3px thick (`#ef4444`)
  - Text: Dark red for emphasis
- [ ] **Non-critical nodes:**
  - Background: Light gray (`#f3f4f6`)
  - Border: Gray, 2px thick (`#9ca3af`)
  - Text: Standard gray
- [ ] Node size: ~180px width, auto height based on content
- [ ] Border radius: 8px (rounded corners)

### Edge Requirements (FR-9.2)
- [ ] Dependency arrows connect nodes based on WBS dependencies
- [ ] **Critical path edges:**
  - Color: Red (`#ef4444`)
  - Width: 3px thick
  - Animated (ReactFlow `animated: true`)
- [ ] **Normal edges:**
  - Color: Gray (`#9ca3af`)
  - Width: 2px thick
  - Not animated
- [ ] Arrow markers at end of edges (`MarkerType.ArrowClosed`)
- [ ] Edge type: `smoothstep` (smooth routing, no collisions)

### Layout & Positioning (FR-9.2)
- [ ] Auto-layout algorithm positions nodes (grid layout: 5 columns)
- [ ] Nodes draggable for manual repositioning
- [ ] Zoom and pan controls available (ReactFlow built-in)
- [ ] Fit-to-view on initial load (`fitView` prop)
- [ ] No node overlaps
- [ ] Edges route smoothly around nodes

### Interactive Controls (FR-9.2)
- [ ] Zoom in/out controls visible
- [ ] Pan control visible
- [ ] Fit view button available
- [ ] Background grid displayed (`<Background />`)
- [ ] Controls panel displayed (`<Controls />`)

### Legend (FR-9.2)
- [ ] Legend displayed below diagram
- [ ] Legend items:
  - Red box with red border: "Kritisk sti" (Critical path)
  - Gray box with gray border: "Ikke-kritisk" (Non-critical)
  - Text explanation: "ES=Tidligst start, EF=Tidligst slutt, LS=Senest start, LF=Senest slutt"

### Real-time Updates (FR-9.2)
- [ ] Diagram re-renders when new commitment added
- [ ] Diagram re-renders when commitment removed (renegotiation)
- [ ] Critical path recalculation updates node/edge colors
- [ ] Timeline updates refresh ES/EF/LS/LF values

### Data Integration
- [ ] WBS items loaded from `wbs.json` or database
- [ ] Dependencies loaded from WBS item `dependencies` array
- [ ] Timeline data (ES/EF/LS/LF) loaded from validation endpoint
- [ ] Critical path data loaded from validation endpoint

---

## 📊 DASHBOARD INTEGRATION CHECKLIST

### Tabbed Navigation (FR-9.4)
- [ ] Dashboard has 3 tabs:
  - "Oversikt" (Overview) - default view
  - "Gantt-diagram" - Gantt chart view
  - "Presedensdiagram" - Precedence diagram view
- [ ] Active tab highlighted (blue background)
- [ ] Tab switching works without page reload
- [ ] View state persists (zoom level, scroll position)

### Component Integration
- [ ] GanttChart component imported in dashboard
- [ ] PrecedenceDiagram component imported in dashboard
- [ ] State management for active tab (`useState`)
- [ ] Conditional rendering based on active tab
- [ ] Props passed correctly:
  - `wbsItems`: Array of WBS items
  - `commitments`: Array of commitments
  - `timeline`: Timeline calculation object (ES/EF/LS/LF, critical path)

### Data Flow
- [ ] Dashboard fetches WBS items on mount
- [ ] Dashboard fetches commitments for current session
- [ ] Dashboard calls validation endpoint to get timeline data
- [ ] All data passed to both visualization components
- [ ] Components re-render when data changes

---

## 🔄 VALIDATION ENDPOINT INTEGRATION

### Timeline Calculation Requirements
The visualizations depend on a validation endpoint that calculates:

- [ ] **Earliest Start (ES)** for each WBS item
- [ ] **Earliest Finish (EF)** for each WBS item
- [ ] **Latest Start (LS)** for each WBS item
- [ ] **Latest Finish (LF)** for each WBS item
- [ ] **Critical Path:** Array of WBS IDs on critical path (slack = 0)
- [ ] **Projected Completion Date:** End date of project

### Validation Endpoint Response Format
```json
{
  "valid": true,
  "earliest_start": {
    "1.3.1": "2025-02-15",
    "1.3.2": "2025-03-20",
    ...
  },
  "earliest_finish": {
    "1.3.1": "2025-03-20",
    "1.3.2": "2025-05-10",
    ...
  },
  "latest_start": {
    "1.3.1": "2025-02-15",
    "1.3.2": "2025-03-20",
    ...
  },
  "latest_finish": {
    "1.3.1": "2025-03-20",
    "1.3.2": "2025-05-10",
    ...
  },
  "critical_path": ["1.3.1", "1.3.2", "1.4.1", ...],
  "projected_completion_date": "2026-05-10",
  "meets_deadline": true
}
```

### Critical Path Algorithm (Backend)
- [ ] Forward pass calculates ES and EF
- [ ] Backward pass calculates LS and LF
- [ ] Slack = LS - ES (or LF - EF)
- [ ] Critical path = tasks with slack = 0
- [ ] Topological sort for dependency ordering
- [ ] Longest path algorithm for critical path

---

## ✅ ACCEPTANCE CRITERIA

### Visual Comparison with Designs
- [ ] Gantt chart matches `visualization-01-gantt-chart.svg`:
  - Timeline range correct
  - Color scheme matches
  - Task bars positioned correctly
  - Legend present and accurate
- [ ] Precedence diagram matches `visualization-02-precedence-diagram.svg`:
  - Node layout similar (allow for drag adjustments)
  - Color scheme matches
  - ES/EF/LS/LF values visible
  - Legend present and accurate

### Functional Testing
- [ ] **Test Case 1:** Commit 1.4.1 Råbygg → Green bar appears in Gantt chart, node updates in precedence
- [ ] **Test Case 2:** Commit all critical path tasks → Red bars/nodes highlight critical path
- [ ] **Test Case 3:** Switch between tabs → Views load correctly
- [ ] **Test Case 4:** Zoom Gantt chart → Timeline scales correctly
- [ ] **Test Case 5:** Drag precedence node → Node repositions, edges follow
- [ ] **Test Case 6:** Refresh page → Committed tasks still displayed with correct colors
- [ ] **Test Case 7:** Uncommit task (renegotiation) → Visualization updates immediately

### Performance
- [ ] Gantt chart renders in <1 second with 15 tasks
- [ ] Precedence diagram renders in <1 second with 15 nodes
- [ ] Tab switching is instant (<100ms)
- [ ] No console errors or warnings

### Responsive Design
- [ ] Gantt chart scrolls horizontally on narrow screens
- [ ] Precedence diagram fits in viewport (600px height)
- [ ] Legend remains visible at all zoom levels
- [ ] Controls accessible on mobile (if mobile support added)

---

## 📝 IMPLEMENTATION NOTES

### Library Configuration Tips

**gantt-task-react:**
- Use `ViewMode.Month` for default view (matches timeline scale)
- Set `locale="nb-NO"` for Norwegian date formatting
- Customize colors via `styles` prop on each Task object
- Enable `todayColor` for today marker
- Set `columnWidth` to control zoom level (60 is reasonable)

**ReactFlow:**
- Use `fitView` on initial render to center diagram
- Enable `draggable` nodes for user repositioning
- Use `type: 'smoothstep'` for edges to avoid collisions
- Set `animated: true` on critical path edges for emphasis
- Use `MarkerType.ArrowClosed` for arrow markers

### Common Pitfalls to Avoid
- ❌ Don't hardcode colors - calculate based on critical path data
- ❌ Don't forget to convert date strings to Date objects for gantt-task-react
- ❌ Don't skip the validation endpoint call - visualizations need ES/EF/LS/LF data
- ❌ Don't position precedence nodes manually - let ReactFlow handle layout
- ❌ Don't forget to add dependencies to package.json

---

## 🚀 IMPLEMENTATION ORDER

1. **Backend First:** Implement validation endpoint with critical path calculation (4-6 hours)
2. **Gantt Chart:** Install gantt-task-react, create component, integrate with dashboard (3-4 hours)
3. **Precedence Diagram:** Install ReactFlow, create component, integrate with dashboard (3-4 hours)
4. **Dashboard Tabs:** Add tabbed navigation (1 hour)
5. **Testing:** Verify all checklist items, compare with UX designs (1-2 hours)

**Total Estimated Time:** 12-16 hours (reduced from 20-30 hours with custom implementation)

---

## 📚 REFERENCE DOCUMENTS

- `docs/PRD.md` - FR-9.1 (Gantt Chart), FR-9.2 (Precedence Diagram)
- `docs/ux/functional_flows/visualization-01-gantt-chart.svg` - Gantt chart design
- `docs/ux/functional_flows/visualization-02-precedence-diagram.svg` - Precedence diagram design
- `docs/Precedence-And-Gantt.md` - Complete implementation guide with code examples
- `docs/VISUALIZATION_STRATEGY_COMPARISON.md` - Analysis of library vs custom approach
- `docs/MVP_COMPLETION_ROADMAP_REVISED.md` - Detailed implementation plan

---

## ✅ SIGN-OFF

Before marking visualization implementation as complete, ensure:

- [ ] All checklist items above are checked ✅
- [ ] Side-by-side comparison with UX designs confirms visual match
- [ ] All 7 acceptance test cases pass
- [ ] No console errors or TypeScript warnings
- [ ] Code reviewed by at least one team member
- [ ] PR approved and merged to main branch

**Implemented by:** _________________
**Reviewed by:** _________________
**Date:** _________________

---

**End of Checklist**
