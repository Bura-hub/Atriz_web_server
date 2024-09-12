from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.crud.users import get_user, get_user_by_username, create_user, update_user, delete_user
from app.schemas.user import UserCreate, User, Token
from app.db.session import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import verify_password, create_access_token
from datetime import timedelta

router = APIRouter()

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users/", response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db, user)

@router.put("/users/{user_id}", response_model=User)
def update_existing_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user details
    updated_user = update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    return updated_user

@router.delete("/users/{user_id}", response_model=User)
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return delete_user(db, user_id)

@router.post("/login", response_model=Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}