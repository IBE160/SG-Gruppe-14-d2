# RLS Testing Guide
## Verifisering av Row Level Security Policies

**Dato:** 15. desember 2025
**Formål:** Teste at RLS policies beskytter brukerdata korrekt
**Forutsetning:** Database-migrasjonen er kjørt i Supabase

---

## 📋 Innholdsfortegnelse

1. [Forberedelser](#forberedelser)
2. [Test 1: Isolasjon mellom brukere](#test-1-isolasjon-mellom-brukere)
3. [Test 2: JWT token validering](#test-2-jwt-token-validering)
4. [Test 3: Backend anon key fungerer](#test-3-backend-anon-key-fungerer)
5. [Test 4: Cascade security](#test-4-cascade-security)
6. [Test 5: Negative tester (skal feile)](#test-5-negative-tester-skal-feile)
7. [Automatiserte tester](#automatiserte-tester)

---

## Forberedelser

### Steg 1: Opprett to testbrukere

**I frontend eller Supabase Dashboard:**

```
Bruker A:
Email: testuser.a@example.com
Password: TestPassword123!

Bruker B:
Email: testuser.b@example.com
Password: TestPassword123!
```

### Steg 2: Logg inn som Bruker A og opprett data

**Via frontend eller backend API:**

1. Logg inn som Bruker A
2. Opprett en game_session
3. Legg til noen wbs_commitments
4. Send noen chat-meldinger (negotiation_history)

**Forventet resultat:**
- `game_sessions`: 1 rad med `user_id` = Bruker A's UUID
- `wbs_commitments`: Flere rader knyttet til Bruker A's session
- `negotiation_history`: Chat-meldinger for Bruker A's session

### Steg 3: Logg inn som Bruker B og opprett data

**Gjenta samme prosess:**

1. Logg inn som Bruker B
2. Opprett en game_session (annen enn Bruker A)
3. Legg til wbs_commitments
4. Send chat-meldinger

**Nå har du:**
- 2 uavhengige brukere med egne sessions
- Testdata i alle 4 tabeller

---

## Test 1: Isolasjon mellom brukere

**Mål:** Verifisere at Bruker A ikke kan se Bruker B's data

### Test 1.1: Supabase SQL Editor (simulerer anon key)

**Gå til Supabase Dashboard → SQL Editor**

```sql
-- Set auth context til Bruker A (hent UUID fra auth.users tabellen)
SET request.jwt.claims = '{"sub": "BRUKER_A_UUID_HER"}';

-- Prøv å lese alle sessions
SELECT * FROM game_sessions;
```

**✅ Forventet resultat:**
- Returnerer **KUN** Bruker A's session(s)
- Bruker B's sessions er **IKKE synlige**

```sql
-- Prøv å lese alle commitments
SELECT * FROM wbs_commitments;
```

**✅ Forventet resultat:**
- Returnerer **KUN** commitments knyttet til Bruker A's sessions
- Ingen data fra Bruker B

```sql
-- Prøv å lese chat-historikk
SELECT * FROM negotiation_history ORDER BY timestamp DESC;
```

**✅ Forventet resultat:**
- Returnerer **KUN** Bruker A's chat-meldinger
- Bruker B's forhandlinger er **IKKE synlige**

### Test 1.2: Bytt til Bruker B context

```sql
-- Set auth context til Bruker B
SET request.jwt.claims = '{"sub": "BRUKER_B_UUID_HER"}';

-- Samme queries som over
SELECT * FROM game_sessions;
SELECT * FROM wbs_commitments;
SELECT * FROM negotiation_history;
```

**✅ Forventet resultat:**
- Returnerer **KUN** Bruker B's data
- Bruker A's data er **IKKE synlige**

---

## Test 2: JWT Token Validering

**Mål:** Verifisere at uten gyldig JWT, får man ingen data

### Test 2.1: Ingen auth context

```sql
-- Reset auth context (simulerer uautorisert tilgang)
RESET request.jwt.claims;

-- Prøv å lese data
SELECT * FROM game_sessions;
```

**✅ Forventet resultat:**
- Returnerer **0 rader** (eller feilmelding)
- RLS blokkerer all tilgang uten gyldig `auth.uid()`

---

## Test 3: Backend Anon Key Fungerer

**Mål:** Bekrefte at backend med anon key kan lese/skrive data korrekt

### Test 3.1: Backend API test med Bruker A token

**Terminal 1 - Start backend:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Test med curl:**

```bash
# 1. Logg inn og få JWT token (via frontend eller Supabase auth)
# Anta at du har token lagret i variabel:
export TOKEN_A="eyJhbGc..."  # Bruker A's JWT

# 2. Test GET /api/sessions (hent alle sessions for innlogget bruker)
curl -X GET http://localhost:8000/api/sessions \
  -H "Authorization: Bearer $TOKEN_A" \
  -H "Content-Type: application/json"
```

**✅ Forventet resultat:**
```json
[
  {
    "id": "...",
    "user_id": "BRUKER_A_UUID",
    "session_name": "Min første session",
    "status": "in_progress",
    ...
  }
]
```
- Returnerer **KUN** Bruker A's sessions
- Ingen data fra Bruker B (selv om backend bruker anon key!)

### Test 3.2: Backend med Bruker B token

```bash
export TOKEN_B="eyJhbGc..."  # Bruker B's JWT

curl -X GET http://localhost:8000/api/sessions \
  -H "Authorization: Bearer $TOKEN_B" \
  -H "Content-Type: application/json"
```

**✅ Forventet resultat:**
- Returnerer **KUN** Bruker B's sessions
- Bruker A's data er **IKKE synlig**

---

## Test 4: Cascade Security

**Mål:** Verifisere at sekundære tabeller (commitments, history) arver sikkerhet fra game_sessions

### Test 4.1: Prøv å lese commitments uten å eie session

```sql
-- Som Bruker A, prøv å lese commitment ved å gjette session_id fra Bruker B
SET request.jwt.claims = '{"sub": "BRUKER_A_UUID"}';

-- Hent Bruker B's session_id først (som admin):
-- Anta session_id = '12345678-...'

-- Prøv å lese Bruker B's commitments
SELECT * FROM wbs_commitments
WHERE session_id = '12345678-1234-1234-1234-123456789012';  -- Bruker B's session
```

**✅ Forventet resultat:**
- Returnerer **0 rader**
- RLS blokkerer fordi EXISTS-check feiler (session tilhører ikke Bruker A)

### Test 4.2: Prøv å inserere commitment i andres session

```sql
-- Som Bruker A, prøv å legge til commitment i Bruker B's session
INSERT INTO wbs_commitments (
    session_id,
    wbs_id,
    wbs_name,
    agent_id,
    agent_name,
    initial_price,
    negotiated_price,
    committed_price
) VALUES (
    '12345678-1234-1234-1234-123456789012',  -- Bruker B's session!
    'WBS-001',
    'Test WBS',
    'agent-1',
    'Test Agent',
    100.00,
    90.00,
    85.00
);
```

**✅ Forventet resultat:**
- **SQL ERROR** - Policy violation
- Feilmelding: `"new row violates row-level security policy"`
- Commitment blir **IKKE opprettet**

---

## Test 5: Negative Tester (Skal Feile)

**Mål:** Bekrefte at uautoriserte handlinger blir blokkert

### Test 5.1: UPDATE andres session

```sql
SET request.jwt.claims = '{"sub": "BRUKER_A_UUID"}';

-- Prøv å oppdatere Bruker B's session
UPDATE game_sessions
SET status = 'completed'
WHERE user_id = 'BRUKER_B_UUID';
```

**✅ Forventet resultat:**
- **0 rows updated**
- RLS blokkerer oppdatering av sessions som ikke tilhører Bruker A

### Test 5.2: DELETE andres data

```sql
-- Prøv å slette Bruker B's commitments
DELETE FROM wbs_commitments
WHERE session_id IN (
    SELECT id FROM game_sessions WHERE user_id = 'BRUKER_B_UUID'
);
```

**✅ Forventet resultat:**
- **0 rows deleted**
- RLS blokkerer sletting av data som ikke tilhører Bruker A

### Test 5.3: Uten JWT token (frontend uten innlogging)

**Test i frontend - åpne browser console:**

```javascript
// Prøv å kalle Supabase direkte uten å være innlogget
const { data, error } = await supabase
  .from('game_sessions')
  .select('*');

console.log('Data:', data);
console.log('Error:', error);
```

**✅ Forventet resultat:**
```
Data: []
Error: null (men data er tom array fordi ingen auth.uid())
```

---

## Test 6: Service Role Key Bypass (Kun for Testing)

**⚠️ ADVARSEL:** Denne testen krever service_role key. Gjør ALDRI dette i frontend!

### Test 6.1: Verifiser at service_role key omgår RLS

**I Supabase SQL Editor med service_role:**

```sql
-- Ikke bruk SET request.jwt.claims
-- Service role omgår RLS automatisk

SELECT * FROM game_sessions;
```

**✅ Forventet resultat:**
- Returnerer **ALLE** sessions fra **ALLE** brukere
- Viser at RLS kan omgås med service_role (derfor må den holdes hemmelig!)

**Konklusjon:** Bekrefter at anon key MÅ ha RLS, mens service_role ikke trenger det.

---

## Automatiserte Tester

### Python Test Script (backend/tests/test_rls.py)

```python
import pytest
from supabase import create_client
import os

# Setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

@pytest.fixture
def user_a_client():
    """Supabase client med Bruker A's JWT"""
    client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    # Autentiser som Bruker A
    client.auth.sign_in_with_password({
        "email": "testuser.a@example.com",
        "password": "TestPassword123!"
    })
    return client

@pytest.fixture
def user_b_client():
    """Supabase client med Bruker B's JWT"""
    client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    # Autentiser som Bruker B
    client.auth.sign_in_with_password({
        "email": "testuser.b@example.com",
        "password": "TestPassword123!"
    })
    return client

def test_user_isolation(user_a_client, user_b_client):
    """Test at Bruker A ikke ser Bruker B's sessions"""

    # Bruker A oppretter session
    session_a = user_a_client.table('game_sessions').insert({
        "session_name": "Bruker A Session",
        "status": "in_progress"
    }).execute()

    # Bruker B oppretter session
    session_b = user_b_client.table('game_sessions').insert({
        "session_name": "Bruker B Session",
        "status": "in_progress"
    }).execute()

    # Bruker A henter sine sessions
    result_a = user_a_client.table('game_sessions').select('*').execute()

    # Assertions
    assert len(result_a.data) == 1  # Kun 1 session
    assert result_a.data[0]['session_name'] == "Bruker A Session"

    # Verifiser at Bruker B's session IKKE er synlig
    session_ids_a = [s['id'] for s in result_a.data]
    assert session_b.data[0]['id'] not in session_ids_a

def test_cascade_security(user_a_client, user_b_client):
    """Test at commitments arver sikkerhet fra sessions"""

    # Bruker B oppretter session og commitment
    session_b = user_b_client.table('game_sessions').insert({
        "session_name": "B Session"
    }).execute()

    commitment_b = user_b_client.table('wbs_commitments').insert({
        "session_id": session_b.data[0]['id'],
        "wbs_id": "WBS-001",
        "wbs_name": "Test",
        "agent_id": "agent-1",
        "agent_name": "Agent 1",
        "initial_price": 100.00,
        "negotiated_price": 90.00,
        "committed_price": 85.00
    }).execute()

    # Bruker A prøver å lese Bruker B's commitments
    result_a = user_a_client.table('wbs_commitments') \
        .select('*') \
        .eq('session_id', session_b.data[0]['id']) \
        .execute()

    # Assertion: Bruker A skal IKKE se Bruker B's commitment
    assert len(result_a.data) == 0

def test_unauthorized_update(user_a_client, user_b_client):
    """Test at Bruker A ikke kan oppdatere Bruker B's data"""

    # Bruker B oppretter session
    session_b = user_b_client.table('game_sessions').insert({
        "session_name": "B Session",
        "status": "in_progress"
    }).execute()

    session_b_id = session_b.data[0]['id']

    # Bruker A prøver å oppdatere Bruker B's session
    result = user_a_client.table('game_sessions') \
        .update({"status": "completed"}) \
        .eq('id', session_b_id) \
        .execute()

    # Assertion: Ingen rader oppdatert
    assert len(result.data) == 0

    # Verifiser at status IKKE ble endret
    check = user_b_client.table('game_sessions') \
        .select('status') \
        .eq('id', session_b_id) \
        .single() \
        .execute()

    assert check.data['status'] == 'in_progress'  # Uendret

# Kjør tester
# pytest backend/tests/test_rls.py -v
```

---

## Kjøre Testene

### Manuell Testing Checklist

- [ ] Test 1.1: Bruker A ser kun egen data ✅
- [ ] Test 1.2: Bruker B ser kun egen data ✅
- [ ] Test 2.1: Ingen auth = ingen data ✅
- [ ] Test 3.1: Backend med Bruker A token fungerer ✅
- [ ] Test 3.2: Backend med Bruker B token fungerer ✅
- [ ] Test 4.1: Kan ikke lese andres commitments ✅
- [ ] Test 4.2: Kan ikke inserere i andres session ✅
- [ ] Test 5.1: UPDATE andres session feiler ✅
- [ ] Test 5.2: DELETE andres data feiler ✅
- [ ] Test 5.3: Frontend uten innlogging = ingen data ✅

### Automatiske Tester

```bash
# Installer pytest
pip install pytest pytest-asyncio

# Kjør RLS-tester
pytest backend/tests/test_rls.py -v

# Kjør alle tester med coverage
pytest backend/tests/ --cov=backend --cov-report=html
```

---

## Troubleshooting

### Problem: RLS blokkerer alt (også egen data)

**Løsning:**
```sql
-- Sjekk at auth.uid() gir riktig UUID
SELECT auth.uid();

-- Hvis NULL, sjekk at JWT er gyldig
-- Sjekk at request.jwt.claims er satt riktig
```

### Problem: Ser andres data

**Løsning:**
```sql
-- Sjekk at RLS er aktivert
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public';
-- rowsecurity skal være TRUE

-- Sjekk policies
SELECT * FROM pg_policies WHERE schemaname = 'public';
```

### Problem: Service role key omgår RLS (som forventet)

**Dette er KORREKT oppførsel!**
- Service role key skal omgå RLS
- Bruk KUN i backend
- Bruk anon key for normale bruker-operasjoner

---

## Konklusjon

Når alle tester passerer, har dere verifisert at:

✅ **RLS policies fungerer korrekt**
✅ **Anon key er trygt å bruke**
✅ **Brukere er isolert fra hverandre**
✅ **Cascade security beskytter relaterte tabeller**
✅ **Uautoriserte handlinger blokkeres**

**Dere kan trygt deploye til produksjon med anon key i backend!** 🎉
