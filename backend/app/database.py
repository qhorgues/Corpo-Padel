from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func
from app.core.config import settings

engine = create_engine(
    settings.database_url,  # ← Changé de DATABASE_URL à database_url
    connect_args={"check_same_thread": False}  # Nécessaire pour SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Générateur de session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialise la base de données avec un admin par défaut"""
    from app.models.models import User, Player, Base
    from app.core.security import get_password_hash
    
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Vérifier si un admin existe déjà
        admin = db.query(User).filter(User.email == "admin@padel.com").first()
        if not admin:
            admin = User(
                email="admin@padel.com",
                password_hash=get_password_hash("Admin@2025!"),
                role="ADMINISTRATEUR",
                must_change_password=False
            )
            db.add(admin)
            player = Player(
                last_name="Admin",
                first_name="Admin",
                company="Admin",
                license_number="L000000",
                birth_date=func.current_date(),
                photo_url="Admin",
                user=admin
            )
            db.add(player)
            db.commit()
            print("✅ Admin créé : admin@padel.com / Admin@2025!")
        else:
            print("ℹ️  Admin existe déjà")
    finally:
        db.close()