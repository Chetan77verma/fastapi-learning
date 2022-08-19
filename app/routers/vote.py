from .. import schemas
from .. import models
from ..database import get_db
from sqlalchemy.orm import Session
from .. import oauth2
from fastapi import status , HTTPException , Depends , APIRouter

router = APIRouter(prefix="/vote",
tags=['Vote']
)

@router.post("/" , status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.CreateVote,db:Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {vote.post_id} not found")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id , models.Vote.user_id == current_user.id)
    vote_found = vote_query.first()
    if(vote.dir == 1):
        if(vote_found):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail=f"User {current_user.id} has already voted on post {vote.post_id}")

        new_vote = models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Vote added successfully"}
    else:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details=f"Vote not found")
        vote_query.delete() 
        db.commit()
        return {"message":"Vote removed successfully"}