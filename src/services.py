import sqlalchemy.orm as _orm

import database as _database
import models as _model
import schemas as _schema
import datetime as _dt


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_by_email(db: _orm.Session, email: str):
    return db.query(_model.User).filter(_model.User.email == email).first()


def create_user(db: _orm.Session, user: _schema.UserCreate):
    fake_hashed_password = user.password + "123"
    db_user = _model.User(
        email=user.email,
        hashed_password=fake_hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: _orm.Session, skip: int, limit: int):
    return db.query(_model.User).offset(skip).limit(limit).all()


def get_user(db: _orm.Session, user_id: int):
    return db.query(_model.User).filter(_model.User.id == user_id).first()


def delete_user(db: _orm.Session, user_id: int):
    db.query(_model.User).filter(_model.User.id == user_id).delete()
    db.commit()


def create_post(db: _orm.Session, post: _schema.PostCreate, user_id: int):
    post = _model.Post(**post.dict(), owner_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_posts(db: _orm.Session, skip: int, limit: int):
    return db.query(_model.Post).offset(skip).limit(limit).all()


def get_post(db: _orm.Session, post_id: int):
    return db.query(_model.Post).filter(_model.Post.id == post_id).first()


def update_post(db: _orm.Session, post: _schema.PostCreate, post_id: int):
    db_post = get_post(db=db, post_id=post_id)
    db_post.title = post.title
    db_post.content = post.content
    db_post.date_last_updated = _dt.datetime.now()
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: _orm.Session, post_id: int):
    db.query(_model.Post).filter(_model.Post.id == post_id).delete()
    db.commit()
