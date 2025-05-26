from fastapi import FastAPI, Response,status,HTTPException, Depends
from fastapi.params import Body
from typing import Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schemas, utils
from .database import engine, get_db
from .routers import posts,user ,auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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

app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return{"message":"Hello world!!! "}

@app.get("/sqlalchemy")
def tet_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


