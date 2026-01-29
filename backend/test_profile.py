import requests

BASE_URL = "http://localhost:8000/api/v1"

# Login
login_data = {"email": "jean.dupont@techcorp.fr", "password": "Player123!"}
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
token = response.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"}

# Test profile pour voir si le joueur existe
print("=== GET PROFILE ===")
response = requests.get(f"{BASE_URL}/profile/me", headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    profile = response.json()
    print(f"Player ID: {profile.get('id')}")
    print(f"Name: {profile.get('first_name')} {profile.get('last_name')}")
else:
    print(f"Erreur: {response.text}")
