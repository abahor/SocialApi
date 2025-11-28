from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session

import models
from database import get_db
from starlette import status
import oauth2
from schemas import Vote

router = APIRouter(tags=["vote"])


@router.post('/vote', status_code=status.HTTP_201_CREATED)
def votes(vote: Vote, db: Session = Depends(get_db), get_current_user=Depends(oauth2.get_current_user)):
    user_id = get_current_user.id
    post = db.query(models.PostModel).filter(models.PostModel.id == vote.post_id).first()
    if not post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {vote.post_id} doesn't exist")
    o = db.query(models.Votes).filter(and_(models.Votes.post_id == vote.post_id, models.Votes.user_id == user_id))
    if o.first():
        if vote.vote_dir == 1:
            return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You already voted for this post")
        elif vote.vote_dir == 0:
            o.delete()
            db.commit()
            return {"message": "vote delete successfully"}
    elif vote.vote_dir == 1:
        new_vote = models.Votes(post_id=vote.post_id, user_id=user_id)
        db.add(new_vote)
        db.commit()
        return {"message": "vote created successfully"}
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="something went wrong")
