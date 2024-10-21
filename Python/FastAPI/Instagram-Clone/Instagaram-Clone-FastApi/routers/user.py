from fastapi import APIRouter, Depends, HTTPException, status
from routers.schemas import UserBase, UserDisplay
from sqlalchemy.orm.session import Session
from db.models import DbUser
from db.database import get_db
from db.hashing import Hash

router = APIRouter(
    prefix="/user",
    tags=['user']
)

@router.post('', response_model=UserDisplay )
def create_user(request: UserBase, db: Session = Depends(get_db)):
    new_user = DbUser(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'user with username {username} not found!')
    return user
    