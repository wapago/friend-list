from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from typing import Optional
from dotenv import load_dotenv
import os
import pymongo

load_dotenv()

PASSWORD = os.environ.get("PASSWORD")

db_connection_str = "mongodb+srv://theanswerkk:"+PASSWORD+"@mongodb-learning.i9t8oz5.mongodb.net/?retryWrites=true&w=majority&appName=mongodb-learning"
client = pymongo.MongoClient(db_connection_str)
database = client.get_database("friend-list")
collection = database.get_collection("dev-searching")

class Friend(BaseModel):
    id:int
    name:str
    phone:str

app = FastAPI()

friend_in_db = []

# 친구 추가
@app.post('/friends')
def add_friend(friend:Friend):
    print(friend)
    data_to_insert = dict(friend)
    collection.insert_one(data_to_insert)

    return "친구 추가에 성공했습니다."

       

# 친구 조회 / 검색
@app.get('/friends')
def get_friends(name : Optional[str] = None):
    if name:
        friend = collection.find_one({"name":name}, {"_id": 0})
        return friend
    
    global friend_in_db
    friend_in_db = list(collection.find({}, {"_id": 0}))
    return friend_in_db


# 친구 삭제
@app.delete("/friends/{friend_id}")    
def delete_friend(friend_id):
    print(friend_id)
    global friend_in_db
    for friend in friend_in_db: 
        if str(friend["id"]) == str(friend_id):
            collection.delete_one(friend)
            return('삭제성공')
        
    return('삭제실패')

app.mount("/", StaticFiles(directory="static", html=True), name="static")







