from fastapi import FastAPI
from routers import task, user
from backend.db import Base, engine



app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)

app.include_router(user.router)
app.include_router(task.router)

Base.metadata.create_all(bind=engine)

@app.get('/')
async def welcome():
    return {'message': 'Welcome to Taskmanager'}