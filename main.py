from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


app = FastAPI()
@app.get("/")

#Building the schema for post
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int = None

my_posts = [{"title": "title of post1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "Content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

# request Get method url: "/"
async def root():
    return {"message": "Hello World"}

@app.get("/post")
async def get_post():
    return {"data": my_posts}

@app.post("/posts")
async def create_post(post: Post):
    post_dict = post.dict() # from pydantic object to dictionary
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/post/{id}")
def get_post(id: int):
    post = find_post(int(id))
    return {"post_detail": post}


