from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from assistant_budget.src.database import Base, engine, SessionLocal
from assistant_budget.src import models

app = FastAPI()

# создаём все таблицы, если их ещё нет
Base.metadata.create_all(bind=engine)

# dependency для работы с БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return {"categories": [c.name for c in categories]}