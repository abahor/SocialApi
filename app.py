import uvicorn
from fastapi import FastAPI

import models
from database import engine

models.Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "hello world"}


from routers import users_router, posts_router, auth_router, vote_router

app.include_router(users_router.router)
app.include_router(posts_router.router)
app.include_router(auth_router.router)
app.include_router(vote_router.router)

if __name__ == "__main__":
    uvicorn.run(app)
