from fastapi import FastAPI, Response,status,HTTPException, Depends
from fastapi.params import Body
from typing import Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schemas
from .database import engine, get_db

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

@app.get("/")
def root():
    return{"message":"Hello world!!! "}

@app.get("/sqlalchemy")
def tet_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts",response_model=List[schemas.Post])
def tet_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts 
#def get_posts(): 
    #   cursor.execute("""SELECT * FROM posts """)
    #   posts =cursor.fetchall()


@app.post("/posts", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """,(post.title,post.content,post.published))
    # new_post =cursor.fetchone()
    # conn.commit()
    # new_post=models.Post(title=post.title,content=post.content,published=post.published)
    new_post=models.Post( **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return  post


@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id: int,db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    # post =cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post eith id: {id} was not found")
    return  post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s  RETURNING *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f" post with id {id} dose not exist")
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id: int,updated_post:schemas.PostCreate,db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s  RETURNING *""",(post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post =post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f" post with id {id} dose not exist")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()

    return post_query.first()

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user:schemas.UserCreated, db: Session = Depends(get_db)):
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user