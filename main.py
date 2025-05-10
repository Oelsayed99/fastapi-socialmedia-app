from fastapi import FastAPI, Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts =[{"title":"title 1","content":"content 1","id":1},{"title":"favorite food","content":"pizza","id":2}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

@app.get("/")
def root():
    return{"message":"Hello world!!! "}

@app.get("/posts")
def get_posts():
    return {"data": my_posts }

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict =post.dict()
    post_dict['id'] = randrange(0,10000000000)
    my_posts.append(post_dict)

    return {"data":post_dict}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"post_details": post} 

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post eith id: {id} was not found")
    return {"post_details": post} 

