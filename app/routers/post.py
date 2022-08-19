from typing import List, Optional
from .. import schemas
from .. import models
from .. import oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

from fastapi import status , HTTPException , Depends , APIRouter

router = APIRouter(prefix="/posts",tags=['Posts'])

@router.get("/",response_model=List[schemas.PostOut])
# @router.get("/")
def get_posts(db:Session = Depends(get_db),current_user = Depends(oauth2.get_current_user),limit:int= 10,offset:int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM POSTS""")
    # posts = cursor.fetchall()
    # Select posts.* , count(votes.post_id) as votes from posts LEFT JOIN votes on posts.id = votes.post_id  group by posts.id;

    results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Post.id == models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(offset).all()
    return results

@router.post("/" , status_code=status.HTTP_201_CREATED , response_model=schemas.Post)
def create_posts(post: schemas.CreatePost,db:Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print("current_user",current_user)
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,db:Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
    # post = cursor.fetchone()

    # Select posts.* , count(votes.post_id) as votes from posts LEFT JOIN votes on posts.id = votes.post_id where posts.id = 3 group by posts.id;

    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Post.id == models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if(post):
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="record not found")

@router.delete("/{id}",response_model=schemas.Post)
def delete_post(id:int,db:Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not allowed to perform this action")

    db.delete(post)
    db.commit()
    return post
  
       

@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int , updated_post:schemas.CreatePost,db:Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not allowed to perform this action")
    post_query.update(updated_post.dict())
    db.commit()
    return post_query.first()
   