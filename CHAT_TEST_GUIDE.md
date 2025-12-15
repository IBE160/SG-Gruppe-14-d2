# Chat Testing Guide

## Step-by-Step Testing Instructions

### Step 1: Confirm Test User Email ✉️

**Why needed:** Supabase requires email confirmation before users can log in.

**Instructions:**

1. **Open Supabase Dashboard**
   - Go to: https://supabase.com/dashboard
   - Log in with your Supabase account (NOT the test user)

2. **Navigate to Users**
   - Click on your project: `cmntglldaqrekloixxoc`
   - Left sidebar → **Authentication** → **Users**

3. **Find Test User**
   - Look for: `testuser@gmail.com`
   - User ID: `a39c315d-1a58-4b01-ab16-4808acce90d0`

4. **Check Status**
   - If status shows "Waiting for verification" or similar:
     - Click on the user row
     - Click the **"Confirm email"** button
     - Status should change to "Confirmed"

   - If status already shows "Confirmed":
     - ✅ Ready to test! Skip to Step 2

**Alternative: Disable Email Confirmation (Development Only)**
1. Supabase Dashboard → Authentication → Settings
2. Scroll to "Email Auth" section
3. Uncheck "Confirm email"
4. Save changes
5. All new users will auto-confirm

---

### Step 2: Access the Frontend 🌐

1. **Open Browser**
   - Chrome, Firefox, or Edge recommended
   - Open Developer Tools (F12) - we'll check console logs

2. **Navigate to Frontend**
   ```
   http://localhost:3000
   ```

3. **Expected:** Next.js homepage should load

---

### Step 3: Log In 🔐

**Current Setup:** The app doesn't have a login page yet, so we'll use the Supabase auth directly.

**Option A: Quick Login Test (Recommended)**

We'll verify authentication by going directly to the chat page. The app will create a session automatically.

1. **Navigate directly to chat:**
   ```
   http://localhost:3000/chat
   ```

2. **Check browser console** (F12 → Console tab)
   - Look for: "Session created: [session-id]"
   - If you see errors about authentication, we need to add a login flow

**Option B: Create Login Page (5 minutes)**

If the app requires login, I can quickly create a login page for you.

---

### Step 4: Test Chat with Anne-Lise Berg 💬

1. **Select Agent**
   - You should see 4 agent cards
   - Click on: **"Anne-Lise Berg"**

2. **Verify Chat Interface Loads**
   - Should see empty chat
   - Input field at bottom
   - "Change Agent" button at top

3. **Send Test Message**
   - Type: `Hei Anne-Lise! Kan vi få 2 måneder ekstra tid til prosjektet?`
   - Press Enter or click Send

4. **Expected Behavior:**
   - ✅ Your message appears immediately
   - ✅ "AI is thinking..." loader appears
   - ✅ After 3-5 seconds, Anne-Lise responds
   - ✅ Response is in Norwegian
   - ✅ She REJECTS the time extension
   - ✅ Mentions the May 15, 2026 deadline

5. **Example Response:**
   ```
   Tidsfristen er ufravikelig. Skolen må stå klar til skolestart
   i august 2026. Samfunnskostnaden ved forsinkelse – midlertidige
   lokaler, bussing av elever, utsatte inntekter – er langt høyere
   enn eventuelle budsjettoverskridelser.
   ```

---

### Step 5: Test Different Agents 🎭

**Test each agent to verify personalities:**

#### **Bjørn Eriksen (Site Prep Supplier)**
```
Message: "Hva koster grunnarbeidet? Kan du gi oss et tilbud?"

Expected:
- Quotes baseline: 105 MNOK
- Mentions duration: 3.5 months
- Open to negotiation
```

#### **Kari Andersen (Foundation Supplier)**
```
Message: "Kan du gjøre fundamenteringsarbeidet raskere hvis vi betaler mer?"

Expected:
- Discusses time vs. cost tradeoffs
- May quote rush fees
- Baseline: 60 MNOK, 2.5 months
```

#### **Per Johansen (Structural Supplier)**
```
Message: "Kan vi redusere omfanget på råbygget for å spare penger?"

Expected:
- Discusses scope reduction options
- Lists critical vs. optional items
- Baseline: 180 MNOK, 4 months
```

---

### Step 6: Verify Database Storage 💾

After sending messages, verify they're saved to the database.

**Method 1: Check Supabase Dashboard**
1. Supabase Dashboard → Table Editor
2. Select table: `negotiation_history`
3. Should see your messages with:
   - `user_message`: Your text
   - `agent_response`: AI response
   - `timestamp`: When sent
   - `agent_id`: Which agent

**Method 2: Run Database Check Script**
```bash
cd backend
python check_user_data.py
```

Should show:
- Session created
- Messages in negotiation_history table
- User ID matching test user

---

### Step 7: Browser Console Checks 🔍

**Open Developer Tools (F12) → Console tab**

**Expected logs:**
```
Session created: [uuid]
Sending message to agent: anne-lise-berg
AI Response received: { agent_id: "anne-lise-berg", ... }
```

**No errors should appear** - if you see errors, check:
- Network tab for failed API requests
- Console for JavaScript errors
- Backend terminal for Python errors

---

## Troubleshooting 🔧

### Issue: "Kunne ikke opprette spilløkt"
**Cause:** Session creation failed

**Fix:**
1. Check backend is running: `curl http://localhost:8000/`
2. Verify `NEXT_PUBLIC_API_URL` in `frontend/.env.local`
3. Check browser console for error details

---

### Issue: "Email not confirmed"
**Cause:** Test user email needs confirmation

**Fix:**
1. Go to Supabase Dashboard → Authentication → Users
2. Click on `testuser@gmail.com`
3. Click "Confirm email" button

---

### Issue: No AI response appears
**Cause:** Backend API error or Gemini API issue

**Fix:**
1. Check backend terminal for errors
2. Verify Gemini API key in `backend/.env.local`
3. Test backend directly: `python test_chat_simple.py`
4. Check browser Network tab for 500 errors

---

### Issue: "Agent is locked"
**Cause:** Agent timeout mechanic triggered (6 disagreements)

**Fix:**
- Wait 10 minutes for timeout to expire
- Or use a different agent
- Or restart backend to clear timeouts

---

### Issue: Authentication errors
**Cause:** User not logged in or JWT token invalid

**Fix:**
1. Clear browser cookies/localStorage
2. Refresh page
3. Try logging in again
4. Check Supabase auth session in browser DevTools:
   ```javascript
   // In browser console
   localStorage.getItem('sb-cmntglldaqrekloixxoc-auth-token')
   ```

---

## Success Criteria ✅

**The test is successful if:**

1. ✅ Frontend loads without errors
2. ✅ Can select an agent (Anne-Lise Berg)
3. ✅ Can send a message
4. ✅ AI responds in Norwegian (3-5 seconds)
5. ✅ Response matches agent personality:
   - Anne-Lise: Rejects time extensions
   - Suppliers: Discuss negotiation
6. ✅ Messages saved to database
7. ✅ Can switch between agents
8. ✅ No errors in console or backend logs

---

## Test Messages Cheat Sheet 📝

Copy-paste these for quick testing:

**Anne-Lise Berg (should reject):**
```
Kan vi få 2 måneder ekstra tid til prosjektet?
```

**Bjørn Eriksen (should negotiate):**
```
Kan du gjøre grunnarbeidet for 95 MNOK?
```

**Kari Andersen (should discuss tradeoffs):**
```
Hva koster det hvis vi trenger fundamentet ferdig raskere?
```

**Per Johansen (should offer options):**
```
Kan vi redusere omfanget på råbygget for å spare kostnader?
```

---

## Next Steps After Testing

If testing succeeds:
1. ✅ Take screenshots for documentation
2. ✅ Test all 4 agents
3. ✅ Verify database stores data correctly
4. ✅ Move to building the main game page

If testing fails:
1. ❌ Check troubleshooting section above
2. ❌ Review backend and frontend logs
3. ❌ Let me know what error you're seeing

---

**Ready to test!** 🚀

Start with Step 1 (confirm email) then proceed through each step.
