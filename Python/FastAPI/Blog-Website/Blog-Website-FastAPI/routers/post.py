from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from routers.schemas import PostBase, PostDisplay
from sqlalchemy.orm.session import Session
import datetime
from database.models import DbPost
from database.database import get_db
import string
import random
import shutil

router = APIRouter(
    prefix='/post',
    tags=['post']
)

@router.post('/image')
def upload_image(image: UploadFile):
    letter= string.ascii_letters
    rand_str= ''.join(random.choice(letter) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'
    
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
        
    return path


@router.post('')
def create(title: str = Form(...),  # Use Form for the title
            content: str = Form(...),  # Use Form for the content
            creator: str = Form(...),
           image: UploadFile= File(...),
           db: Session =Depends(get_db)):
    
    image_path = upload_image(image)
    
    new_post = DbPost(
        image_url = image_path,
        title = title,
        content = content,
        creator = creator,
        timestamp = datetime.datetime.now()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.get('/all')
def get_post(db: Session= Depends(get_db)):
    return db.query(DbPost).all()

@router.delete('/{id}')
def delete_post(id: int, db: Session= Depends(get_db)):
    post = db.query(DbPost).filter(DbPost.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} not found!')
    db.delete(post)
    db.commit()
    
    return 'Post Deleted Successfully!'
