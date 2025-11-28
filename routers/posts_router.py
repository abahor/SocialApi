from typing import List, Optional, Set

from fastapi import Depends, Response, APIRouter, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette import status

import models
import oauth2
from database import get_db
from schemas import PostResponseSchema, Post, PostOut

router = APIRouter()


@router.get("/posts", response_model=List[PostOut])
# @router.get("/posts", response_model=PostResponseSchema)
# @router.get("/posts")
def posts(search: Optional[str] = "", limit: int = 10, db: Session = Depends(get_db), skip: int = 0,
          # current_user=Depends(oauth2.get_current_user)
          ):
    # yy = db.query(models.PostModel).filter(
    #     models.PostModel.owner_id == current_user.id
    # ).all()
    # noinspection PyTypeChecker
    # join(models.Votes, models.Votes.post_id == models.PostModel.id, isouter=True).\
    # pos = db.query(models.PostModel, func.count(models.Votes.post_id)).join(models.Votes, models.Votes.post_id == models.PostModel.id, isouter=True).group_by(models.PostModel.id).all()
    pos = db.query(models.PostModel, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.PostModel.id, isouter=True).group_by(models.PostModel.id)
        # .filter(
        # models.PostModel.title.contains(search)).limit(limit).offset(skip)
    print(
        pos
    )
    # group_by(models.PostModel.id).filter(models.PostModel.title.contains(search)).limit(limit).offset(skip)
    # print(pos)
    # print(dir(pos[0]))
    # print(pos[0][0])
    # # print(g)
    # # print(pos.all())
    # # for i in pos:
    # #     print(dict(i[0]))
    #     # print(dict(i))
    # # return yy
    # f = PostOut(pos[0])
    # print(f)
    # print(dict(zip(pos)))
    # for i in pos:
    #     t
    pos = pos.all()
    # print(pos[0].t._data)
    print(pos[0]._key_to_index)
    print(pos[0].PostModel.owner_id)
    return pos

    # def beautify_posts(n):
    #     post = n.Post
    #     post.votes = n.votes
    #     return post
    #
    # out_posts = list(map(beautify_posts, pos))
    #
    # return list(out_posts)
    # return "pos"


@router.put("/update/{idg}", response_model=PostResponseSchema)
def update_post(idg: int, posted: Post, db: Session = Depends(get_db),
                get_current_user=Depends(oauth2.get_current_user)):
    yy = db.query(models.PostModel).filter(models.PostModel.id == idg)
    print(yy)
    post = yy.first()
    if not post or post.owner_id != get_current_user.id:
        return {"problem": "das"}
    print(posted.model_dump())
    # if y
    yy.update(posted.model_dump())
    # yy.title = "the update title"
    # yy.content = "the update content"
    db.commit()

    return yy.first()


# @router.get("/posts/{idg:str}",)
@router.get("/posts/{idg:str}", response_model=PostOut)
def get_post(idg: str, db: Session = Depends(get_db),
             # get_current_user=Depends(oauth2.get_current_user)
             ):
    # p = db.query(models.PostModel).filter(models.PostModel.id == idg)
    # print(p)
    # p = db.query(models.PostModel).filter(models.PostModel.id == idg).first()
    p = db.query(models.PostModel, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.PostModel.id, isouter=True).group_by(models.PostModel.id).filter(
        models.PostModel.id == idg
    ).first()
    # if p.owner_id == get_current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    # p = find_post(idg)
    print(p)
    if p:
        return p
    else:
        return Response(content="Doesn't Exist", status_code=404)


@router.delete("/posts/{idg:str}")
def delete_post(idg: str, db: Session = Depends(get_db), get_current_user=Depends(oauth2.get_current_user)):
    t = db.query(models.PostModel).filter(models.PostModel.id == idg).first()
    print(t)
    if t.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    try:
        db.delete(t)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        return {"data": "Something went wrong"}
    # conn.commit()

    return {"data": "Post deleted"}


@router.get("/posts/latest")
def posts():
    return {"data": "the latest post"}


@router.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(posted: Post, db: Session = Depends(get_db), get_current_user=Depends(oauth2.get_current_user)):
    t = models.PostModel(owner_id=get_current_user.id, **posted.model_dump())
    try:
        db.add(t)
        db.commit()
        db.refresh(t)
        print(t)
    except:
        db.rollback()
        return "error"
    return {"data": t}
