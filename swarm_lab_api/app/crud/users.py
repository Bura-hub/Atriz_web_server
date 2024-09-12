from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

# Obtener un usuario por ID
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Obtener un usuario por nombre de usuario
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# Crear un nuevo usuario
def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password, full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Actualizar un usuario existente
def update_user(db: Session, user_id: int, user: UserCreate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        if user.username != db_user.username:
            if get_user_by_username(db, user.username):
                return None  # Username already exists
        
        db_user.username = user.username
        db_user.hashed_password = get_password_hash(user.password)
        db_user.full_name = user.full_name  # Actualizar el nombre completo
        db.commit()
        db.refresh(db_user)
    return db_user

# Eliminar un usuario
def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user