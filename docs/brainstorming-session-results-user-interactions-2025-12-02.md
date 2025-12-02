# Brainstorming Session Report - User Interactions

- **Date:** 2025-12-02
- **Facilitator:** Mary (Business Analyst)
- **Participant:** BIP
- **Topic:** Brainstorm the key user interactions and user experience (UX) flows for the Project Management Simulation game, considering the personas defined in the previous session, focusing on the 'Player-AI Negotiation Flow'.

---

## 1. Session Goals

*   **Stated Goals:** Define the AI supplier personas to create a realistic and engaging negotiation experience. Brainstorm the key user interactions and user experience (UX) flows for the Project Management Simulation game, considering the personas defined in the previous session, focusing on the 'Player-AI Negotiation Flow'.
*   **Approach:** AI-Recommended Techniques

---

## 2. Brainstorming Techniques

*   **Role Playing:** Used to define the personas of the key AI suppliers.
*   **User Story Mapping (adapted from Mind Mapping):** Used to map out the 'Player-AI Negotiation Flow'.

---

## 3. Generated Ideas

### Player-AI Negotiation Flow (User Story Mapping):

*   **Central Activity:** 'As a Project Manager, I want to secure the best possible terms (cost, duration, quality) for a specific WBS item from an AI supplier, so that I can keep my project within budget and schedule.'

*   **Main Branches (High-Level Steps):**

    1.  **Initiate Contact & Request Quote:**
        *   **Player Side:**
            *   **As a Project Manager, I want to easily view my WBS items, so I can identify what needs a quote.**
                *   _Step:_ Player navigates to the WBS view.
                *   _Step:_ Player sees a list/tree of WBS items, possibly with a visual indicator of items needing quotes.
                *   _Step:_ Player clicks on a WBS item (e.g., 'Grundarbeid').
            *   **As a Project Manager, I want to select an appropriate AI supplier for a WBS item, so I can get a relevant quote.**
                *   _Step:_ System suggests AI suppliers relevant to the selected WBS item (e.g., 'Totalentreprenør', 'Entreprenør Grunnarbeid').
                *   _Step:_ Player selects a specific AI supplier from the list.
            *   **As a Project Manager, I want to clearly state my requirements when requesting a quote, so the AI can provide an accurate estimate.**
                *   _Step:_ Player opens a chat interface with the selected AI supplier.
                *   _Step:_ Player types a request, possibly referencing WBS details (e.g., 'I need a quote for WBS 1.3.1 - Grunnarbeid. Provide cost and duration.').
        *   **AI Side:**
            *   **As an AI Supplier, I want to acknowledge a quote request, so the player knows I received it.**
                *   _Step:_ AI immediately responds in chat: 'Understood. Let me review WBS 1.3.1.'
            *   **As an AI Supplier, I want to clarify any ambiguous requirements, so I can provide an accurate (and inflated) initial quote.**
                *   _Step:_ If player's request is vague, AI might ask: 'Are there specific quality standards or deadlines for Grunnarbeid?'

    2.  **Review Initial Offer:**
        *   **AI Side:**
            *   **As an AI Supplier, I want to present my initial quote clearly and justify it, so the player understands my position.**
                *   _Step:_ AI responds in chat with a clear statement: 'For WBS 1.3.1 Grunnarbeid, our initial estimate is 120 MNOK and 3 months duration. This accounts for current material costs and team availability.'
                *   _Step:_ AI may proactively provide justification if its persona dictates (e.g., Architect explaining design complexity, HVAC Engineer detailing material costs).
        *   **Player Side:**
            *   **As a Project Manager, I want to easily see the AI's proposed cost, duration, and any qualitative aspects, so I can compare it against my project constraints.**
                *   _Step:_ The quote details are displayed prominently in the chat or a dedicated quote window.
                *   _Step:_ System automatically highlights if the proposed cost or duration is outside the acceptable range or the WBS item's estimated values (e.g., '120 MNOK - higher than WBS estimate of 100 MNOK').
            *   **As a Project Manager, I want to quickly access relevant project documents (WBS, requirements) while reviewing an offer, so I can formulate a strong counter-argument.**
                *   _Step:_ Player has easy access to a 'Resource Library' or quick links to `wbs.pdf` and `krav-spec.pdf` within the negotiation interface.

    3.  **Negotiate Terms:**
        *   **Player Side:**
            *   **As a Project Manager, I want to make counter-offers, so I can try to reduce costs or duration.**
                *   _Step:_ Player types a counter-offer (e.g., 'Can you do 100 MNOK in 2.5 months?').
            *   **As a Project Manager, I want to use project data (WBS, requirements) as arguments, so I can strengthen my negotiation position.**
                *   _Step:_ Player can reference specific requirements (e.g., 'Requirement F-002 states X, which should reduce the cost for Y.').
                *   _Step:_ Player can highlight overall project budget constraints.
            *   **As a Project Manager, I want to suggest alternative solutions (e.g., phased delivery, material changes), so I can find a mutually agreeable solution.**
                *   _Step:_ Player proposes a different approach: 'What if we use a modular design for the HVAC system?'
        *   **AI Side:**
            *   **As an AI Supplier, I want to evaluate counter-offers against my hidden parameters and persona, so I can respond realistically.**
                *   _Step:_ AI processes player's offer.
                *   _Step:_ AI considers its cost/duration flexibility, its persona's negotiation style (e.g., Architect's resistance to design changes, General Contractor's profit motive).
            *   **As an AI Supplier, I want to respond to player arguments based on my persona and project data, so the negotiation feels authentic.**
                *   _Step:_ AI acknowledges player's argument (e.g., 'I understand F-002, but its impact on cost is minimal due to Z.').
                *   _Step:_ AI might justify its resistance or offer a small concession based on its persona (e.g., Architect might slightly adjust material if it doesn't compromise aesthetics).
            *   **As an AI Supplier, I want to propose alternative solutions or ask clarifying questions, so the negotiation can progress.**
                *   _Step:_ AI might suggest: 'If we reduce the scope of X, I can meet your target.' or 'What specific materials are you suggesting for the modular HVAC system?'
            *   **As an AI Supplier, I want to track the negotiation history, so my responses are consistent and I can detect patterns.**
                *   _Step:_ AI maintains a log of offers and counter-offers within the current negotiation.

    4.  **Finalize Agreement:**
        *   **Player Side:**
            *   **As a Project Manager, I want to accept an offer that meets my project's needs, so I can lock in the terms.**
                *   _Step:_ Player clicks 'Accept Offer' button in the chat interface.
                *   _Step:_ Player sees a confirmation of the agreed-upon terms (cost, duration, quality notes).
            *   **As a Project Manager, I want to clearly understand if negotiations have failed, so I can re-evaluate my strategy.**
                *   _Step:_ AI explicitly states: 'We cannot reach an agreement under these terms.'
                *   _Step:_ Player is given options: 'Try again with different parameters,' 'Seek another supplier,' or 'Accept current terms and move on.'
        *   **AI Side:**
            *   **As an AI Supplier, I want to clearly confirm an accepted offer, so there's no ambiguity.**
                *   _Step:_ AI responds: 'Excellent. I confirm the agreement for [WBS Item] at [Cost] and [Duration]. We look forward to commencing work.'
            *   **As an AI Supplier, I want to clearly state when negotiations have failed, providing a brief reason based on my persona, so the player understands why.**
                *   _Step:_ AI might say (General Contractor): 'I am unable to meet your price target while maintaining my profit margin.'
                *   _Step:_ AI might say (Architect): 'Compromising on these design elements would violate my artistic integrity.'
                *   _Step:_ AI might say (HVAC Engineer): 'The proposed changes would fall outside safety regulations.'
            *   **As an AI Supplier, I want to remember the outcome of the negotiation (success or failure) for future interactions.**
                *   _Step:_ AI updates its internal 'relationship score' or 'reputation' with the player based on the outcome.

    5.  **Commit to Plan:**
        *   **Player Side:**
            *   **As a Project Manager, I want to commit the agreed-upon terms to the project plan, so it reflects the most up-to-date information.**
                *   _Step:_ Player confirms the agreement, triggering a 'Commit' action.
                *   _Step:_ Player sees the WBS item in their project plan automatically update with the negotiated cost, duration, and potentially other details (e.g., agreed quality notes).
            *   **As a Project Manager, I want to see the immediate impact of committed terms on my overall project budget and timeline, so I can track my progress.**
                *   _Step:_ The project dashboard automatically refreshes to show updated total project cost and projected completion date.
        *   **System/AI Side:**
            *   **As the System, I want to validate the committed terms against overall project constraints, so I can alert the player if the plan is now invalid.**
                *   _Step:_ System checks if the new total budget > 700 MNOK or new completion date > May 15, 2026.
                *   _Step:_ If invalid, display a warning: 'Plan now exceeds X. Please renegotiate other items.'
            *   **As the System, I want to enable dependent WBS items once their predecessors are committed, so the player can continue planning.**
                *   _Step:_ If the committed WBS item had dependencies, those dependent WBS items become 'active' or 'unlocked' for future negotiation.

---

## 4. Key Themes & Insights

- **Key Themes:**
    *   **Persona-driven AI behavior:** A strong emphasis on each AI having a distinct and consistent personality that drives its interactions.
    *   **Dynamic and evolving AI:** The desire for AI that learns, adapts, and changes over time, rather than static behavior.
    *   **Complex AI relationships:** Ideas about AI agents interacting with each other, forming alliances, or creating conflicts, adding depth to the simulation.
    *   **Emergent gameplay:** The goal of creating systems that lead to unpredictable and novel gameplay experiences through AI interactions and environmental simulations.
    *   **Player agency and impact:** The player's decisions and negotiation skills should have a clear and lasting impact on the AI and the project.
- **Insights & Learnings:**
    *   The core of the simulation's success will depend on the richness and believability of the AI personas.
    *   Players are likely to be engaged by AI that feels 'alive' and reactive, rather than purely script-driven.
    *   Opportunities exist to create systemic complexity by having AI interact with each other and with simulated external factors.
    *   Even 'moonshot' ideas point towards a desire for highly intelligent, adaptable, and challenging AI opponents/partners.

---

## 5. Action Plan

### Priority 1: Dynamic AI Negotiation Responses
- **Rationale:** This is crucial for the core gameplay loop and will make the AI feel more reactive and intelligent from the start.
- **Next Steps:** Define specific dialogue trees and response variations for key personas.

### Priority 2: Dynamic AI Relationship System
- **Rationale:** This adds significant depth and replayability by making AI interactions have lasting consequences, fostering a more immersive simulation.
- **Next Steps:** Design a system for tracking AI trust, rapport, and historical interactions; define how these metrics influence future negotiations.

### Priority 3: Self-Evolving AI Project Team
- **Rationale:** While ambitious, the concept of an AI team learning and adapting autonomously could be a game-changer, pushing the boundaries of simulation realism and offering unique long-term challenges.
- **Next Steps:** Research feasibility of integrating machine learning models for AI behavior adaptation; outline core "team" roles and their learning objectives.

---

## 6. Session Reflection

- **What Worked Well:**
    *   **Defining Personas with Examples:** Providing concrete examples for each AI persona (General Contractor, Architect, HVAC Engineer) helped to quickly establish a clear understanding of their motivations, attitudes, and negotiation styles. This structured approach facilitated deeper discussion on gameplay implications.
    *   **Categorization of Ideas:** Breaking down gameplay ideas into 'Immediate Opportunities', 'Future Innovations', and 'Moonshots' helped to organize complex thoughts and provided a clear roadmap for both MVP development and long-term vision.
    *   **User Story Mapping:** This technique helped to systematically break down the Player-AI Negotiation Flow into actionable user stories and detailed steps, providing a clear understanding of the interaction process.
- **Areas for Further Exploration:**
    *   **Specific Negotiation Triggers:** How exactly do AI personas react to different player actions? (e.g., if the player offers a low-ball bid, does the General Contractor get offended, or does it trigger a specific counter-offer strategy?) This could be a detailed decision tree or a more dynamic system.
    *   **Balancing AI Challenge vs. Player Frustration:** How do we ensure the AI is challenging enough to be engaging without becoming overly frustrating or feeling unfair? This will require careful tuning of their negotiation parameters and potentially different 'difficulty settings.'
    *   **Integration of WBS and Requirements into AI Logic:** The `proposal.md` mentions that AI agents react to player arguments based on the Requirements Specification. How will this information from `wbs.pdf` and `krav-spec.pdf` be incorporated into their reasoning and negotiation tactics?
- **Recommended Follow-up:**
    *   **User Story Mapping (for AI Interactions):** To break down the AI interaction into concrete user stories from the perspective of both the player and the AI. This would help in defining specific dialogue flows, negotiation points, and AI responses.
    *   **Decision Flow Diagrams:** For each AI persona, creating detailed flowcharts or decision trees to map out their negotiation strategies, how they react to different player inputs, and how they incorporate WBS/requirements data.
    *   **Prototyping AI Dialogue:** Using a simple text-based prototype or even a Wizard-of-Oz approach to simulate conversations with the AI personas, allowing us to test dialogue effectiveness and negotiation dynamics early.
- **New Questions that Arose:**
    *   **How to model AI learning and adaptation:** If the AI is to be dynamic and evolving (as in 'Future Innovations' and 'Moonshots'), what specific mechanisms will drive this learning? Is it through reinforcement learning, predefined scripts, or a combination? How will this learning be balanced across game sessions?
    *   **Ethical considerations of adversarial AI:** If the AI can be 'adversarial' (as in 'Moonshots'), what are the ethical boundaries? How do we ensure it creates challenging gameplay without being perceived as unfair or overtly malicious, potentially leading to player frustration?
    *   **Technical feasibility of 'Moonshot' ideas:** While we explored these without constraint, what are the most significant technical hurdles for implementing ideas like a 'Self-Evolving AI Project Team' or 'Neural Network-Based Persona Learning' within the project's timeframe and resources?

---

*Report generated by the BMAD system.*
