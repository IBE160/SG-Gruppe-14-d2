"""
Create Test User in Supabase
Creates a test user for frontend testing
"""

from supabase import create_client
from config import settings
import sys

print("=" * 60)
print("Creating Test User in Supabase")
print("=" * 60)
print()

# Initialize Supabase client
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

# Test user credentials
email = "testuser@gmail.com"
password = "testpass123"

print(f"Email: {email}")
print(f"Password: {password}")
print()

try:
    # Try to create user
    print("Creating user...")
    response = supabase.auth.sign_up({
        "email": email,
        "password": password
    })

    if response.user:
        print("[OK] User created successfully!")
        print(f"User ID: {response.user.id}")
        print()

        if response.session:
            print("[OK] User is automatically signed in")
            print(f"Access Token: {response.session.access_token[:30]}...")
        else:
            print("[INFO] Email confirmation may be required")
            print("      Check Supabase settings to disable email confirmation for testing")
        print()

        print("=" * 60)
        print("TEST USER READY!")
        print("=" * 60)
        print()
        print("You can now test the frontend by:")
        print(f"1. Go to http://localhost:3000")
        print(f"2. Log in with: {email} / {password}")
        print("3. Navigate to /chat and select an agent")
        print("4. Send a message to test the AI integration")
        print()

    else:
        print("[ERROR] User creation returned no user object")
        print(f"Response: {response}")

except Exception as e:
    error_msg = str(e)

    if "already registered" in error_msg.lower() or "duplicate" in error_msg.lower():
        print("[INFO] User already exists!")
        print()

        # Try to sign in
        try:
            print("Attempting to sign in...")
            signin_response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if signin_response.session:
                print("[OK] Successfully signed in!")
                print(f"User ID: {signin_response.user.id}")
                print(f"Access Token: {signin_response.session.access_token[:30]}...")
                print()

                print("=" * 60)
                print("TEST USER READY!")
                print("=" * 60)
                print()
                print("You can now test the frontend by:")
                print(f"1. Go to http://localhost:3000")
                print(f"2. Log in with: {email} / {password}")
                print("3. Navigate to /chat and select an agent")
                print("4. Send a message to test the AI integration")
                print()
            else:
                print("[ERROR] Could not sign in - no session created")

        except Exception as signin_error:
            print(f"[ERROR] Could not sign in: {signin_error}")
            print()
            print("SOLUTION:")
            print("1. Go to Supabase Dashboard -> Authentication -> Users")
            print(f"2. Find user with email: {email}")
            print("3. Reset password or delete and recreate")

    else:
        print(f"[ERROR] {error_msg}")
        print()
        print("SOLUTION:")
        print("1. Check if email confirmation is enabled in Supabase")
        print("   Settings -> Authentication -> Email Auth -> Disable 'Confirm email'")
        print("2. Or manually create user in Supabase Dashboard:")
        print("   Authentication -> Users -> Add user")
