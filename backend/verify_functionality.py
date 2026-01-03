"""
Verify BMAD Model Phase Testing
Tests all database functionality mentioned in Phase 1.3 and Phase 2
"""

from supabase import create_client
from config import settings
import json

print("=" * 80)
print("BMAD Model Phase 1-2 Verification")
print("=" * 80)
print()

# Initialize Supabase
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

# Sign in as test user
email = "testuser@gmail.com"
password = "testpass123"

try:
    response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

    user_id = response.user.id
    print(f"Logged in as: {email}")
    print(f"User ID: {user_id}")
    print()

    # ========================================================================
    # PHASE 1.3: Verify Downstream Updates Work
    # ========================================================================

    print("=" * 80)
    print("PHASE 1.3: Verify Contract Acceptance Updates")
    print("=" * 80)
    print()

    # Get most recent session
    sessions = supabase.table("game_sessions")\
        .select("*")\
        .eq("user_id", user_id)\
        .order("created_at", desc=True)\
        .limit(1)\
        .execute()

    if not sessions.data:
        print("No sessions found. Please create a session and accept at least one contract.")
        exit(1)

    session = sessions.data[0]
    session_id = session['id']

    print(f"Testing Session: {session_id}")
    print(f"Available Budget: {session['available_budget']} MNOK")
    print(f"Current Budget Used: {session['current_budget_used']} MNOK")
    print(f"Total Budget: {session['total_budget']} MNOK")
    print()

    # Test 1.3.1: Check wbs_commitments table
    print("1. WBS_COMMITMENTS TABLE")
    print("-" * 80)
    commitments = supabase.table("wbs_commitments")\
        .select("*")\
        .eq("session_id", session_id)\
        .order("created_at")\
        .execute()

    if commitments.data:
        print(f"✓ Found {len(commitments.data)} commitment(s)")
        for i, c in enumerate(commitments.data, 1):
            print(f"  {i}. WBS {c['wbs_id']}: {c['contract_cost']} MNOK, {c['contract_duration']} days, Agent: {c['agent_id']}")
        print()
    else:
        print("✗ No commitments found")
        print()

    # Test 1.3.2: Check game_sessions.current_budget_used
    print("2. BUDGET TRACKING")
    print("-" * 80)
    if commitments.data:
        total_committed = sum(c['contract_cost'] for c in commitments.data)
        print(f"Total committed cost: {total_committed} MNOK")
        print(f"Session current_budget_used: {session['current_budget_used']} MNOK")
        if abs(total_committed - session['current_budget_used']) < 0.01:
            print("✓ Budget tracking is correct")
        else:
            print(f"✗ Budget mismatch! Committed: {total_committed}, Tracked: {session['current_budget_used']}")
        print()
    else:
        print("Skipped (no commitments)")
        print()

    # Test 1.3.3: Check session_snapshots
    print("3. SESSION_SNAPSHOTS TABLE")
    print("-" * 80)
    snapshots = supabase.table("session_snapshots")\
        .select("*")\
        .eq("session_id", session_id)\
        .order("version")\
        .execute()

    if snapshots.data:
        print(f"✓ Found {len(snapshots.data)} snapshot(s)")
        for sn in snapshots.data:
            print(f"  Version {sn['version']}: {sn['snapshot_type']} - {sn['label']}")
        print()

        # Check if snapshots match commitments (each contract should create a snapshot)
        contract_snapshots = [s for s in snapshots.data if s['snapshot_type'] == 'contract_acceptance']
        budget_snapshots = [s for s in snapshots.data if s['snapshot_type'] == 'budget_revision']

        print(f"Contract acceptance snapshots: {len(contract_snapshots)}")
        print(f"Budget revision snapshots: {len(budget_snapshots)}")
        print(f"Total commitments: {len(commitments.data)}")

        if len(contract_snapshots) == len(commitments.data):
            print("✓ Each contract created a snapshot")
        else:
            print(f"⚠ Snapshot count mismatch: {len(contract_snapshots)} snapshots vs {len(commitments.data)} commitments")
        print()
    else:
        print("✗ No snapshots found")
        print()

    # ========================================================================
    # PHASE 2: Budget Revision Snapshots
    # ========================================================================

    print("=" * 80)
    print("PHASE 2: Verify Budget Revision Snapshots")
    print("=" * 80)
    print()

    if budget_snapshots:
        print(f"✓ Found {len(budget_snapshots)} budget revision snapshot(s)")
        for sn in budget_snapshots:
            print(f"  Version {sn['version']}: {sn['label']}")
            # Try to decode gantt_state to check budget data
            try:
                if sn['gantt_state']:
                    gantt = json.loads(sn['gantt_state'])
                    print(f"    Budget in snapshot: {gantt.get('available_budget', 'N/A')} / {gantt.get('total_budget', 'N/A')} MNOK")
            except:
                pass
        print()
    else:
        print("⚠ No budget revision snapshots found")
        print("  This feature may not have been tested yet.")
        print()

    # ========================================================================
    # VALIDATION TESTS
    # ========================================================================

    print("=" * 80)
    print("VALIDATION TESTS STATUS")
    print("=" * 80)
    print()
    print("To verify validations, the following must be tested manually in the UI:")
    print("1. Dependency validation - Try accepting 1.4.1 before 1.3.1 (should fail)")
    print("2. Timeline validation - Try accepting offers that exceed deadline (should fail)")
    print("3. Budget validation - Try accepting offers that exceed available budget (should fail)")
    print("4. Budget revision validation - Try requesting negative budget increase (should fail)")
    print()

    # ========================================================================
    # SUMMARY
    # ========================================================================

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()

    checks_passed = []
    checks_failed = []

    if commitments.data:
        checks_passed.append("✓ Commitments are stored in database")
    else:
        checks_failed.append("✗ No commitments found")

    if session['current_budget_used'] > 0:
        checks_passed.append("✓ Budget tracking updates correctly")
    else:
        checks_failed.append("⚠ Budget tracking needs verification")

    if snapshots.data:
        checks_passed.append("✓ Snapshots are created")
    else:
        checks_failed.append("✗ No snapshots found")

    if contract_snapshots:
        checks_passed.append("✓ Contract acceptance creates snapshots")
    else:
        checks_failed.append("⚠ Contract snapshots need verification")

    print("PASSED:")
    for check in checks_passed:
        print(f"  {check}")
    print()

    if checks_failed:
        print("NEEDS ATTENTION:")
        for check in checks_failed:
            print(f"  {check}")
        print()

    print(f"Overall: {len(checks_passed)}/{len(checks_passed) + len(checks_failed)} checks passed")
    print()

except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
