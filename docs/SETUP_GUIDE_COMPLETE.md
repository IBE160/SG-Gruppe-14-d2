# PM Simulator - Complete Setup Guide
## Step-by-Step Manual Setup Instructions

**Version:** 1.0
**Date:** December 14, 2024
**Estimated Time:** 15 minutes
**Difficulty:** Beginner-friendly

---

## 📋 Table of Contents

1. [Prerequisites & Accounts](#prerequisites)
2. [Step 1: Import Database to Supabase](#step1)
3. [Step 2: Get Gemini API Key](#step2)
4. [Step 3: Configure Backend](#step3)
5. [Step 4: Test Backend](#step4)
6. [Step 5: Start Backend Server](#step5)
7. [Troubleshooting](#troubleshooting)
8. [Verification Checklist](#checklist)

---

<a name="prerequisites"></a>
## 🔧 Prerequisites & Accounts

Before you begin, ensure you have:

### **Accounts Required:**

1. ✅ **Supabase Account** (already set up)
   - Project: `cmntglldaqrekloixxoc`
   - URL: https://supabase.com/dashboard

2. 🔴 **Google Account** (for Gemini API)
   - Any Gmail account works
   - Free tier available

### **Programs Required:**

1. ✅ **Web Browser**
   - Chrome, Firefox, Edge, or Safari
   - Used for: Supabase dashboard, Google AI Studio

2. ✅ **Text Editor**
   - VS Code, Notepad++, or any code editor
   - Used for: Editing `.env.local` file

3. ✅ **Terminal/Command Prompt**
   - Windows: Command Prompt or PowerShell
   - Mac/Linux: Terminal
   - Used for: Running backend server

### **Files You'll Need:**

- `database/migrations/001_complete_schema.sql` (ready in your project)
- `backend/.env.local` (ready in your project)

---

<a name="step1"></a>
## 📊 Step 1: Import Database Schema to Supabase

**Time:** 5 minutes
**Difficulty:** Easy

This step creates 5 database tables in your Supabase project.

### **1.1 Open Supabase Dashboard**

1. Open your web browser
2. Go to: **https://supabase.com/dashboard**
3. Log in with your Supabase credentials
4. You'll see your project list

**Screenshot Location:** Main dashboard with project tiles

### **1.2 Select Your Project**

1. Look for project: **cmntglldaqrekloixxoc**
2. Click on the project tile to open it
3. You'll be taken to the project overview page

**What you'll see:**
- Left sidebar with menu options
- Project details in the center
- Database, Auth, Storage icons

### **1.3 Navigate to SQL Editor**

1. Look at the **left sidebar**
2. Scroll down if needed
3. Click on **"SQL Editor"** icon (looks like a code bracket `</>`)
4. The SQL Editor page will open

**What you'll see:**
- Large text area for SQL code
- "New query" button at the top
- List of saved queries on the left (if any)

### **1.4 Create New Query**

1. Click the **"New query"** button at the top
2. Or click the **"+"** icon
3. A blank query editor will appear

**Editor features:**
- Large text box for entering SQL
- Syntax highlighting (SQL keywords in color)
- Line numbers on the left
- "Run" button (green, top-right)

### **1.5 Open Database Schema File**

**Using Windows File Explorer:**

1. Open File Explorer (Windows key + E)
2. Navigate to your project folder:
   ```
   C:\Users\morte\Documents\GitHub\SG-Gruppe-14-d2
   ```
3. Go to subfolder: **database** → **migrations**
4. Find file: **001_complete_schema.sql**
5. Right-click the file
6. Select **"Open with"** → Choose your text editor (VS Code, Notepad++, or Notepad)

**OR Using VS Code:**

1. Open VS Code
2. File → Open Folder
3. Select: `C:\Users\morte\Documents\GitHub\SG-Gruppe-14-d2`
4. In the file tree, navigate to:
   ```
   database/migrations/001_complete_schema.sql
   ```
5. Click to open the file

### **1.6 Copy All SQL Code**

1. In your text editor with `001_complete_schema.sql` open
2. Select all content:
   - **Windows:** Press `Ctrl + A`
   - **Mac:** Press `Cmd + A`
3. Copy the selection:
   - **Windows:** Press `Ctrl + C`
   - **Mac:** Press `Cmd + C`

**What you're copying:**
- 527 lines of SQL code
- Creates 5 tables
- Sets up security policies
- Adds triggers and indexes

### **1.7 Paste SQL into Supabase Editor**

1. Go back to your Supabase SQL Editor tab in your browser
2. Click inside the large text area
3. Paste the SQL code:
   - **Windows:** Press `Ctrl + V`
   - **Mac:** Press `Cmd + V`

**What you should see:**
- The entire SQL file content in the editor
- Colored syntax highlighting
- Line numbers showing 1-527

### **1.8 Run the SQL Migration**

1. Look for the **"Run"** button (usually green, top-right corner)
2. **Click "Run"**
3. Wait 5-10 seconds for execution

**What happens:**
- Supabase processes all 527 lines
- Creates database tables
- Sets up security
- Adds computed columns

### **1.9 Check for Success**

**Success Message:**

You'll see one of these messages at the bottom:
- ✅ "Success. No rows returned"
- ✅ "Success. X rows affected"
- ✅ Green checkmark icon

**Error Message (if something went wrong):**

- ❌ Red error box
- Error message starting with "ERROR:"
- Line number of the problem

**If you see an error:**
- See [Troubleshooting Section](#troubleshooting) below

### **1.10 Verify Tables Were Created**

**Method 1: Using SQL Query**

1. In the SQL Editor, clear the current query:
   - Select all (Ctrl+A)
   - Delete
2. Paste this verification query:

```sql
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
```

3. Click **"Run"**

**Expected Result:**

You should see **5 rows** with these exact table names:
```
agent_timeouts
game_sessions
negotiation_history
user_analytics
wbs_commitments
```

**Method 2: Using Table Editor**

1. Click **"Table Editor"** in the left sidebar
2. Look for the tables in the list:
   - ✅ agent_timeouts
   - ✅ game_sessions
   - ✅ negotiation_history
   - ✅ user_analytics
   - ✅ wbs_commitments

### **1.11 Database Import Complete! ✅**

If you see all 5 tables, you're done with Step 1!

---

<a name="step2"></a>
## 🔑 Step 2: Get Google Gemini API Key

**Time:** 3 minutes
**Difficulty:** Easy

This step gets you a free API key to use Google's Gemini AI.

### **2.1 Open Google AI Studio**

1. Open a new browser tab
2. Go to: **https://aistudio.google.com/apikey**
3. You'll be redirected to Google sign-in if not logged in

### **2.2 Sign In with Google Account**

1. Enter your Gmail address
2. Enter your password
3. Click **"Sign in"**

**Note:** Use any Google account - personal Gmail works fine

### **2.3 Access API Key Page**

After signing in, you'll land on the API Keys page.

**What you'll see:**
- Page title: "Get an API key"
- Blue button: "Create API Key"
- Or: List of existing API keys (if you have any)

### **2.4 Create New API Key**

**If you already have an API key:**
- Skip to step 2.7 and use your existing key

**If you need a new key:**

1. Click the **"Create API Key"** button
2. A dialog box will appear

### **2.5 Select Google Cloud Project**

The dialog asks: "Which Google Cloud project would you like to use?"

**Option A - Create new project (Recommended):**

1. Click **"Create API key in new project"**
2. Wait 5-10 seconds
3. Your API key will be generated

**Option B - Use existing project:**

1. Select an existing project from dropdown
2. Click **"Create API key"**

### **2.6 Copy Your API Key**

**What you'll see:**
- A dialog box with your API key
- The key looks like: `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`
- A **"Copy"** button next to the key
- ⚠️ Warning message about keeping it secure

**Action:**

1. Click the **"Copy"** button (or manually select and copy)
2. Your API key is now in your clipboard
3. Click **"Close"** or "Got it"

**IMPORTANT SECURITY NOTES:**

⚠️ **Keep this key private!**
- Don't share it publicly
- Don't commit it to Git/GitHub
- Don't post it in forums or chat
- Our `.env.local` file is already in `.gitignore` (safe)

### **2.7 Save API Key Temporarily**

While you have the key copied:

**Option A - Paste into Notepad (Recommended):**

1. Open Notepad (Windows) or TextEdit (Mac)
2. Paste the key (Ctrl+V)
3. Keep this window open for next step

**Option B - Leave the tab open:**

- Keep the Google AI Studio tab open
- You can view your key anytime

### **2.8 Gemini API Key Obtained! ✅**

You now have a valid Gemini API key ready to use!

---

<a name="step3"></a>
## ⚙️ Step 3: Configure Backend Environment

**Time:** 2 minutes
**Difficulty:** Easy

This step adds your Gemini API key to the backend configuration.

### **3.1 Open Backend Folder**

**Using File Explorer:**

1. Open File Explorer (Windows key + E)
2. Navigate to:
   ```
   C:\Users\morte\Documents\GitHub\SG-Gruppe-14-d2\backend
   ```
3. You should see files including:
   - `.env.local` (the file we need)
   - `main.py`
   - `config.py`
   - `requirements.txt`

### **3.2 Open .env.local File**

**Method 1 - Using VS Code (Recommended):**

1. Right-click `.env.local`
2. Select **"Open with Code"** or **"Open with VS Code"**
3. The file opens in VS Code

**Method 2 - Using Notepad++:**

1. Right-click `.env.local`
2. Select **"Edit with Notepad++"**

**Method 3 - Using Notepad (Windows):**

1. Right-click `.env.local`
2. Select **"Open with"** → **"Notepad"**

**What you'll see:**

```env
SUPABASE_URL=https://cmntglldaqrekloixxoc.supabase.co
SUPABASE_ANON_KEY=sb_publishable_ChXJKjeBDhzccsllf_4d8A_MoOP3S6l
SUPABASE_JWT_SECRET=sb_secret_kAepUmTdBY2uRhQJwOjSbw_NGESm0Pj

# Gemini AI Configuration
GEMINI_API_KEY=REPLACE_WITH_YOUR_ACTUAL_API_KEY
GEMINI_MODEL=gemini-1.5-pro
```

### **3.3 Replace Placeholder with Your API Key**

1. Find line 6: `GEMINI_API_KEY=REPLACE_WITH_YOUR_ACTUAL_API_KEY`
2. Select the text: `REPLACE_WITH_YOUR_ACTUAL_API_KEY`
   - Don't select `GEMINI_API_KEY=`
   - Only select the placeholder text
3. Paste your API key (Ctrl+V)

**After editing, line 6 should look like:**

```env
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

**IMPORTANT:**
- ✅ No spaces around the `=` sign
- ✅ No quotes around the key
- ✅ No extra lines or spaces

**Example of CORRECT format:**
```env
GEMINI_API_KEY=AIzaSyD1234567890abcdefghijklmnopqrstuvwxyz
GEMINI_MODEL=gemini-1.5-pro
```

**Example of WRONG format:**
```env
GEMINI_API_KEY = AIza...  ❌ (spaces around =)
GEMINI_API_KEY="AIza..."  ❌ (quotes)
GEMINI_API_KEY=           ❌ (empty)
```

### **3.4 Save the File**

1. **In VS Code or Notepad++:**
   - Press `Ctrl + S` (Windows)
   - Or: File → Save

2. **In Notepad:**
   - File → Save
   - Or: Press `Ctrl + S`

**You should see:**
- No asterisk (*) next to filename
- File saved indicator

### **3.5 Close the File**

You can now close the editor.

### **3.6 Backend Configuration Complete! ✅**

Your backend is now configured with the Gemini API key!

---

<a name="step4"></a>
## 🧪 Step 4: Test Backend Configuration

**Time:** 2 minutes
**Difficulty:** Easy

This step verifies everything is set up correctly.

### **4.1 Open Terminal/Command Prompt**

**Windows - Method 1 (Using File Explorer):**

1. Open File Explorer
2. Navigate to: `C:\Users\morte\Documents\GitHub\SG-Gruppe-14-d2\backend`
3. In the address bar, type: `cmd`
4. Press Enter
5. Command Prompt opens in the backend folder

**Windows - Method 2 (Using Start Menu):**

1. Press Windows key
2. Type: `cmd`
3. Press Enter
4. Command Prompt opens
5. Navigate to backend folder:
   ```cmd
   cd C:\Users\morte\Documents\GitHub\SG-Gruppe-14-d2\backend
   ```

**Windows - Method 3 (Using VS Code):**

1. Open VS Code
2. Terminal → New Terminal
3. Navigate to backend:
   ```cmd
   cd backend
   ```

**Mac/Linux:**

1. Open Terminal
2. Navigate to backend:
   ```bash
   cd ~/path/to/SG-Gruppe-14-d2/backend
   ```

### **4.2 Verify You're in Backend Folder**

Type this command:

**Windows:**
```cmd
dir
```

**Mac/Linux:**
```bash
ls
```

**You should see these files:**
- `main.py`
- `config.py`
- `test_setup.py` ← We'll run this
- `.env.local`
- `requirements.txt`

### **4.3 Run Test Script**

Type this exact command:

```bash
python test_setup.py
```

Press Enter.

### **4.4 Read Test Results**

**EXPECTED OUTPUT (Success):**

```
============================================================
PM Simulator Backend Setup Test
============================================================

Test 1: Environment Configuration
------------------------------------------------------------
[OK] Config loaded successfully
   Supabase URL: https://cmntglldaqrekloixxoc.supabase.co...
   Supabase Key: sb_publishable_ChXJK...
[OK] Gemini API Key: AIzaSy...
   Gemini Model: gemini-1.5-pro

Test 2: Agent Prompts Loader
------------------------------------------------------------
[OK] Loaded 4 agent prompts:
   - anne-lise-berg: Anne-Lise Berg
     Prompt length: 8047 characters
   - bjorn-eriksen: Bjørn Eriksen
     Prompt length: 5783 characters
   - kari-andersen: Kari Andersen
     Prompt length: 4028 characters
   - per-johansen: Per Johansen
     Prompt length: 4503 characters
[OK] Anne-Lise prompt contains 'NEVER' rule (correct)

Test 3: Gemini Service
------------------------------------------------------------
[OK] Gemini service initialized
   Model: models/gemini-1.5-pro
   Temperature: 0.7
   Max tokens: 2048

Test 4: Supabase Connection
------------------------------------------------------------
[OK] Connected to Supabase
[OK] game_sessions table exists
[OK] wbs_commitments table exists
[OK] negotiation_history table exists
[OK] agent_timeouts table exists
[OK] user_analytics table exists

============================================================
SUCCESS! All tests passed!
============================================================

Next steps:
2. Start the backend: uvicorn main:app --reload
3. Visit API docs: http://localhost:8000/docs
4. Test chat endpoint with a real message
```

### **4.5 Interpret Results**

**All [OK] - Perfect! ✅**
- Everything configured correctly
- Proceed to Step 5

**Any [WARN] - Warning ⚠️**
- Something not critical is missing
- Backend might still work
- Read the warning message

**Any [FAIL] - Error ❌**
- Critical issue found
- Backend won't work correctly
- See [Troubleshooting](#troubleshooting)

### **4.6 Common Test Results**

**Scenario 1: Missing API Key**
```
[WARN] GEMINI_API_KEY not configured yet!
```
**Fix:** Go back to Step 3 and add your API key

**Scenario 2: Missing Database Tables**
```
[FAIL] game_sessions table missing
```
**Fix:** Go back to Step 1 and import the database schema

**Scenario 3: Invalid API Key**
```
[FAIL] Gemini service error: API key not valid
```
**Fix:** Check your API key in `.env.local` - ensure it's correct

### **4.7 Testing Complete! ✅**

If all tests passed, your backend is ready to run!

---

<a name="step5"></a>
## 🚀 Step 5: Start Backend Server

**Time:** 1 minute
**Difficulty:** Easy

This starts your backend API server.

### **5.1 Ensure You're in Backend Folder**

In your terminal/command prompt, verify you're still in the backend folder:

```bash
cd C:\Users\morte\Documents\GitHub\SG-Gruppe-14-d2\backend
```

### **5.2 Start the Server**

Type this exact command:

```bash
uvicorn main:app --reload
```

Press Enter.

### **5.3 Server Starting**

**You'll see output like:**

```
INFO:     Will watch for changes in these directories: ['C:\\Users\\morte\\Documents\\GitHub\\SG-Gruppe-14-d2\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [67890]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Key indicators:**
- ✅ "Uvicorn running on http://127.0.0.1:8000"
- ✅ "Application startup complete"
- ✅ No error messages

### **5.4 Test in Browser**

1. Open your web browser
2. Go to: **http://localhost:8000**

**You should see:**
```json
{
  "message": "Welcome to the FastAPI backend with Supabase!"
}
```

### **5.5 View API Documentation**

1. Go to: **http://localhost:8000/docs**

**You should see:**
- Interactive API documentation (Swagger UI)
- List of all 8 endpoints:
  - GET `/` - Root
  - GET `/me` - Current user
  - **POST `/api/chat`** - Chat with AI agents ⭐
  - POST `/api/sessions` - Create session
  - GET `/api/sessions/{id}` - Get session
  - PUT `/api/sessions/{id}` - Update session
  - POST `/api/sessions/{id}/commitments` - Create commitment
  - GET `/api/sessions/{id}/commitments` - Get commitments

### **5.6 Keep Server Running**

**IMPORTANT:**
- ✅ Keep this terminal window open
- ✅ Keep the server running
- ✅ Don't close the window

**To stop the server later:**
- Press `Ctrl + C` in the terminal

**To restart the server:**
- Run `uvicorn main:app --reload` again

### **5.7 Backend Server Running! ✅**

Your backend is now live and ready to accept requests!

---

<a name="troubleshooting"></a>
## 🔧 Troubleshooting

### **Problem 1: "Table already exists" Error in Step 1**

**Error Message:**
```
ERROR: relation "game_sessions" already exists
```

**Cause:**
- Database schema was previously imported
- Tables already exist

**Solution A (Recommended):**
- Skip Step 1 - tables already exist
- Continue to Step 2

**Solution B (Clean slate):**

Run this SQL first to delete all tables:

```sql
DROP TABLE IF EXISTS public.agent_timeouts CASCADE;
DROP TABLE IF EXISTS public.negotiation_history CASCADE;
DROP TABLE IF EXISTS public.wbs_commitments CASCADE;
DROP TABLE IF EXISTS public.user_analytics CASCADE;
DROP TABLE IF EXISTS public.game_sessions CASCADE;
```

Then run the full migration again.

---

### **Problem 2: "Invalid API key" Error**

**Error Message:**
```
[FAIL] Gemini service error: Invalid API key
```

**Possible Causes:**

1. **Typo in API key**
   - Check for extra spaces
   - Check for missing characters
   - Copy key again from Google AI Studio

2. **API key restrictions**
   - Go to: https://aistudio.google.com/apikey
   - Check if key has restrictions
   - Try creating a new unrestricted key

3. **Wrong format in .env.local**
   - Ensure no quotes around key
   - Ensure no spaces around `=`
   - Example: `GEMINI_API_KEY=AIzaSy...`

**Solution:**

1. Go back to Google AI Studio
2. Copy the key again (use the copy button)
3. Open `backend/.env.local`
4. Delete the entire line 6
5. Type fresh: `GEMINI_API_KEY=` (no space after =)
6. Paste your key
7. Save
8. Run test again

---

### **Problem 3: "Could not find table" Error**

**Error Message:**
```
[FAIL] Could not find the table 'public.game_sessions'
```

**Cause:**
- Database schema not imported
- Import failed silently

**Solution:**

1. Go back to Supabase SQL Editor
2. Run the verification query:
   ```sql
   SELECT table_name
   FROM information_schema.tables
   WHERE table_schema = 'public';
   ```
3. Check if your tables are listed
4. If not, re-run the migration from Step 1

---

### **Problem 4: "Module not found" Error**

**Error Message:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Cause:**
- Python dependencies not installed

**Solution:**

1. Open terminal in backend folder
2. Run:
   ```bash
   pip install -r requirements.txt
   ```
3. Wait for installation to complete
4. Try running test again

---

### **Problem 5: "uvicorn: command not found"**

**Error Message:**
```
'uvicorn' is not recognized as an internal or external command
```

**Cause:**
- Uvicorn not installed or not in PATH

**Solution:**

**Option 1 - Install uvicorn:**
```bash
pip install uvicorn
```

**Option 2 - Run as Python module:**
```bash
python -m uvicorn main:app --reload
```

---

### **Problem 6: Port 8000 Already in Use**

**Error Message:**
```
ERROR: [Errno 48] Address already in use
```

**Cause:**
- Another server is running on port 8000

**Solution:**

**Option 1 - Stop the other server:**
1. Find the terminal running the other server
2. Press `Ctrl + C` to stop it
3. Start your server again

**Option 2 - Use a different port:**
```bash
uvicorn main:app --reload --port 8001
```
Then use `http://localhost:8001` instead

---

### **Problem 7: "Permission denied" in Supabase**

**Error Message:**
```
ERROR: permission denied for schema public
```

**Cause:**
- Not logged in as project owner
- Insufficient permissions

**Solution:**

1. Check you're logged in to correct Supabase account
2. Ensure you're the project owner
3. Try logging out and logging back in
4. Contact project owner for access

---

<a name="checklist"></a>
## ✅ Final Verification Checklist

Before considering setup complete, verify:

### **Database:**
- [ ] Logged into Supabase dashboard
- [ ] Opened SQL Editor
- [ ] Ran `001_complete_schema.sql` successfully
- [ ] Verified 5 tables exist:
  - [ ] game_sessions
  - [ ] wbs_commitments
  - [ ] negotiation_history
  - [ ] agent_timeouts
  - [ ] user_analytics

### **Gemini API:**
- [ ] Visited https://aistudio.google.com/apikey
- [ ] Created or retrieved API key
- [ ] Copied API key to clipboard

### **Backend Configuration:**
- [ ] Opened `backend/.env.local`
- [ ] Replaced `REPLACE_WITH_YOUR_ACTUAL_API_KEY` with real key
- [ ] Saved file
- [ ] No quotes or spaces around key

### **Testing:**
- [ ] Opened terminal in backend folder
- [ ] Ran `python test_setup.py`
- [ ] All tests show `[OK]`
- [ ] No `[FAIL]` messages

### **Backend Server:**
- [ ] Ran `uvicorn main:app --reload`
- [ ] Server started successfully
- [ ] Visited http://localhost:8000
- [ ] Saw welcome message
- [ ] Visited http://localhost:8000/docs
- [ ] Saw 8 API endpoints listed

### **All Complete:**
- [ ] All checkboxes above are checked
- [ ] Backend is running
- [ ] No error messages
- [ ] Ready to test chat with AI agents!

---

## 🎉 Setup Complete!

**Congratulations!** Your PM Simulator backend is now fully configured and running.

### **What You've Accomplished:**

✅ Imported complete database schema (5 tables)
✅ Configured Gemini AI integration
✅ Set up backend environment
✅ Verified all components working
✅ Started backend server

### **What You Can Do Now:**

1. **Chat with AI Agents:**
   - Use the `/api/chat` endpoint
   - Get Norwegian responses from 4 different agents

2. **Create Game Sessions:**
   - Initialize budget tracking
   - Start negotiation simulations

3. **Track Commitments:**
   - Accept supplier offers
   - Monitor budget usage

### **Next Steps:**

1. Test the chat endpoint with real messages
2. Connect frontend to backend (future task)
3. Start building the main game page

### **Need Help?**

- **Test endpoint:** http://localhost:8000/docs
- **Documentation:** See `docs/BACKEND_API_COMPLETED.md`
- **Quick reference:** See `QUICK_START_GUIDE.md`

---

## 📞 Support & Additional Resources

### **Documentation Files:**

- `docs/DATABASE_IMPLEMENTATION_GUIDE.md` - Full database reference
- `docs/BACKEND_API_COMPLETED.md` - Complete API documentation
- `QUICK_START_GUIDE.md` - 15-minute quick start
- `database/IMPORT_TO_SUPABASE.md` - Database import guide

### **API Endpoints Reference:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/chat` | POST | Chat with AI agents |
| `/api/sessions` | POST | Create game session |
| `/api/sessions/{id}` | GET | Get session data |
| `/api/sessions/{id}` | PUT | Update session |
| `/api/sessions/{id}/commitments` | POST | Accept offer |
| `/api/sessions/{id}/commitments` | GET | Get commitments |

### **Important URLs:**

- **Supabase Dashboard:** https://supabase.com/dashboard
- **Google AI Studio:** https://aistudio.google.com/apikey
- **API Documentation:** http://localhost:8000/docs (when server running)
- **Backend Root:** http://localhost:8000

---

**End of Setup Guide**

**Version:** 1.0
**Last Updated:** December 14, 2024
**Total Setup Time:** ~15 minutes
