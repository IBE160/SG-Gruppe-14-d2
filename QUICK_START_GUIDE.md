# 🚀 Quick Start Guide - Get Your POC Running

**Status:** Backend Complete ✅ | Next: Database + Testing

---

## ⚡ 3-Step Quick Start (15 minutes)

### Step 1: Import Database (2 minutes) 🔴 REQUIRED

1. Open Supabase Dashboard: https://supabase.com/dashboard
2. Select your project
3. Go to **SQL Editor** → **New query**
4. Open file: `database/migrations/001_complete_schema.sql`
5. Copy ALL contents (`Ctrl+A`, `Ctrl+C`)
6. Paste into Supabase SQL Editor (`Ctrl+V`)
7. Click **Run** button (or `Ctrl+Enter`)
8. Wait 5-10 seconds
9. ✅ Done! (5 tables created)

**Verify:**
```sql
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN ('game_sessions', 'wbs_commitments', 'negotiation_history', 'agent_timeouts', 'user_analytics');
```
Expected: 5 rows

---

### Step 2: Add Gemini API Key (1 minute) 🔴 REQUIRED

1. Get API key from: https://aistudio.google.com/apikey
2. Open: `backend/.env.local`
3. Add these lines:
   ```env
   GEMINI_API_KEY=your-actual-key-here
   GEMINI_MODEL=gemini-1.5-pro
   ```
4. Save file
5. ✅ Done!

---

### Step 3: Test Backend (10 minutes) 🧪

#### Start Backend Server
```bash
cd backend
uvicorn main:app --reload
```

**Expected:** Server running on http://localhost:8000

#### Open API Documentation
Visit: http://localhost:8000/docs

You'll see:
- 6 new endpoints (chat, sessions, commitments)
- Interactive testing interface

#### Quick Test
1. Go to frontend: http://localhost:3000
2. Login with test user
3. Go to chat page: http://localhost:3000/chat
4. Send message to any agent
5. **Expected:** You get a REAL Norwegian AI response (not fake!)

---

## ✅ What You Should See Working

After completing steps 1-3:

✅ **Backend:**
- API server starts without errors
- 6 endpoints available at `/api/...`
- Agent prompts loaded (4 agents)
- Gemini AI connected

✅ **Database:**
- 5 tables created
- RLS policies active
- Computed columns working

✅ **Minimal Test:**
- Can chat with Anne-Lise Berg
- She responds in Norwegian
- She REJECTS time extensions (as expected)

---

## 📊 Available Endpoints

| Endpoint | What It Does |
|----------|-------------|
| `POST /api/chat` | Chat with AI agents (Norwegian responses) |
| `POST /api/sessions` | Create new game session |
| `GET /api/sessions/{id}` | Get session data |
| `PUT /api/sessions/{id}` | Update session |
| `POST /api/sessions/{id}/commitments` | Accept offer (create commitment) |
| `GET /api/sessions/{id}/commitments` | Get all commitments |

---

## 🧪 Manual Test (Optional - 5 minutes)

**Test chat endpoint with curl:**

1. Get JWT token:
   - Login at http://localhost:3000
   - Open DevTools → Application → Local Storage
   - Copy `sb-<project>-auth-token` value

2. Test Anne-Lise (Owner):
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "session_id": "test-123",
    "agent_id": "anne-lise-berg",
    "message": "Kan vi få 2 måneder ekstra tid?",
    "conversation_history": []
  }'
```

**Expected Response:**
- Norwegian text
- Anne-Lise says NO to time extension
- `"is_disagreement": true`

---

## 🔴 Troubleshooting

### Error: "Could not load agent prompts"
**Fix:** Check that `docs/AI_AGENT_SYSTEM_PROMPTS.md` exists

### Error: "GEMINI_API_KEY not found"
**Fix:** Check `backend/.env.local` has the key

### Error: "relation 'game_sessions' does not exist"
**Fix:** Run Step 1 (import database schema)

### Error: "Invalid token"
**Fix:** Login again at http://localhost:3000

---

## 📚 Detailed Documentation

For more details, see:
- `docs/BACKEND_API_COMPLETED.md` - Full backend API documentation
- `docs/DATABASE_IMPLEMENTATION_GUIDE.md` - Database reference
- `database/IMPORT_TO_SUPABASE.md` - Database import guide

---

## 🎯 Next Steps (After Testing)

Once backend is working:

1. **Update frontend** to use real API (instead of fake responses)
2. **Create main game page** with split layout (chat + dashboard)
3. **End-to-end testing**
4. **Deploy** 🚀

---

**Total Time to Working POC:** ~15 minutes

**Questions?** Check the documentation files in `docs/` folder.
