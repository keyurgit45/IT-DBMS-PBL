from typing import Optional
from urllib3 import HTTPResponse
from server.models.blog import ResponseModel
from server.auth.hashing import Hash
from fastapi import  Cookie, FastAPI, HTTPException, Depends, Request, Response,status
# from server.auth.oauth import get_current_user
from server.auth.jwttoken import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

from server.models.user import User
import motor.motor_asyncio

MONGO_DETAILS = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
userapp = FastAPI(title="Authentication API",)

db = client.blogapp

@userapp.post('/register' , tags=["User"])
async def create_user(request:User):
   hashed_pass = Hash.bcrypt(request.password)
   user_object = dict(request)
   user_object["password"] = hashed_pass
   user_id = await db["users"].insert_one(user_object)
   return {"res":"user created"}

@userapp.post('/login' , tags=["User"])
async def login(response: Response, request:OAuth2PasswordRequestForm = Depends() ):
    user = await db["users"].find_one({"username":request.username})
    if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    ismatched =  Hash.verify(user["password"],request.password)
    if not ismatched:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    access_token = create_access_token(data={"sub": user["username"] }, response=response)
    # response.set_cookie('_u',request.username , httponly=True, expires=30 * 60,secure=True)
    return {"access_token": access_token, "token_type": "bearer"}

@userapp.get('/logout' , tags=["User"])
def logout(request: Request, response: Response):
    response.delete_cookie("_token")
    return ResponseModel("","Logout Successful.")

@userapp.get("/getcookie" , tags=["User"])
async def getcookie(request: Request):
    try:
        cookie_authorization: str = request.cookies.get("_token")
        # some logic with cookie_authorization
        print(cookie_authorization)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication"
        )