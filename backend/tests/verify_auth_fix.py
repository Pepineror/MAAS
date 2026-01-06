import requests
import time
import sys

BASE_URL = "http://localhost:7777"

def test_health():
    print("Testing /health (should be public)...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        assert response.status_code == 200
        print("✅ Health check passed")
    except Exception as e:
        print(f"❌ Health check failed: {e}")

def test_protected_no_token():
    print("\nTesting /teams without token (should be 401)...")
    try:
        response = requests.get(f"{BASE_URL}/teams")
        print(f"Status: {response.status_code}")
        # JWTMiddleware returns 401 if token is missing
        assert response.status_code == 401
        print("✅ Protected access restricted as expected")
    except Exception as e:
        print(f"❌ Protected access check failed: {e}")

def get_token():
    print("\nGetting dev token from /api/auth/token...")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/token?role=ADMIN")
        assert response.status_code == 200
        data = response.json()
        token = data.get("access_token")
        assert token is not None
        print(f"✅ Token received: {token[:20]}...")
        return token
    except Exception as e:
        print(f"❌ Failed to get token: {e}")
        return None

def test_protected_with_token(token):
    print("\nTesting /teams with valid token (should be 200)...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/teams", headers=headers)
        print(f"Status: {response.status_code}")
        assert response.status_code == 200
        print("✅ Protected access granted with token")
    except Exception as e:
        print(f"❌ Protected access with token failed: {e}")

if __name__ == "__main__":
    print("Starting verification of MAAS v4.0 Auth Fix...")
    print("Ensure the backend is running on http://localhost:7777")
    
    test_health()
    test_protected_no_token()
    token = get_token()
    if token:
        test_protected_with_token(token)
    else:
        print("Skipping token test because token could not be retrieved.")
