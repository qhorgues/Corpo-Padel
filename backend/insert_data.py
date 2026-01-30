import sqlite3
from datetime import datetime, date, time, timedelta
import bcrypt

# Connexion à la base de données
conn = sqlite3.connect('padel_corpo.db')
cursor = conn.cursor()

# Fonction pour hasher les mots de passe
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

print("👥 Insertion des utilisateurs et joueurs...")

# Joueurs
players_data = [
    ("Dupont", "Jean", "TechCorp", "L123456", "1985-03-15", "jean.dupont@techcorp.fr"),
    ("Martin", "Sophie", "InnoSoft", "L234567", "1990-07-22", "sophie.martin@innosoft.fr"),
    ("Bernard", "Pierre", "TechCorp", "L345678", "1988-11-30", "pierre.bernard@dataflow.fr"),
    ("Dubois", "Marie", "InnoSoft", "L456789", "1992-05-18", "marie.dubois@cloudtech.fr"),
    ("Moreau", "Luc", "DevHub", "L567890", "1987-09-25", "luc.moreau@devhub.fr"),
    ("Laurent", "Emma", "DevHub", "L678901", "1991-12-08", "emma.laurent@codelab.fr"),
    ("Simon", "Thomas", "WebForce", "L789012", "1989-04-14", "thomas.simon@webforce.fr"),
    ("Michel", "Julie", "WebForce", "L890123", "1993-08-21", "julie.michel@appmakers.fr"),
    ("Leroy", "Paul", "SoftWorks", "L901234", "1986-02-28", "paul.leroy@softworks.fr"),
    ("Garcia", "Camille", "SoftWorks", "L012345", "1994-10-05", "camille.garcia@techvision.fr"),
    ("Roux", "Nicolas", "DigitalPlus", "L111222", "1988-06-12", "nicolas.roux@digitalplus.fr"),
    ("Fournier", "Laura", "DigitalPlus", "L222333", "1992-01-19", "laura.fournier@nextgen.fr"),
]

player_hash = hash_password("Player123!")
player_ids = []

for last_name, first_name, company, license, birth_date, email in players_data:
    cursor.execute("""
        INSERT INTO users (email, password_hash, role, must_change_password, is_active)
        VALUES (?, ?, 'JOUEUR', 0, 1)
    """, (email, player_hash))
    user_id = cursor.lastrowid
    
    cursor.execute("""
        INSERT INTO players (last_name, first_name, company, license_number, birth_date, photo_url, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (last_name, first_name, company, license, birth_date, f"{first_name.lower()}.jpg", user_id))
    player_ids.append(cursor.lastrowid)

print("🏊 Insertion des poules...")

pools_data = ["Poule A", "Poule B", "Poule C"]
pool_ids = []

for name in pools_data:
    cursor.execute("INSERT INTO pools (name) VALUES (?)", (name,))
    pool_ids.append(cursor.lastrowid)

print("👥 Insertion des équipes...")

teams_data = [
    ("TechCorp", player_ids[0], player_ids[1], pool_ids[0]),
    ("InnoSoft", player_ids[2], player_ids[3], pool_ids[0]),
    ("DevHub", player_ids[4], player_ids[5], pool_ids[1]),
    ("WebForce", player_ids[6], player_ids[7], pool_ids[1]),
    ("SoftWorks", player_ids[8], player_ids[9], pool_ids[2]),
    ("DigitalPlus", player_ids[10], player_ids[11], pool_ids[2]),
]

team_ids = []
for company, player1, player2, pool_id in teams_data:
    cursor.execute("""
        INSERT INTO teams (company, player1_id, player2_id, pool_id)
        VALUES (?, ?, ?, ?)
    """, (company, player1, player2, pool_id))
    team_ids.append(cursor.lastrowid)

print("📅 Insertion des événements...")

now = datetime.now()
start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

events_data = [
    (
        (start + timedelta(days=i * 10)).strftime("%Y-%m-%d"),
        t
    )
    for i, t in enumerate(["10:00:00", "14:00:00", "09:00:00", "15:00:00"])
]

event_ids = []
for event_date, event_time in events_data:
    cursor.execute("""
        INSERT INTO events (event_date, event_time)
        VALUES (?, ?)
    """, (event_date, event_time))
    event_ids.append(cursor.lastrowid)

print("🎾 Insertion des matchs...")

matches_data = [
    (event_ids[0], team_ids[0], team_ids[1], 1, "A_VENIR", None, None),
    (event_ids[3], team_ids[2], team_ids[3], 2, "A_VENIR", None, None),
    (event_ids[1], team_ids[4], team_ids[5], 3, "A_VENIR", None, None),
    (event_ids[2], team_ids[0], team_ids[1], 1, "A_VENIR", None, None),
    (event_ids[2], team_ids[2], team_ids[3], 2, "TERMINE", 6, 3),
    (event_ids[2], team_ids[4], team_ids[5], 3, "TERMINE", 6, 4),
]

match_ids = []
for event_id, team1_id, team2_id, court, status, score1, score2 in matches_data:
    cursor.execute("""
        INSERT INTO matches (event_id, team1_id, team2_id, court_number, status, score_team1, score_team2)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (event_id, team1_id, team2_id, court, status, score1, score2))
    match_ids.append(cursor.lastrowid)

# Commit et fermeture
conn.commit()
conn.close()

print("\n✅ BASE DE DONNÉES PEUPLÉE AVEC SUCCÈS!")
print("=" * 60)
print("\n📝 Informations de connexion:")
print("   Admin: admin@padel.com / Admin@2025!")
print("   Joueur: jean.dupont@techcorp.fr / Player123!")
print("\n" + "=" * 60)

