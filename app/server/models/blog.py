from ast import keyword
import datetime
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field

from server.models.pyobjectid import PyObjectId

class BlogSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    author: str = Field(...)
    user: str = Field(...)
    description: str = Field(...)
    content : str = Field(...)
    keywords : list[str] = []
    likes: int = Field(..., const=0)
    createdAt: datetime.datetime = datetime.datetime.now()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        
        schema_extra = {
            "example": {
                "title": "Blog Title",
                "author": "author",
                "user": "john-doe",
                "content" : "Content of blog",
                "description" : "This is my first blog",
                "likes" : 0,
                "keywords": ["New", "Python"]
            }
        }


class UpdateBlogModel(BaseModel):
    title: Optional[str]
    content: Optional[str]
    desciption: Optional[str]
    keywords: Optional[list[str]]

    class Config:
        schema_extra = {
            "example": {
                "title": "Blog Title",
                "content" : "Content of blog",
                "description" : "This is my first blog",
                "keywords": ["New", "Python"]
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}