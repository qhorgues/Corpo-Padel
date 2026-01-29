import sqlite3

conn = sqlite3.connect('padel_corpo.db')
cursor = conn.cursor()

print("=== ÉQUIPES ===")
cursor.execute('SELECT id, company, player1_id, player2_id FROM teams')
for row in cursor.fetchall():
    print(f"Team {row[0]}: {row[1]} - Players: {row[2]}, {row[3]}")

print("\n=== MATCHS ===")
cursor.execute('SELECT id, team1_id, team2_id, status, score_team1, score_team2 FROM matches')
for row in cursor.fetchall():
    print(f"Match {row[0]}: Team {row[1]} vs Team {row[2]} - Status: {row[3]} - Score: {row[4]}-{row[5]}")

print("\n=== JOUEURS (premiers 5) ===")
cursor.execute('SELECT id, first_name, last_name, company FROM players LIMIT 5')
for row in cursor.fetchall():
    print(f"Player {row[0]}: {row[1]} {row[2]} ({row[3]})")

conn.close()
