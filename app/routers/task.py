from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from models import Task, User
from schemas import CreateTask, UpdateTask
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify


router = APIRouter(prefix='/task', tags=['task'])

@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks

@router.get('/{task_id}')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        return {'status_code': status.HTTP_404_NOT_FOUND,
                'transaction': 'task was not found'}
    return task

@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], add_task: CreateTask, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    db.execute(insert(Task).values(
        title=add_task.title,
        content=add_task.content,
        user_id=add_task.user_id,
        priority=add_task.priority,
        slug=add_task.slug
    ))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'new task successfuly created'}

@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)], update_task: UpdateTask, task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='task not found'
        )
    db.execute(update(Task).where(Task.id == task_id).values(
        title=update_task.title,
        content=update_task.content,
        priority=update_task.priority
    ))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Successfuly updated task'
    }

@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='task not found'
        )
    db.execute(delete(Task).where(Task.id == task_id)) 
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Successfuly delete task'
    }