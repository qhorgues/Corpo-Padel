import sqlite3
from passlib.hash import bcrypt

# Connexion à la base de données
conn = sqlite3.connect('padel_corpo.db')
cursor = conn.cursor()

# Hash du mot de passe avec passlib (compatible avec le backend)
password_hash = bcrypt.hash("Admin@2025!")

# Mise à jour du mot de passe admin
cursor.execute(
    "UPDATE users SET password_hash = ? WHERE email = ?",
    (password_hash, 'admin@padel.com')
)

# Déblocage du compte
cursor.execute(
    "UPDATE login_attempts SET attempts_count = 0, locked_until = NULL WHERE email = ?",
    ('admin@padel.com',)
)

conn.commit()

# Vérification
cursor.execute("SELECT email, role FROM users WHERE email = ?", ('admin@padel.com',))
user = cursor.fetchone()
print(f"✓ Mot de passe mis à jour pour {user[0]}")
print(f"✓ Rôle: {user[1]}")
print(f"✓ Compte débloqué")
print(f"\nConnexion: admin@padel.com / Admin@2025!")

conn.close()
