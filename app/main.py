from fastapi import FastAPI, status, HTTPException

from .schemas import Post, UpdatedPost


app = FastAPI()

# dummy db
posts = {
    0: {'id': 0, 'title': 'title post #0', 'content': 'post content #0', 'published': False},
    1: {'id': 1, 'title': 'title post #1', 'content': 'post content #1', 'published': True},
    2: {'id': 2, 'title': 'title post #2', 'content': 'post content #2', 'published': True},
}
post_next_id = len(posts)


@app.get('/')
async def root():
    return {'Hello': 'FastApi ⚡'}


@app.get('/posts')
async def get_posts():
    return {'posts': [*posts.values()]}


@app.get('/posts/{post_id}')
async def get_post(post_id: int):
    if post_id not in posts:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with id {post_id} wasn't found")

    return posts[post_id]


@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_post(payload: Post):
    global post_next_id

    post = {'id': post_next_id, **payload.dict()}
    post_next_id += 1

    posts[post['id']] = post

    return {'data': post}


@app.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    if post_id not in posts:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"post with id {post_id} was't found"
        )

    del posts[post_id]


@app.patch('/posts/{post_id}')
async def update_post(post_id: int, new_post_fields: UpdatedPost):
    if post_id not in posts:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"post with id {post_id} was't found"
        )

    post = posts[post_id]

    print(new_post_fields)
    for k, v in new_post_fields:
        if v is None:
            continue
        post[k] = v

    return post
