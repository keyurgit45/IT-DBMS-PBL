from matplotlib.pyplot import title
import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.blogapp

blog_collection = database.get_collection("blogs")


def blog_helper(blog) -> dict:
    return {
        
        "title": blog["title"],
        "author": blog["author"],
        "user": blog["user"],
        "description": blog["description"],
        "keywords": blog['keywords'],
        "likes": blog["likes"],
        "content": blog["content"],
        "createdAt" : blog["createdAt"]
    }


async def retrieve_blogs():
    blogs = []
    async for blog in blog_collection.find():
        blogs.append(blog_helper(blog))
    return blogs


# Add a new blog into to the database
async def add_blog(blog_data: dict, uid: str) -> dict:
    user = await database['users'].find_one({'_id': ObjectId(uid)})
    blog_data.update({'author' : user['username'], 'user': str(user['_id'])})
    print(blog_data)
    blog = await blog_collection.insert_one(blog_data)
    new_blog = await blog_collection.find_one({"_id": blog.inserted_id})
    return blog_helper(new_blog)
    
# Retrieve a blog with a matching ID
async def retrieve_blog(id: str) -> dict:
    blog = await blog_collection.find_one({"_id": ObjectId(id)})
    if blog:
        return blog_helper(blog)

# Retrieve a blog for current user
async def retrieve_userblog(uid: str) -> list:
    blog = await blog_collection.find({"user": str(uid)}).to_list(100)
    if blog:
        toret = []
        for b in blog:
            toret.append(blog_helper(b))
        return toret


# Update a blog with a matching ID
async def update_blog(id: str,uid: str, data: dict, ):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    blog = await blog_collection.find_one({"_id": ObjectId(id)})
    if blog['user'] != uid:
        return False
    if blog:
        updated_blog = await blog_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_blog:
            return True
        return False


# Delete a blog from the database
async def delete_blog(id: str, uid: str):
    blog = await blog_collection.find_one({"_id": ObjectId(id)})
    if blog['user'] != uid:
        return False
    if blog:
        await blog_collection.delete_one({"_id": ObjectId(id)})
        return True

async def search_by_title(key: str) -> list:
    blog = await blog_collection.find({"title" : { "$regex": f"{key}.*" }}).to_list(100)
    if blog:
        toret = []
        for b in blog:
            toret.append(blog_helper(b))
        return toret
