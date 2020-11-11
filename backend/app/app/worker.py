from typing import Generator

from raven import Client
import subprocess, pickle

from app import crud, models, schemas
from app.core.celery_app import celery_app
from app.core.config import settings
from app.db.session import SessionLocal

client_sentry = Client(settings.SENTRY_DSN)


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"

@celery_app.task(acks_late=True)
def test_alphapy(id: int) -> str:
    db = SessionLocal()
    item = crud.item.get(db=db, id=id)
    #result = subprocess.run(["mflow"])
    binary_data = open("./model/model_20201027.pkl",'rb')
    model = pickle.load(binary_data)
    item_in = schemas.ItemUpdate(pickled_model=model)
    crud.item.update(db=db, db_obj=item, obj_in=item_in)
    db.close()
    return f"alphapy test task return {item.id}"