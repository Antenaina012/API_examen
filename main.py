from datetime import datetime
from typing import List
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import PlainTextResponse, HTMLResponse
from fastapi.security import HTTPBasic
from pydantic import BaseModel

app = FastAPI()

security = HTTPBasic()
posts_memory = []

class Post(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime

# Q1:
@app.get("/ping", response_class=PlainTextResponse)
async def ping():
    return "pong"

# Q2:
@app.get("/home", response_class=HTMLResponse)
async def home():
    return "<h1>Welcome home!</h1>"

# Q3:
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return HTMLResponse(
        content="<html><body><h1>404 NOT FOUND</h1></body></html>",
        status_code=404
    )

# Q4:
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(new_posts: List[Post]):
    posts_memory.extend([post.model_dump() for post in new_posts])
    return posts_memory

#Q5 :
@app.get("/posts")
async def get_posts():
    return posts_memory

# Q6 :
@app.put("/posts")
async def update_posts(updated_posts: List[Post]):
    for new_post in updated_posts:
        existing_index = None
        for i, existing_post in enumerate(posts_memory):
            if existing_post["title"] == new_post.title:
                existing_index = i
                break

        if existing_index is not None:
            posts_memory[existing_index] = new_post.model_dump()
        else:
            posts_memory.append(new_post.model_dump())

    return posts_memory
