from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from models import User
from schemas import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users

@router.get('/{user_id}')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(user_id == User.id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )
    return user

@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], add_user: CreateUser):
    db.execute(insert(User).values(
        username=add_user.username,
        firstname=add_user.firstname,
        lastname=add_user.lastname,
        age=add_user.age,
        slug=add_user.slug
    ))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], update_user: UpdateUser, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )
    db.execute(update(User).where(User.id == user_id).values(
        firstname=update_user.firstname,
        lastname=update_user.lastname,
        age=update_user.age
    ))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Successful'
    }

@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )
    db.execute(delete(User).where(User.id == user_id)) 
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Successful delete user'
    }