from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.models import DbComment
from routers.schemas import CommentBase, UserAuth
from auth.oauth2 import get_current_user
from datetime import datetime

router = APIRouter(
    prefix='/comment',
    tags=['comment']
)

@router.get('/all/{post_id}')
def get_all_comments(post_id: int, db: Session= Depends(get_db)):
    return db.query(DbComment).filter(DbComment.post_id == post_id).all()

@router.post('')
def post_comment(request: CommentBase, db: Session= Depends(get_db),
                 current_user: UserAuth=Depends(get_current_user)):
    new_comment = DbComment(
        username = current_user.username,
        text = request.text,
        post_id = request.post_id,
        timestamp = datetime.now()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return new_comment
    