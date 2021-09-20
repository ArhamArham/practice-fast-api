from typing import List

import fastapi as _fastapi
import services as _service
import schemas as _schemas
import sqlalchemy.orm as _orm

app = _fastapi.FastAPI()

_service.create_database()


@app.post("/users/", response_model=_schemas.User)
def create_user(
        user: _schemas.UserCreate,
        db: _orm.Session = _fastapi.Depends(_service.get_db)
):
    db_user = _service.get_user_by_email(db=db, email=user.email)

    if db_user:
        raise _fastapi.HTTPException(
            status_code=422, detail="The email address is already taken"
        )

    return _service.create_user(db=db, user=user)


@app.get('/users/', response_model=List[_schemas.User])
def get_users(
        skip: int = 0,
        limit: int = 0,
        db: _orm.Session = _fastapi.Depends(_service.get_db)
):
    return _service.get_users(db=db, skip=skip, limit=limit)


@app.get("/users/{user_id}", response_model=_schemas.User)
def get_user(
        user_id: int,
        db: _orm.Session = _fastapi.Depends(_service.get_db)
):
    user = _service.get_user(db=db, user_id=user_id)
    if user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="User not found"
        )

    return user


@app.delete("/users/{user_id}")
def delete_user(
        user_id: int,
        db: _orm.Session = _fastapi.Depends(_service.get_db)
):
    user = _service.get_user(db=db, user_id=user_id)
    if user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="User not found"
        )
    _service.delete_user(db=db, user_id=user_id)

    return {"message": f"Successfully deleted user with id:{user_id}"}


@app.post("/users/{user_id}/posts/", response_model=_schemas.Post)
def create_post(
        user_id: int,
        post: _schemas.PostCreate,
        db: _orm.Session = _fastapi.Depends(_service.get_db)
):
    user = _service.get_user(db=db, user_id=user_id)
    if user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="User not found"
        )

    return _service.create_post(db=db, post=post, user_id=user_id)


@app.get('/posts/', response_model=List[_schemas.Post])
def get_posts(
        skip: int = 0,
        limit: int = 0,
        db: _orm.Session = _fastapi.Depends(_service.get_db)
):
    return _service.get_posts(db=db, skip=skip, limit=limit)


@app.get("/posts/{post_id}", response_model=_schemas.Post)
def get_post(
        post_id: int,
        db: _orm.Session = _fastapi.Depends(_service.get_db)
):
    post = _service.get_post(db=db, post_id=post_id)
    if post is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="Post not found"
        )

    return post


@app.put("/posts/{post_id}", response_model=_schemas.Post)
def update_post(
        post_id: int,
        post: _schemas.PostCreate,
        db: _orm.Session = _fastapi.Depends(_service.get_db)
):
    db_post = _service.get_post(db=db, post_id=post_id)
    if db_post is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="Post not found"
        )

    return _service.update_post(db=db, post=post, post_id=post_id)


@app.delete("/posts/{post_id}")
def delete_post(
        post_id: int,
        db: _orm.Session = _fastapi.Depends(_service.get_db)
):
    post = _service.get_post(db=db, post_id=post_id)
    if post is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="Post not found"
        )
    _service.delete_post(db=db, post_id=post_id)

    return {"message": f"Successfully deleted post with id:{post_id}"}
