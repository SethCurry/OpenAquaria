import typing

from fastapi import FastAPI
from sqlalchemy.orm import joinedload, sessionmaker
from sqlalchemy import create_engine
import uvicorn

from openaquaria.hub import db

engine = create_engine("sqlite:///hub.db")
db.Base.metadata.create_all(engine)

app = FastAPI()
Session = sessionmaker(engine)


@app.get("/v1/kingdoms")
def list_kingdoms():
    with Session() as session:
        return session.query(db.Kingdom).all()


@app.get("/v1/phylums")
def list_phylums():
    with Session() as session:
        return session.query(db.Phylum).all()


@app.get("/v1/classes")
def list_classes():
    with Session() as session:
        return session.query(db.Class).all()


@app.get("/v1/orders")
def list_orders():
    with Session() as session:
        return session.query(db.Order).all()


@app.get("/v1/families")
def list_families():
    with Session() as session:
        return session.query(db.Family).all()


@app.get("/v1/genuses")
def list_genuses():
    with Session() as session:
        return session.query(db.Genus).all()


@app.get("/v1/species")
def list_species(name: typing.Optional[str] = None):
    with Session() as session:
        query = session.query(db.Species).options(joinedload(db.Species.aquatic_animal))

        if name is not None:
            query = query.filter(db.Species.name == name)

        return query.all()


@app.get("/v1/aquatic_animals")
def list_aquatic_animals():
    with Session() as session:
        return session.query(db.AquaticAnimal).all()


uvicorn.run(app, host="0.0.0.0", port=8888)
