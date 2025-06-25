from fastapi import FastAPI
from app.routes import user_routes
from app.models import user_model
from app.database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()
user_model.Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router)
