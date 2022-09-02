***MAIN.py***
from fastapi import FastAPI,Query,Depends
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,String,Integer,Boolean

from sqlalchemy.orm import Session

from database import Base,engine,SessionLocal

app=FastAPI()

#model
class User(Base):
    __tablename__ ="users"
    id=Column(Integer,primary_key=True,index=True)
    email =Column(String,unique=True,index=True)
    is_active =Column(Boolean,default=True)

#schema
class UserSchema(BaseModel):
    id:int
    email:str
    is_active:bool

    class Config:
        orm_mode=True

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)

@app.post("/users",response_model=UserSchema)
def index(user:UserSchema,db:Session=Depends(get_db)):
    #db work to put data into db
    u=User(email=user.email,is_active=user.is_active,id=user.id)
    db.add(u)
    db.commit()
    return u

@app.get("/users",response_model=List[UserSchema])
def index(db:Session=Depends(get_db)):
    return db.query(User).all()
