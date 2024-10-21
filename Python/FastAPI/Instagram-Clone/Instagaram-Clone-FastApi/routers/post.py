from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from .schemas import PostBase, PostDisplay
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.models import DbPost
import datetime
from typing import List
import string
import random
import shutil
from routers.schemas import UserAuth
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/post',
    tags=['post']
)

image_url_type = ['absolute', 'relative']

@router.post('', response_model=PostDisplay)
def create_post(request: PostBase, db: Session =Depends(get_db), current_user: UserAuth= Depends(get_current_user)):
    if request.image_url_type not in image_url_type:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                            detail='Entity should be either absolute or relative')       
        
    new_post = DbPost(
    image_url = request.image_url,
    image_url_type = request.image_url_type,
    caption = request.caption,
    timestamp = datetime.datetime.now(),
    user_id = current_user.id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.get('/all', response_model=List[PostDisplay])
def get_all_post(db: Session= Depends(get_db)):
    return db.query(DbPost).all()

@router.post('/image')
def upload_image(image: UploadFile, current_user: UserAuth= Depends(get_current_user)):
    letter= string.ascii_letters
    rand_str= ''.join(random.choice(letter) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'
    
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
        
    return path

@router.get('/delete/{id}')
def delete_post(id: int, db: Session=Depends(get_db), 
                current_user: UserAuth=Depends(get_current_user)):
    post = db.query(DbPost).filter(DbPost.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with post id {id} not found')
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User is not authorised to perform action")
    db.delete(post)
    db.commit()
        
    return "Post Deleted Successfully!"
        
        
        
        
        
        
        
        
        
    