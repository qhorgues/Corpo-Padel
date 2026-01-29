import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# 1. Login
print("=== LOGIN ===")
login_data = {
    "email": "jean.dupont@techcorp.fr",
    "password": "Player123!"
}
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    token = data.get("access_token")
    print(f"Token obtenu: {token[:50]}...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Get Events
    print("\n=== GET EVENTS ===")
    response = requests.get(f"{BASE_URL}/events", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        events = response.json()
        print(f"Nombre d'événements: {events.get('total', 0)}")
        if events.get('events'):
            print(f"Premier événement: {json.dumps(events['events'][0], indent=2)}")
    else:
        print(f"Erreur: {response.text}")
    
    # 3. Get Matches
    print("\n=== GET MATCHES ===")
    response = requests.get(f"{BASE_URL}/matches", headers=headers, params={"upcoming": True})
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        matches = response.json()
        print(f"Nombre de matchs: {matches.get('total', 0)}")
        if matches.get('matches'):
            print(f"Premier match: {json.dumps(matches['matches'][0], indent=2)}")
    else:
        print(f"Erreur: {response.text}")
    
    # 4. Get Results
    print("\n=== GET MY RESULTS ===")
    response = requests.get(f"{BASE_URL}/results/my-results", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        results = response.json()
        print(f"Nombre de résultats: {len(results.get('results', []))}")
        print(f"Stats: {json.dumps(results.get('statistics', {}), indent=2)}")
    else:
        print(f"Erreur: {response.text}")
    
    # 5. Get Rankings
    print("\n=== GET RANKINGS ===")
    response = requests.get(f"{BASE_URL}/results/rankings", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        rankings = response.json()
        print(f"Nombre de classements: {len(rankings.get('rankings', []))}")
        if rankings.get('rankings'):
            print(f"Premier: {json.dumps(rankings['rankings'][0], indent=2)}")
    else:
        print(f"Erreur: {response.text}")
else:
    print(f"Erreur login: {response.text}")
