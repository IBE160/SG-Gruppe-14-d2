# Database Implementation Guide
## PM Simulator - Nye Hædda Barneskole

**Version:** 1.0
**Date:** December 14, 2024
**Target:** Backend Developer / Database Administrator
**Database:** PostgreSQL (Supabase)

---

## Table of Contents

1. [Overview](#overview)
2. [Database Architecture](#database-architecture)
3. [Table Definitions](#table-definitions)
4. [Example Data](#example-data)
5. [Row-Level Security (RLS)](#row-level-security-rls)
6. [Triggers and Functions](#triggers-and-functions)
7. [Views](#views)
8. [Step-by-Step Implementation](#step-by-step-implementation)
9. [Testing the Database](#testing-the-database)
10. [Troubleshooting](#troubleshooting)

---

## Overview

### Purpose

This database supports a project management simulator where users (students) negotiate with AI agents to stay within budget constraints. The database tracks:

- Game sessions with 3-tier budget model
- WBS (Work Breakdown Structure) commitments
- Chat/negotiation history
- Agent timeout mechanics
- User analytics and leaderboards

### Key Concepts

**3-Tier Budget Model:**
- **Tier 1 (Tilgjengelig):** 310 MNOK available for 3 negotiable packages
- **Tier 2 (Låst):** 390 MNOK locked in 12 non-negotiable packages
- **Tier 3 (Totalt):** 700 MNOK total project budget

**Game Challenge:**
- Baseline estimates for 3 negotiable packages = 345 MNOK
- Available budget = 310 MNOK
- **Deficit = 35 MNOK** → Must negotiate savings

**Timeline Constraint:**
- Hard deadline: **May 15, 2026**
- Owner agent (Anne-Lise Berg) NEVER approves extensions

**Timeout Mechanic:**
- Agents lock after 6 disagreement rounds
- Lock duration: 10 minutes
- Auto-unlock when timer expires

---

## Database Architecture

### Entity Relationship Diagram

```
┌─────────────────┐
│   auth.users    │ (Supabase Auth - managed by Supabase)
│   (External)    │
└────────┬────────┘
         │
         │ 1:N
         ▼
┌─────────────────────────────────────────────────────────┐
│              game_sessions                               │
│ ─────────────────────────────────────────────────────── │
│ • id (PK)                                               │
│ • user_id (FK → auth.users)                            │
│ • 3-tier budget (total, locked, available, used)       │
│ • Computed budget fields (auto-calculated)              │
│ • Timeline (deadline, projected, is_valid)             │
│ • Status (in_progress, completed, abandoned)           │
└────────┬────────────────────────────────┬──────────────┘
         │                                │
         │ 1:N                            │ 1:N
         ▼                                ▼
┌──────────────────────┐      ┌──────────────────────────┐
│  wbs_commitments     │      │  negotiation_history     │
│ ──────────────────── │      │ ──────────────────────── │
│ • id (PK)            │      │ • id (PK)                │
│ • session_id (FK)    │      │ • session_id (FK)        │
│ • wbs_id (1.3.1-3)   │      │ • agent_id               │
│ • agent_id           │      │ • user_message           │
│ • Costs (baseline,   │      │ • agent_response         │
│   negotiated,        │      │ • is_disagreement        │
│   committed)         │      │ • contains_offer         │
│ • Duration           │      │ • offer_data (JSONB)     │
│ • Savings (computed) │      └──────────────────────────┘
└──────────────────────┘
         │
         │ 1:N
         ▼
┌──────────────────────┐
│   agent_timeouts     │
│ ──────────────────── │
│ • id (PK)            │
│ • session_id (FK)    │
│ • agent_id           │
│ • locked_at          │
│ • unlock_at          │
│ • agent_message      │
│ • disagreement_count │
│ • is_active          │
└──────────────────────┘

┌──────────────────────┐
│   user_analytics     │
│ ──────────────────── │
│ • id (PK)            │
│ • user_id (FK)       │
│ • total_sessions     │
│ • completed_sessions │
│ • total_budget_saved │
│ • avg_savings_%      │
│ • best_savings_%     │
└──────────────────────┘
```

---

## Table Definitions

### 1. `game_sessions`

**Purpose:** Stores each game session with budget tracking and status.

**Columns:**

| Column Name                    | Data Type                  | Constraints               | Description                                    | Example Value                |
|-------------------------------|----------------------------|---------------------------|------------------------------------------------|------------------------------|
| `id`                          | `UUID`                     | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique session identifier | `550e8400-e29b-41d4-a716-446655440000` |
| `user_id`                     | `UUID`                     | NOT NULL, FK → auth.users | User who owns this session | `7f3b8c1d-2e4a-4b5c-9d8e-1a2b3c4d5e6f` |
| `total_budget`                | `NUMERIC(12, 2)`          | NOT NULL, DEFAULT 700000000.00 | Total project budget (700 MNOK) | `700000000.00` |
| `locked_budget`               | `NUMERIC(12, 2)`          | NOT NULL, DEFAULT 390000000.00 | Locked budget (390 MNOK) | `390000000.00` |
| `available_budget`            | `NUMERIC(12, 2)`          | NOT NULL, DEFAULT 310000000.00 | Available budget (310 MNOK) | `310000000.00` |
| `current_budget_used`         | `NUMERIC(12, 2)`          | NOT NULL, DEFAULT 0.00 | Amount used from available budget | `105000000.00` (105 MNOK) |
| `budget_tier1_percentage`     | `NUMERIC(5, 2)`           | GENERATED ALWAYS AS STORED (computed) | Percentage of available used | `33.87` (33.87%) |
| `budget_tier3_total`          | `NUMERIC(12, 2)`          | GENERATED ALWAYS AS STORED (computed) | Locked + used | `495000000.00` |
| `budget_remaining`            | `NUMERIC(12, 2)`          | GENERATED ALWAYS AS STORED (computed) | Available - used | `205000000.00` |
| `deadline_date`               | `DATE`                     | NOT NULL, DEFAULT '2026-05-15' | Hard project deadline | `2026-05-15` |
| `projected_completion_date`   | `DATE`                     | NULL | Estimated completion date | `2026-04-20` or `NULL` |
| `is_timeline_valid`           | `BOOLEAN`                  | GENERATED ALWAYS AS STORED (computed) | projected <= deadline | `TRUE` or `FALSE` |
| `status`                      | `VARCHAR(20)`              | NOT NULL, DEFAULT 'in_progress' | Session status | `in_progress`, `completed`, `abandoned` |
| `negotiable_wbs_commitments`  | `JSONB`                    | DEFAULT '[]'::jsonb | Array of committed WBS summaries | `[{"wbs_id":"1.3.1","cost":95000000}]` |
| `created_at`                  | `TIMESTAMP WITH TIME ZONE` | DEFAULT NOW() | When session was created | `2024-12-14T10:30:00Z` |
| `updated_at`                  | `TIMESTAMP WITH TIME ZONE` | DEFAULT NOW() | Last update timestamp | `2024-12-14T11:45:00Z` |

**Constraints:**

```sql
CHECK (current_budget_used >= 0)
CHECK (current_budget_used <= available_budget)
CHECK ((locked_budget + current_budget_used) <= total_budget)
CHECK (status IN ('in_progress', 'completed', 'abandoned'))
```

**Indexes:**

```sql
CREATE INDEX idx_game_sessions_user_id ON game_sessions(user_id);
CREATE INDEX idx_game_sessions_status ON game_sessions(status);
CREATE INDEX idx_game_sessions_created_at ON game_sessions(created_at DESC);
```

---

### 2. `wbs_commitments`

**Purpose:** Tracks commitments to specific WBS packages (only 3 negotiable packages).

**Columns:**

| Column Name              | Data Type                  | Constraints               | Description                          | Example Value                |
|-------------------------|----------------------------|---------------------------|--------------------------------------|------------------------------|
| `id`                    | `UUID`                     | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique commitment identifier | `8a1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d` |
| `session_id`            | `UUID`                     | NOT NULL, FK → game_sessions(id) ON DELETE CASCADE | Parent session | `550e8400-e29b-41d4-a716-446655440000` |
| `wbs_id`                | `VARCHAR(50)`              | NOT NULL, CHECK IN ('1.3.1', '1.3.2', '1.4.1') | WBS package identifier | `1.3.1`, `1.3.2`, or `1.4.1` |
| `wbs_name`              | `VARCHAR(200)`             | NOT NULL | WBS package name | `Grunnarbeid`, `Fundamentering`, `Råbygg` |
| `agent_id`              | `VARCHAR(50)`              | NOT NULL | Agent responsible | `bjorn-eriksen`, `kari-andersen`, `per-johansen` |
| `baseline_cost`         | `NUMERIC(12, 2)`          | NOT NULL | Original estimate | `105000000.00` (105 MNOK) |
| `negotiated_cost`       | `NUMERIC(12, 2)`          | NOT NULL | Final negotiated amount | `95000000.00` (95 MNOK) |
| `committed_cost`        | `NUMERIC(12, 2)`          | NOT NULL | Amount user committed to | `95000000.00` |
| `savings`               | `NUMERIC(12, 2)`          | GENERATED ALWAYS AS STORED | baseline - committed | `10000000.00` (10 MNOK saved) |
| `savings_percentage`    | `NUMERIC(5, 2)`           | GENERATED ALWAYS AS STORED | (savings / baseline) * 100 | `9.52` (9.52% saved) |
| `baseline_duration`     | `NUMERIC(3, 1)`           | NOT NULL | Original duration (months) | `3.5` (3.5 months) |
| `negotiated_duration`   | `NUMERIC(3, 1)`           | NOT NULL | Final duration (months) | `3.5` |
| `quality_level`         | `VARCHAR(20)`              | NULL | Quality tier | `standard`, `budget`, `premium`, or `NULL` |
| `status`                | `VARCHAR(20)`              | NOT NULL, DEFAULT 'committed' | Commitment status | `committed`, `rejected` |
| `committed_at`          | `TIMESTAMP WITH TIME ZONE` | DEFAULT NOW() | When commitment was made | `2024-12-14T11:30:00Z` |
| `notes`                 | `TEXT`                     | NULL | Additional notes | `Negotiated lower quality materials` |

**Constraints:**

```sql
CHECK (wbs_id IN ('1.3.1', '1.3.2', '1.4.1'))
CHECK (baseline_cost > 0)
CHECK (negotiated_cost > 0)
CHECK (committed_cost > 0)
CHECK (baseline_duration > 0)
CHECK (negotiated_duration > 0)
CHECK (quality_level IN ('standard', 'budget', 'premium') OR quality_level IS NULL)
CHECK (status IN ('committed', 'rejected'))
UNIQUE (session_id, wbs_id)  -- Only one commitment per WBS per session
```

**Indexes:**

```sql
CREATE INDEX idx_wbs_commitments_session_id ON wbs_commitments(session_id);
CREATE INDEX idx_wbs_commitments_wbs_id ON wbs_commitments(wbs_id);
CREATE INDEX idx_wbs_commitments_agent_id ON wbs_commitments(agent_id);
```

---

### 3. `negotiation_history`

**Purpose:** Stores all chat messages between user and AI agents.

**Columns:**

| Column Name           | Data Type                  | Constraints               | Description                          | Example Value                |
|----------------------|----------------------------|---------------------------|--------------------------------------|------------------------------|
| `id`                 | `UUID`                     | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique message identifier | `9b2c3d4e-5f6a-7b8c-9d0e-1f2a3b4c5d6e` |
| `session_id`         | `UUID`                     | NOT NULL, FK → game_sessions(id) ON DELETE CASCADE | Parent session | `550e8400-e29b-41d4-a716-446655440000` |
| `agent_id`           | `VARCHAR(50)`              | NOT NULL | Agent identifier | `anne-lise-berg`, `bjorn-eriksen`, `kari-andersen`, `per-johansen` |
| `agent_name`         | `VARCHAR(100)`             | NOT NULL | Agent display name | `Anne-Lise Berg`, `Bjørn Eriksen`, etc. |
| `agent_type`         | `VARCHAR(20)`              | NOT NULL, CHECK IN ('owner', 'supplier') | Agent role type | `owner` or `supplier` |
| `user_message`       | `TEXT`                     | NOT NULL | User's message | `Kan du redusere prisen til 95 MNOK?` |
| `agent_response`     | `TEXT`                     | NOT NULL | Agent's response | `Ja, jeg kan godta 95 MNOK for standardkvalitet.` |
| `is_disagreement`    | `BOOLEAN`                  | DEFAULT FALSE | Flagged as disagreement | `TRUE` or `FALSE` |
| `disagreement_reason`| `TEXT`                     | NULL | Why flagged as disagreement | `Offer too far from acceptable range` |
| `contains_offer`     | `BOOLEAN`                  | DEFAULT FALSE | Response contains formal offer | `TRUE` or `FALSE` |
| `offer_data`         | `JSONB`                    | NULL | Structured offer details | `{"wbs_id":"1.3.1","cost":95000000,"duration":3.5}` |
| `context_snapshot`   | `JSONB`                    | NULL | Game state at time of message | `{"budget_used":0,"commitments":[]}` |
| `timestamp`          | `TIMESTAMP WITH TIME ZONE` | DEFAULT NOW() | Message timestamp | `2024-12-14T11:25:00Z` |

**Constraints:**

```sql
CHECK (agent_type IN ('owner', 'supplier'))
```

**Indexes:**

```sql
CREATE INDEX idx_negotiation_history_session_id ON negotiation_history(session_id);
CREATE INDEX idx_negotiation_history_agent_id ON negotiation_history(agent_id);
CREATE INDEX idx_negotiation_history_timestamp ON negotiation_history(timestamp DESC);
CREATE INDEX idx_negotiation_history_disagreement ON negotiation_history(is_disagreement) WHERE is_disagreement = TRUE;
```

---

### 4. `agent_timeouts`

**Purpose:** Tracks agent lockouts after 6 disagreement rounds.

**Columns:**

| Column Name           | Data Type                  | Constraints               | Description                          | Example Value                |
|----------------------|----------------------------|---------------------------|--------------------------------------|------------------------------|
| `id`                 | `UUID`                     | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique timeout identifier | `a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d` |
| `session_id`         | `UUID`                     | NOT NULL, FK → game_sessions(id) ON DELETE CASCADE | Parent session | `550e8400-e29b-41d4-a716-446655440000` |
| `agent_id`           | `VARCHAR(50)`              | NOT NULL | Agent being locked | `bjorn-eriksen`, `kari-andersen`, `per-johansen` |
| `locked_at`          | `TIMESTAMP WITH TIME ZONE` | NOT NULL, DEFAULT NOW() | When lock started | `2024-12-14T11:30:00Z` |
| `unlock_at`          | `TIMESTAMP WITH TIME ZONE` | NOT NULL | When lock expires | `2024-12-14T11:40:00Z` (10 min later) |
| `lock_duration_minutes` | `INTEGER`               | NOT NULL, DEFAULT 10 | Duration in minutes | `10` |
| `agent_message`      | `TEXT`                     | NOT NULL | Agent's goodbye message | `Jeg må gå til et møte. Snakkes senere.` |
| `trigger_reason`     | `VARCHAR(100)`             | NULL | Why timeout triggered | `disagreement_threshold_reached`, `too_far_apart` |
| `disagreement_count` | `INTEGER`                  | NOT NULL | Disagreements at timeout | `6` |
| `is_active`          | `BOOLEAN`                  | DEFAULT TRUE | Currently locked | `TRUE` or `FALSE` |
| `unlocked_at`        | `TIMESTAMP WITH TIME ZONE` | NULL | When actually unlocked | `2024-12-14T11:40:05Z` or `NULL` |
| `created_at`         | `TIMESTAMP WITH TIME ZONE` | DEFAULT NOW() | Record creation time | `2024-12-14T11:30:00Z` |

**Constraints:**

```sql
CHECK (lock_duration_minutes > 0)
CHECK (disagreement_count >= 0)
CHECK (unlock_at > locked_at)
```

**Indexes:**

```sql
CREATE INDEX idx_agent_timeouts_session_agent ON agent_timeouts(session_id, agent_id);
CREATE INDEX idx_agent_timeouts_active ON agent_timeouts(is_active, unlock_at) WHERE is_active = TRUE;
CREATE INDEX idx_agent_timeouts_unlock_at ON agent_timeouts(unlock_at);
```

---

### 5. `user_analytics`

**Purpose:** Aggregated statistics for leaderboards and user progress.

**Columns:**

| Column Name                  | Data Type                  | Constraints               | Description                          | Example Value                |
|-----------------------------|----------------------------|---------------------------|--------------------------------------|------------------------------|
| `id`                        | `UUID`                     | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique analytics record | `b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e` |
| `user_id`                   | `UUID`                     | NOT NULL, FK → auth.users(id), UNIQUE | User identifier | `7f3b8c1d-2e4a-4b5c-9d8e-1a2b3c4d5e6f` |
| `total_sessions`            | `INTEGER`                  | DEFAULT 0 | Total games started | `5` |
| `completed_sessions`        | `INTEGER`                  | DEFAULT 0 | Total games completed | `3` |
| `total_budget_saved`        | `NUMERIC(12, 2)`          | DEFAULT 0.00 | Total MNOK saved across all games | `50000000.00` (50 MNOK) |
| `average_savings_percentage`| `NUMERIC(5, 2)`           | DEFAULT 0.00 | Average % saved | `14.49` (14.49%) |
| `best_savings_percentage`   | `NUMERIC(5, 2)`           | DEFAULT 0.00 | Best % saved in single game | `22.86` (22.86%) |
| `created_at`                | `TIMESTAMP WITH TIME ZONE` | DEFAULT NOW() | Record creation | `2024-12-10T09:00:00Z` |
| `updated_at`                | `TIMESTAMP WITH TIME ZONE` | DEFAULT NOW() | Last update | `2024-12-14T12:00:00Z` |

**Constraints:**

```sql
CHECK (total_sessions >= 0)
CHECK (completed_sessions >= 0)
CHECK (completed_sessions <= total_sessions)
CHECK (total_budget_saved >= 0)
CHECK (average_savings_percentage >= 0)
CHECK (best_savings_percentage >= 0)
UNIQUE (user_id)  -- One analytics record per user
```

**Indexes:**

```sql
CREATE INDEX idx_user_analytics_user_id ON user_analytics(user_id);
CREATE INDEX idx_user_analytics_best_savings ON user_analytics(best_savings_percentage DESC);
CREATE INDEX idx_user_analytics_total_saved ON user_analytics(total_budget_saved DESC);
```

---

## Example Data

### Example 1: Complete Game Session

**User:** Student (user_id: `7f3b8c1d-2e4a-4b5c-9d8e-1a2b3c4d5e6f`)

#### `game_sessions` Row:

```sql
INSERT INTO game_sessions (
    id, user_id, total_budget, locked_budget, available_budget, current_budget_used,
    deadline_date, projected_completion_date, status, negotiable_wbs_commitments
) VALUES (
    '550e8400-e29b-41d4-a716-446655440000',
    '7f3b8c1d-2e4a-4b5c-9d8e-1a2b3c4d5e6f',
    700000000.00,  -- 700 MNOK total
    390000000.00,  -- 390 MNOK locked
    310000000.00,  -- 310 MNOK available
    270000000.00,  -- 270 MNOK used (saved 40 MNOK!)
    '2026-05-15',  -- Deadline
    '2026-04-25',  -- Projected completion
    'completed',
    '[
        {"wbs_id":"1.3.1","agent_id":"bjorn-eriksen","cost":95000000,"duration":3.5},
        {"wbs_id":"1.3.2","agent_id":"kari-andersen","cost":55000000,"duration":2.5},
        {"wbs_id":"1.4.1","agent_id":"per-johansen","cost":120000000,"duration":4.0}
    ]'::jsonb
);
```

**Computed Values (automatic):**
- `budget_tier1_percentage`: 87.10% (270/310 * 100)
- `budget_tier3_total`: 660 MNOK (390 + 270)
- `budget_remaining`: 40 MNOK (310 - 270)
- `is_timeline_valid`: TRUE (2026-04-25 <= 2026-05-15)

#### `wbs_commitments` Rows:

```sql
-- WBS 1.3.1: Grunnarbeid (saved 10 MNOK)
INSERT INTO wbs_commitments (
    id, session_id, wbs_id, wbs_name, agent_id,
    baseline_cost, negotiated_cost, committed_cost,
    baseline_duration, negotiated_duration, quality_level, status
) VALUES (
    '8a1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d',
    '550e8400-e29b-41d4-a716-446655440000',
    '1.3.1', 'Grunnarbeid', 'bjorn-eriksen',
    105000000.00, 95000000.00, 95000000.00,
    3.5, 3.5, 'standard', 'committed'
);

-- WBS 1.3.2: Fundamentering (saved 5 MNOK)
INSERT INTO wbs_commitments (
    id, session_id, wbs_id, wbs_name, agent_id,
    baseline_cost, negotiated_cost, committed_cost,
    baseline_duration, negotiated_duration, quality_level, status
) VALUES (
    '9b2c3d4e-5f6a-7b8c-9d0e-1f2a3b4c5d6e',
    '550e8400-e29b-41d4-a716-446655440000',
    '1.3.2', 'Fundamentering', 'kari-andersen',
    60000000.00, 55000000.00, 55000000.00,
    2.5, 2.5, 'standard', 'committed'
);

-- WBS 1.4.1: Råbygg (saved 60 MNOK - scope reduction)
INSERT INTO wbs_commitments (
    id, session_id, wbs_id, wbs_name, agent_id,
    baseline_cost, negotiated_cost, committed_cost,
    baseline_duration, negotiated_duration, quality_level, status, notes
) VALUES (
    'a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d',
    '550e8400-e29b-41d4-a716-446655440000',
    '1.4.1', 'Råbygg', 'per-johansen',
    180000000.00, 120000000.00, 120000000.00,
    4.0, 4.0, 'budget', 'committed',
    'Reduced scope - fewer interior walls'
);
```

**Computed Values (automatic):**
- WBS 1.3.1: `savings` = 10 MNOK, `savings_percentage` = 9.52%
- WBS 1.3.2: `savings` = 5 MNOK, `savings_percentage` = 8.33%
- WBS 1.4.1: `savings` = 60 MNOK, `savings_percentage` = 33.33%

#### `negotiation_history` Sample Rows:

```sql
-- Message 1: User asks Bjørn for lower price
INSERT INTO negotiation_history (
    id, session_id, agent_id, agent_name, agent_type,
    user_message, agent_response, is_disagreement, contains_offer, timestamp
) VALUES (
    'c1d2e3f4-a5b6-7c8d-9e0f-1a2b3c4d5e6f',
    '550e8400-e29b-41d4-a716-446655440000',
    'bjorn-eriksen', 'Bjørn Eriksen', 'supplier',
    'Kan du redusere prisen fra 105 MNOK til 95 MNOK?',
    'Ja, jeg kan godta 95 MNOK hvis vi holder standardkvalitet og 3.5 måneders varighet.',
    FALSE, TRUE, '2024-12-14T10:35:00Z'
);

-- Message 2: User accepts offer
INSERT INTO negotiation_history (
    id, session_id, agent_id, agent_name, agent_type,
    user_message, agent_response, is_disagreement, contains_offer,
    offer_data, timestamp
) VALUES (
    'd2e3f4a5-b6c7-8d9e-0f1a-2b3c4d5e6f7a',
    '550e8400-e29b-41d4-a716-446655440000',
    'bjorn-eriksen', 'Bjørn Eriksen', 'supplier',
    'Jeg godtar 95 MNOK for 3.5 måneder.',
    'Flott! Vi har en avtale. 95 MNOK for grunnarbeid med standardkvalitet.',
    FALSE, TRUE,
    '{"wbs_id":"1.3.1","cost":95000000,"duration":3.5,"quality":"standard"}'::jsonb,
    '2024-12-14T10:37:00Z'
);

-- Message 3: User tries to negotiate time extension with owner
INSERT INTO negotiation_history (
    id, session_id, agent_id, agent_name, agent_type,
    user_message, agent_response, is_disagreement, contains_offer, timestamp
) VALUES (
    'e3f4a5b6-c7d8-9e0f-1a2b-3c4d5e6f7a8b',
    '550e8400-e29b-41d4-a716-446655440000',
    'anne-lise-berg', 'Anne-Lise Berg', 'owner',
    'Kan vi få 2 måneder ekstra tid til å fullføre prosjektet?',
    'Dessverre, det går ikke. Fristen 15. mai 2026 er satt av skolestyret og kan ikke endres. Vi må holde oss til den.',
    TRUE,  -- Disagreement because owner NEVER extends time
    FALSE, '2024-12-14T11:00:00Z'
);
```

#### `agent_timeouts` Sample Row:

```sql
-- Kari Andersen locked after 6 disagreements
INSERT INTO agent_timeouts (
    id, session_id, agent_id, locked_at, unlock_at,
    lock_duration_minutes, agent_message, trigger_reason,
    disagreement_count, is_active
) VALUES (
    'f4a5b6c7-d8e9-0f1a-2b3c-4d5e6f7a8b9c',
    '550e8400-e29b-41d4-a716-446655440000',
    'kari-andersen',
    '2024-12-14T10:50:00Z',
    '2024-12-14T11:00:00Z',
    10,
    'Jeg må dessverre gå til et møte med teamet mitt. Jeg kontakter deg om 10 minutter.',
    'disagreement_threshold_reached',
    6,
    FALSE  -- Already unlocked
);
```

#### `user_analytics` Row:

```sql
INSERT INTO user_analytics (
    id, user_id, total_sessions, completed_sessions,
    total_budget_saved, average_savings_percentage, best_savings_percentage
) VALUES (
    'a5b6c7d8-e9f0-1a2b-3c4d-5e6f7a8b9c0d',
    '7f3b8c1d-2e4a-4b5c-9d8e-1a2b3c4d5e6f',
    3,  -- 3 games played
    2,  -- 2 completed
    100000000.00,  -- 100 MNOK saved total (this game: 75 MNOK)
    18.50,  -- Average 18.5% saved
    33.33   -- Best: 33.33% (from WBS 1.4.1 this game)
);
```

---

### Example 2: Failed Session (Over Budget)

```sql
-- Session where user exceeded budget
INSERT INTO game_sessions (
    id, user_id, total_budget, locked_budget, available_budget, current_budget_used,
    deadline_date, status
) VALUES (
    '660f9511-f3ac-52e5-b827-557766551111',
    '8g4c9d2e-3f5b-5c6d-0e9f-2b3c4d5e6f7g',
    700000000.00,
    390000000.00,
    310000000.00,
    325000000.00,  -- OVER BUDGET by 15 MNOK!
    '2026-05-15',
    'abandoned'  -- User gave up
);
```

**Computed Values:**
- `budget_tier1_percentage`: 104.84% ⚠ OVER BUDGET
- `budget_tier3_total`: 715 MNOK (exceeds total!)
- `budget_remaining`: -15 MNOK (negative!)

This would trigger validation errors preventing session completion.

---

## Row-Level Security (RLS)

### Purpose

RLS ensures users can ONLY access their own data. Critical for multi-tenant security.

### Enable RLS on All Tables

```sql
ALTER TABLE game_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE wbs_commitments ENABLE ROW LEVEL SECURITY;
ALTER TABLE negotiation_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_timeouts ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_analytics ENABLE ROW LEVEL SECURITY;
```

### Policy: `game_sessions`

**Users can only see/modify their own sessions:**

```sql
-- SELECT policy
CREATE POLICY "Users can view own game sessions"
ON game_sessions FOR SELECT
USING (auth.uid() = user_id);

-- INSERT policy
CREATE POLICY "Users can create own game sessions"
ON game_sessions FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- UPDATE policy
CREATE POLICY "Users can update own game sessions"
ON game_sessions FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- DELETE policy
CREATE POLICY "Users can delete own game sessions"
ON game_sessions FOR DELETE
USING (auth.uid() = user_id);
```

### Policy: `wbs_commitments`

**Users can only see/modify commitments for their own sessions:**

```sql
CREATE POLICY "Users can view own commitments"
ON wbs_commitments FOR SELECT
USING (
    session_id IN (
        SELECT id FROM game_sessions WHERE user_id = auth.uid()
    )
);

CREATE POLICY "Users can create commitments for own sessions"
ON wbs_commitments FOR INSERT
WITH CHECK (
    session_id IN (
        SELECT id FROM game_sessions WHERE user_id = auth.uid()
    )
);

CREATE POLICY "Users can update own commitments"
ON wbs_commitments FOR UPDATE
USING (
    session_id IN (
        SELECT id FROM game_sessions WHERE user_id = auth.uid()
    )
);

CREATE POLICY "Users can delete own commitments"
ON wbs_commitments FOR DELETE
USING (
    session_id IN (
        SELECT id FROM game_sessions WHERE user_id = auth.uid()
    )
);
```

### Policy: `negotiation_history`

```sql
CREATE POLICY "Users can view own negotiation history"
ON negotiation_history FOR SELECT
USING (
    session_id IN (
        SELECT id FROM game_sessions WHERE user_id = auth.uid()
    )
);

CREATE POLICY "Users can create negotiation messages"
ON negotiation_history FOR INSERT
WITH CHECK (
    session_id IN (
        SELECT id FROM game_sessions WHERE user_id = auth.uid()
    )
);
```

### Policy: `agent_timeouts`

```sql
CREATE POLICY "Users can view own agent timeouts"
ON agent_timeouts FOR SELECT
USING (
    session_id IN (
        SELECT id FROM game_sessions WHERE user_id = auth.uid()
    )
);

CREATE POLICY "System can create agent timeouts"
ON agent_timeouts FOR INSERT
WITH CHECK (
    session_id IN (
        SELECT id FROM game_sessions WHERE user_id = auth.uid()
    )
);
```

### Policy: `user_analytics`

```sql
CREATE POLICY "Users can view own analytics"
ON user_analytics FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can update own analytics"
ON user_analytics FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can insert own analytics"
ON user_analytics FOR INSERT
WITH CHECK (auth.uid() = user_id);
```

---

## Triggers and Functions

### 1. Auto-Update `updated_at` Timestamp

**Purpose:** Automatically update `updated_at` column on row changes.

```sql
-- Create function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to game_sessions
CREATE TRIGGER update_game_sessions_updated_at
    BEFORE UPDATE ON game_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Apply to user_analytics
CREATE TRIGGER update_user_analytics_updated_at
    BEFORE UPDATE ON user_analytics
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### 2. Auto-Unlock Expired Agent Timeouts

**Purpose:** Automatically set `is_active = FALSE` when timeout expires.

```sql
CREATE OR REPLACE FUNCTION unlock_expired_timeouts()
RETURNS void AS $$
BEGIN
    UPDATE agent_timeouts
    SET is_active = FALSE,
        unlocked_at = NOW()
    WHERE is_active = TRUE
      AND unlock_at <= NOW()
      AND unlocked_at IS NULL;
END;
$$ LANGUAGE plpgsql;

-- This function should be called periodically by backend
-- Or can be triggered via pg_cron extension if available
```

### 3. Update Session Budget on Commitment

**Purpose:** Update `current_budget_used` when new commitment is created.

```sql
CREATE OR REPLACE FUNCTION update_session_budget_on_commit()
RETURNS TRIGGER AS $$
BEGIN
    -- Add committed cost to session's current_budget_used
    UPDATE game_sessions
    SET current_budget_used = current_budget_used + NEW.committed_cost
    WHERE id = NEW.session_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_budget_on_commit
    AFTER INSERT ON wbs_commitments
    FOR EACH ROW
    EXECUTE FUNCTION update_session_budget_on_commit();
```

---

## Views

### 1. Active Sessions Summary

**Purpose:** Quick overview of all active sessions.

```sql
CREATE OR REPLACE VIEW active_sessions_summary AS
SELECT
    gs.id,
    gs.user_id,
    gs.current_budget_used,
    gs.budget_tier1_percentage,
    gs.budget_remaining,
    gs.deadline_date,
    gs.status,
    COUNT(wc.id) AS commitments_count,
    COALESCE(SUM(wc.savings), 0) AS total_savings,
    gs.created_at,
    gs.updated_at
FROM game_sessions gs
LEFT JOIN wbs_commitments wc ON gs.id = wc.session_id
WHERE gs.status = 'in_progress'
GROUP BY gs.id;
```

### 2. Leaderboard View

**Purpose:** Rankings for best performers.

```sql
CREATE OR REPLACE VIEW leaderboard AS
SELECT
    ua.user_id,
    au.email,  -- From auth.users (if accessible)
    ua.completed_sessions,
    ua.total_budget_saved,
    ua.average_savings_percentage,
    ua.best_savings_percentage,
    RANK() OVER (ORDER BY ua.best_savings_percentage DESC) AS rank_by_best_savings,
    RANK() OVER (ORDER BY ua.total_budget_saved DESC) AS rank_by_total_saved
FROM user_analytics ua
LEFT JOIN auth.users au ON ua.user_id = au.id
WHERE ua.completed_sessions > 0
ORDER BY ua.best_savings_percentage DESC;
```

---

## Step-by-Step Implementation

### Prerequisites

1. **Supabase Project Created:** You have a Supabase project URL and anon key
2. **Access to SQL Editor:** Open Supabase Dashboard → SQL Editor
3. **UUID Extension Enabled:** Supabase enables this by default

### Step 1: Create Tables

Copy and paste the complete SQL migration from `database/migrations/001_complete_schema.sql` into Supabase SQL Editor.

**Or create tables manually:**

```sql
-- 1. Create game_sessions table
CREATE TABLE public.game_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- 3-tier budget model
    total_budget NUMERIC(12, 2) NOT NULL DEFAULT 700000000.00,
    locked_budget NUMERIC(12, 2) NOT NULL DEFAULT 390000000.00,
    available_budget NUMERIC(12, 2) NOT NULL DEFAULT 310000000.00,
    current_budget_used NUMERIC(12, 2) NOT NULL DEFAULT 0.00,

    -- Computed columns
    budget_tier1_percentage NUMERIC(5, 2) GENERATED ALWAYS AS
        ((current_budget_used / available_budget) * 100) STORED,
    budget_tier3_total NUMERIC(12, 2) GENERATED ALWAYS AS
        (locked_budget + current_budget_used) STORED,
    budget_remaining NUMERIC(12, 2) GENERATED ALWAYS AS
        (available_budget - current_budget_used) STORED,

    -- Timeline
    deadline_date DATE NOT NULL DEFAULT '2026-05-15',
    projected_completion_date DATE,
    is_timeline_valid BOOLEAN GENERATED ALWAYS AS
        (projected_completion_date IS NULL OR projected_completion_date <= deadline_date) STORED,

    -- Status
    status VARCHAR(20) NOT NULL DEFAULT 'in_progress',
    negotiable_wbs_commitments JSONB DEFAULT '[]'::jsonb,

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Constraints
    CHECK (current_budget_used >= 0),
    CHECK (current_budget_used <= available_budget),
    CHECK ((locked_budget + current_budget_used) <= total_budget),
    CHECK (status IN ('in_progress', 'completed', 'abandoned'))
);

-- 2. Create wbs_commitments table
CREATE TABLE public.wbs_commitments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES public.game_sessions(id) ON DELETE CASCADE,

    wbs_id VARCHAR(50) NOT NULL,
    wbs_name VARCHAR(200) NOT NULL,
    agent_id VARCHAR(50) NOT NULL,

    baseline_cost NUMERIC(12, 2) NOT NULL,
    negotiated_cost NUMERIC(12, 2) NOT NULL,
    committed_cost NUMERIC(12, 2) NOT NULL,

    savings NUMERIC(12, 2) GENERATED ALWAYS AS (baseline_cost - committed_cost) STORED,
    savings_percentage NUMERIC(5, 2) GENERATED ALWAYS AS
        ((baseline_cost - committed_cost) / baseline_cost * 100) STORED,

    baseline_duration NUMERIC(3, 1) NOT NULL,
    negotiated_duration NUMERIC(3, 1) NOT NULL,

    quality_level VARCHAR(20),
    status VARCHAR(20) NOT NULL DEFAULT 'committed',
    committed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    notes TEXT,

    CHECK (wbs_id IN ('1.3.1', '1.3.2', '1.4.1')),
    CHECK (baseline_cost > 0),
    CHECK (negotiated_cost > 0),
    CHECK (committed_cost > 0),
    CHECK (baseline_duration > 0),
    CHECK (negotiated_duration > 0),
    CHECK (quality_level IN ('standard', 'budget', 'premium') OR quality_level IS NULL),
    CHECK (status IN ('committed', 'rejected')),
    CONSTRAINT unique_wbs_per_session UNIQUE (session_id, wbs_id)
);

-- 3. Create negotiation_history table
CREATE TABLE public.negotiation_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES public.game_sessions(id) ON DELETE CASCADE,

    agent_id VARCHAR(50) NOT NULL,
    agent_name VARCHAR(100) NOT NULL,
    agent_type VARCHAR(20) NOT NULL,

    user_message TEXT NOT NULL,
    agent_response TEXT NOT NULL,

    is_disagreement BOOLEAN DEFAULT FALSE,
    disagreement_reason TEXT,

    contains_offer BOOLEAN DEFAULT FALSE,
    offer_data JSONB,

    context_snapshot JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CHECK (agent_type IN ('owner', 'supplier'))
);

-- 4. Create agent_timeouts table
CREATE TABLE public.agent_timeouts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES public.game_sessions(id) ON DELETE CASCADE,
    agent_id VARCHAR(50) NOT NULL,

    locked_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    unlock_at TIMESTAMP WITH TIME ZONE NOT NULL,
    lock_duration_minutes INTEGER NOT NULL DEFAULT 10,

    agent_message TEXT NOT NULL,
    trigger_reason VARCHAR(100),
    disagreement_count INTEGER NOT NULL,

    is_active BOOLEAN DEFAULT TRUE,
    unlocked_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CHECK (lock_duration_minutes > 0),
    CHECK (disagreement_count >= 0),
    CHECK (unlock_at > locked_at)
);

-- 5. Create user_analytics table
CREATE TABLE public.user_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    total_sessions INTEGER DEFAULT 0,
    completed_sessions INTEGER DEFAULT 0,
    total_budget_saved NUMERIC(12, 2) DEFAULT 0.00,
    average_savings_percentage NUMERIC(5, 2) DEFAULT 0.00,
    best_savings_percentage NUMERIC(5, 2) DEFAULT 0.00,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CHECK (total_sessions >= 0),
    CHECK (completed_sessions >= 0),
    CHECK (completed_sessions <= total_sessions),
    CHECK (total_budget_saved >= 0),
    CHECK (average_savings_percentage >= 0),
    CHECK (best_savings_percentage >= 0),
    CONSTRAINT unique_user_analytics UNIQUE (user_id)
);
```

### Step 2: Create Indexes

```sql
-- game_sessions indexes
CREATE INDEX idx_game_sessions_user_id ON public.game_sessions(user_id);
CREATE INDEX idx_game_sessions_status ON public.game_sessions(status);
CREATE INDEX idx_game_sessions_created_at ON public.game_sessions(created_at DESC);

-- wbs_commitments indexes
CREATE INDEX idx_wbs_commitments_session_id ON public.wbs_commitments(session_id);
CREATE INDEX idx_wbs_commitments_wbs_id ON public.wbs_commitments(wbs_id);
CREATE INDEX idx_wbs_commitments_agent_id ON public.wbs_commitments(agent_id);

-- negotiation_history indexes
CREATE INDEX idx_negotiation_history_session_id ON public.negotiation_history(session_id);
CREATE INDEX idx_negotiation_history_agent_id ON public.negotiation_history(agent_id);
CREATE INDEX idx_negotiation_history_timestamp ON public.negotiation_history(timestamp DESC);
CREATE INDEX idx_negotiation_history_disagreement ON public.negotiation_history(is_disagreement)
    WHERE is_disagreement = TRUE;

-- agent_timeouts indexes
CREATE INDEX idx_agent_timeouts_session_agent ON public.agent_timeouts(session_id, agent_id);
CREATE INDEX idx_agent_timeouts_active ON public.agent_timeouts(is_active, unlock_at)
    WHERE is_active = TRUE;
CREATE INDEX idx_agent_timeouts_unlock_at ON public.agent_timeouts(unlock_at);

-- user_analytics indexes
CREATE INDEX idx_user_analytics_user_id ON public.user_analytics(user_id);
CREATE INDEX idx_user_analytics_best_savings ON public.user_analytics(best_savings_percentage DESC);
CREATE INDEX idx_user_analytics_total_saved ON public.user_analytics(total_budget_saved DESC);
```

### Step 3: Enable RLS

```sql
-- Enable RLS on all tables
ALTER TABLE public.game_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.wbs_commitments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.negotiation_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_timeouts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_analytics ENABLE ROW LEVEL SECURITY;
```

### Step 4: Create RLS Policies

```sql
-- game_sessions policies
CREATE POLICY "Users can view own game sessions"
ON public.game_sessions FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can create own game sessions"
ON public.game_sessions FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own game sessions"
ON public.game_sessions FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own game sessions"
ON public.game_sessions FOR DELETE
USING (auth.uid() = user_id);

-- wbs_commitments policies
CREATE POLICY "Users can view own commitments"
ON public.wbs_commitments FOR SELECT
USING (session_id IN (SELECT id FROM public.game_sessions WHERE user_id = auth.uid()));

CREATE POLICY "Users can create commitments for own sessions"
ON public.wbs_commitments FOR INSERT
WITH CHECK (session_id IN (SELECT id FROM public.game_sessions WHERE user_id = auth.uid()));

CREATE POLICY "Users can update own commitments"
ON public.wbs_commitments FOR UPDATE
USING (session_id IN (SELECT id FROM public.game_sessions WHERE user_id = auth.uid()));

CREATE POLICY "Users can delete own commitments"
ON public.wbs_commitments FOR DELETE
USING (session_id IN (SELECT id FROM public.game_sessions WHERE user_id = auth.uid()));

-- negotiation_history policies
CREATE POLICY "Users can view own negotiation history"
ON public.negotiation_history FOR SELECT
USING (session_id IN (SELECT id FROM public.game_sessions WHERE user_id = auth.uid()));

CREATE POLICY "Users can create negotiation messages"
ON public.negotiation_history FOR INSERT
WITH CHECK (session_id IN (SELECT id FROM public.game_sessions WHERE user_id = auth.uid()));

-- agent_timeouts policies
CREATE POLICY "Users can view own agent timeouts"
ON public.agent_timeouts FOR SELECT
USING (session_id IN (SELECT id FROM public.game_sessions WHERE user_id = auth.uid()));

CREATE POLICY "System can create agent timeouts"
ON public.agent_timeouts FOR INSERT
WITH CHECK (session_id IN (SELECT id FROM public.game_sessions WHERE user_id = auth.uid()));

-- user_analytics policies
CREATE POLICY "Users can view own analytics"
ON public.user_analytics FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can update own analytics"
ON public.user_analytics FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can insert own analytics"
ON public.user_analytics FOR INSERT
WITH CHECK (auth.uid() = user_id);
```

### Step 5: Create Triggers

```sql
-- Auto-update updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_game_sessions_updated_at
    BEFORE UPDATE ON public.game_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_analytics_updated_at
    BEFORE UPDATE ON public.user_analytics
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Update session budget on commitment
CREATE OR REPLACE FUNCTION update_session_budget_on_commit()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE public.game_sessions
    SET current_budget_used = current_budget_used + NEW.committed_cost
    WHERE id = NEW.session_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_budget_on_commit
    AFTER INSERT ON public.wbs_commitments
    FOR EACH ROW
    EXECUTE FUNCTION update_session_budget_on_commit();
```

### Step 6: Create Views

```sql
-- Active sessions summary
CREATE OR REPLACE VIEW active_sessions_summary AS
SELECT
    gs.id,
    gs.user_id,
    gs.current_budget_used,
    gs.budget_tier1_percentage,
    gs.budget_remaining,
    gs.deadline_date,
    gs.status,
    COUNT(wc.id) AS commitments_count,
    COALESCE(SUM(wc.savings), 0) AS total_savings,
    gs.created_at,
    gs.updated_at
FROM public.game_sessions gs
LEFT JOIN public.wbs_commitments wc ON gs.id = wc.session_id
WHERE gs.status = 'in_progress'
GROUP BY gs.id;

-- Leaderboard
CREATE OR REPLACE VIEW leaderboard AS
SELECT
    ua.user_id,
    ua.completed_sessions,
    ua.total_budget_saved,
    ua.average_savings_percentage,
    ua.best_savings_percentage,
    RANK() OVER (ORDER BY ua.best_savings_percentage DESC) AS rank_by_best_savings,
    RANK() OVER (ORDER BY ua.total_budget_saved DESC) AS rank_by_total_saved
FROM public.user_analytics ua
WHERE ua.completed_sessions > 0
ORDER BY ua.best_savings_percentage DESC;
```

### Step 7: Verify Installation

```sql
-- Check all tables exist
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN (
    'game_sessions',
    'wbs_commitments',
    'negotiation_history',
    'agent_timeouts',
    'user_analytics'
  )
ORDER BY table_name;

-- Should return 5 rows

-- Check RLS is enabled
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
  AND tablename IN (
    'game_sessions',
    'wbs_commitments',
    'negotiation_history',
    'agent_timeouts',
    'user_analytics'
  );

-- rowsecurity should be TRUE for all
```

---

## Testing the Database

### Test 1: Create a Test Session

```sql
-- Assuming you have a user ID from auth.users
-- Replace 'YOUR_USER_ID_HERE' with actual UUID

INSERT INTO public.game_sessions (
    user_id,
    total_budget,
    locked_budget,
    available_budget,
    current_budget_used
) VALUES (
    'YOUR_USER_ID_HERE',
    700000000.00,
    390000000.00,
    310000000.00,
    0.00
);

-- Verify computed columns
SELECT
    id,
    current_budget_used,
    budget_tier1_percentage,  -- Should be 0.00
    budget_tier3_total,       -- Should be 390000000.00
    budget_remaining          -- Should be 310000000.00
FROM public.game_sessions
WHERE user_id = 'YOUR_USER_ID_HERE'
ORDER BY created_at DESC
LIMIT 1;
```

### Test 2: Create a Commitment

```sql
-- Get session_id from previous test
INSERT INTO public.wbs_commitments (
    session_id,
    wbs_id,
    wbs_name,
    agent_id,
    baseline_cost,
    negotiated_cost,
    committed_cost,
    baseline_duration,
    negotiated_duration,
    quality_level
) VALUES (
    'SESSION_ID_FROM_TEST_1',
    '1.3.1',
    'Grunnarbeid',
    'bjorn-eriksen',
    105000000.00,
    95000000.00,
    95000000.00,
    3.5,
    3.5,
    'standard'
);

-- Verify:
-- 1. Commitment created with computed savings
SELECT
    wbs_id,
    committed_cost,
    savings,              -- Should be 10000000.00
    savings_percentage    -- Should be 9.52
FROM public.wbs_commitments
WHERE session_id = 'SESSION_ID_FROM_TEST_1';

-- 2. Session budget updated automatically (via trigger)
SELECT
    current_budget_used,  -- Should be 95000000.00
    budget_tier1_percentage,  -- Should be ~30.65
    budget_remaining      -- Should be 215000000.00
FROM public.game_sessions
WHERE id = 'SESSION_ID_FROM_TEST_1';
```

### Test 3: Test Budget Constraint

```sql
-- Try to exceed budget (should FAIL)
UPDATE public.game_sessions
SET current_budget_used = 350000000.00  -- Exceeds 310 MNOK available
WHERE id = 'SESSION_ID_FROM_TEST_1';

-- Should get error: new row violates check constraint "game_sessions_current_budget_used_check"
```

### Test 4: Test RLS Policies

```sql
-- Try to access another user's session (should return 0 rows)
SELECT * FROM public.game_sessions
WHERE user_id != auth.uid();

-- Should return 0 rows due to RLS
```

---

## Troubleshooting

### Issue: Computed columns not calculating

**Solution:** Ensure GENERATED ALWAYS AS ... STORED syntax is correct.

```sql
-- Check column definition
SELECT column_name, is_generated, generation_expression
FROM information_schema.columns
WHERE table_name = 'game_sessions'
  AND column_name = 'budget_tier1_percentage';

-- Should show is_generated = 'ALWAYS'
```

### Issue: RLS blocking all access

**Solution:** Verify auth.uid() returns correct user ID.

```sql
-- Check current user
SELECT auth.uid();

-- Temporarily disable RLS for testing (NOT in production!)
ALTER TABLE public.game_sessions DISABLE ROW LEVEL SECURITY;

-- Re-enable after testing
ALTER TABLE public.game_sessions ENABLE ROW LEVEL SECURITY;
```

### Issue: Trigger not firing

**Solution:** Check trigger exists and is enabled.

```sql
-- List all triggers
SELECT
    trigger_name,
    event_manipulation,
    event_object_table,
    action_statement
FROM information_schema.triggers
WHERE event_object_schema = 'public'
  AND event_object_table IN ('game_sessions', 'wbs_commitments');

-- Should show triggers listed
```

### Issue: Foreign key constraint violation

**Solution:** Ensure parent record exists before inserting child.

```sql
-- Check session exists before creating commitment
SELECT id FROM public.game_sessions WHERE id = 'YOUR_SESSION_ID';

-- If no result, create session first
```

---

## Appendix: Quick Reference

### WBS Package IDs

| WBS ID  | Name            | Agent           | Baseline Cost | Baseline Duration |
|---------|-----------------|-----------------|---------------|-------------------|
| `1.3.1` | Grunnarbeid     | bjorn-eriksen   | 105 MNOK      | 3.5 months        |
| `1.3.2` | Fundamentering  | kari-andersen   | 60 MNOK       | 2.5 months        |
| `1.4.1` | Råbygg          | per-johansen    | 180 MNOK      | 4.0 months        |

### Agent IDs

| Agent ID          | Name              | Type      | Role                              |
|-------------------|-------------------|-----------|-----------------------------------|
| `anne-lise-berg`  | Anne-Lise Berg    | owner     | Municipality Owner (can increase budget/reduce scope, NEVER extend time) |
| `bjorn-eriksen`   | Bjørn Eriksen     | supplier  | Supplier 1: Site Preparation (WBS 1.3.1) |
| `kari-andersen`   | Kari Andersen     | supplier  | Supplier 2: Foundation (WBS 1.3.2) |
| `per-johansen`    | Per Johansen      | supplier  | Supplier 3: Structural Work (WBS 1.4.1) |

### Budget Constants

| Constant          | Value (MNOK) | Value (NOK)       |
|-------------------|--------------|-------------------|
| Total Budget      | 700          | 700,000,000.00    |
| Locked Budget     | 390          | 390,000,000.00    |
| Available Budget  | 310          | 310,000,000.00    |
| Baseline Total    | 345          | 345,000,000.00    |
| **Deficit**       | **35**       | **35,000,000.00** |

---

**End of Database Implementation Guide**

For questions or issues, contact: Backend Development Team
