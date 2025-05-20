from fastapi import FastAPI, Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password='415263',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("✅ Database connection was successful!")
        break
    except Exception as error:
        print("❌ Connection to database failed")
        print("Error:", error)
        time.sleep(2)


my_posts =[{"title":"title 1","content":"content 1","id":1},{"title":"favorite food","content":"pizza","id":2}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
        
def find_index_post(id):
    for  i,post in enumerate(my_posts):
        if post['id'] == id:
            return i

@app.get("/")
def root():
    return{"message":"Hello world!!! "}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts =cursor.fetchall()
    return {"data": posts }

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """,(post.title,post.content,post.published))
    new_post =cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"post_details": post} 

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    post =cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post eith id: {id} was not found")
    return {"post_details": post} 

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s  RETURNING *""",(str(id),))
    delete_post = cursor.fetchone()
    conn.commit()
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f" post with id {id} dose not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_post(id: int,post:Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f" post with id {id} dose not exist")
    
    post_dict = post.dict()
    post_dict['id']=id
    my_posts[index]=post_dict
    return {"data":"my_posts"}