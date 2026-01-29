from sqlalchemy import create_engine
from app.models.models import Base

# Créer les tables sans passer par init_db qui utilise bcrypt
engine = create_engine(
    "sqlite:///padel_corpo.db",
    connect_args={"check_same_thread": False}
)

Base.metadata.create_all(bind=engine)
print("✅ Tables créées avec succès!")
