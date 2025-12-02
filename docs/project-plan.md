# Project Plan

## Instruksjoner

1. Der hvor det står {prompt / user-input-file}, kan dere legge inn en egen prompt eller filnavn for å gi ekstra instruksjoner. Hvis dere ikke ønsker å legge til ekstra instruksjoner, kan dere bare fjerne denne delen.
2. Hvis jeg har skrevet noe der allerede, f.eks. "Root Cause Analysis and Solution Design for Player Inactivity", så kan dere bytte ut min prompt med deres egen.

## Fase 0

- [ ] /run-agent-task analyst *workflow-init
  - [ ] File: bmm-workflow-status.yaml
- [ ] Brainstorming
  - [ ] /run-agent-task analyst *brainstorm "Skriv her hva dere ønsker å brainstorme"
    - [ ] File: brainstorming-session-results-date.md
  - [ ] /run-agent-task analyst *brainstorm "Skriv her hva dere ønsker å brainstorme"
    - [ ] File: brainstorming-session-results-date.md
  - [ ] /run-agent-task analyst *brainstorm "Skriv her hva dere ønsker å brainstorme"
    - [ ] File: brainstorming-session-results-date.md
- [ ] Research
  - [ ] /run-agent-task analyst *research "Skriv her hva dere ønsker å brainstorme"
    - [ ] File: research-technical-date.md
- [ ] Product Brief
  - [ ] /run-agent-task analyst *product-brief "Read the brainstorming sessions the research session and the @proposal.md file, and create a product brief for the project."
    - [ ] File: product-brief.md

## Fase 1

- [ ] Planning
  - [ ] /run-agent-task pm *prd
    - [ ] File: PRD.md
  - [ ] /run-agent-task pm *validate-prd
    - [ ] File: validation-report-date.md
  - [ ] /run-agent-task ux-designer *create-ux-design {prompt / user-input-file}
    - [ ] File: ux-design-specification.md
    - [ ] File: ux-color-themes.html
    - [ ] File: ux-design-directions.html
  - [ ] /run-agent-task ux-designer *validate-ux-design {prompt / user-input-file}

## Fase 2

- [ ] Solutioning
  - [ ] /run-agent-task architect *create-architecture {prompt / user-input-file}
    - [ ] File: architecture.md
  - [ ] /run-agent-task pm *create-epics-and-stories {prompt / user-input-file}
    - [ ] File: epics.md
  - [ ] /run-agent-task tea *test-design {prompt / user-input-file}
  - [ ] /run-agent-task architect *solutioning-gate-check {prompt / user-input-file}

## Fase 3

- [ ] Implementation

  - [ ] /run-agent-task sm *sprint-planning {prompt / user-input-file}
    - [ ] File: sprint-artifacts/sprint-status.yaml

  - foreach epic in sprint planning:

    - [ ] /run-agent-task sm create-epic-tech-context {prompt / user-input-file}
      - [ ] File: sprint-artifacts/tech-spec-epic-{{epic_id}}.md
    - [ ] /run-agent-task sm validate-epic-tech-context {prompt / user-input-file}

    - foreach story in epic:
      - [ ] /run-agent-task sm *create-story {prompt / user-input-file}
        - [ ] File: sprint-artifacts/{{story_key}}.md
      - [ ] /run-agent-task sm *validate-create-story {prompt / user-input-file}
      - [ ] /run-agent-task sm *create-story-context {prompt / user-input-file}
        - [ ] File: sprint-artifacts/{{story_key}}.context.xml
      - [ ] /run-agent-task sm *validate-story-context {prompt / user-input-file}
      - [ ] /run-agent-task sm *story-ready-for-dev {prompt / user-input-file}
        while code-review != approved:
        - [ ] /run-agent-task dev *develop-story {prompt / user-input-file}
        - [ ] /run-agent-task dev *code-review {prompt / user-input-file}
      - [ ] /run-agent-task dev *story-done {prompt / user-input-file}
      - [ ] /run-agent-task sm *test-review {prompt / user-input-file}

    - [ ] /run-agent-task sm *epic-retrospective {prompt / user-input-file}

## BMAD workflow

<img src="images/bmad-workflow.svg" alt="BMAD workflow">
