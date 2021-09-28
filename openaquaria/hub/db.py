from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Integer, ForeignKey, Float

Base = declarative_base()

"""
Kingdom
Subkingdom
Phylum
Class
Order
Family
Genus
Species
"""


class AquaticAnimal(Base):
    __tablename__ = "aquatic_animal"

    id = Column(Integer, primary_key=True)
    species = relationship("Species", back_populates="aquatic_animal")

    minimum_temperature = Column(Float)
    maximum_temperature = Column(Float)


class Species(Base):
    __tablename__ = "species"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    aquatic_animal_id = Column(Integer, ForeignKey("aquatic_animal.id"))
    aquatic_animal = relationship("AquaticAnimal", back_populates="species")

    genus_id = Column(Integer, ForeignKey("genus.id"))
    genus = relationship("Genus", back_populates="species")


class Genus(Base):
    __tablename__ = "genus"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    species = relationship("Species", order_by=Species.id, back_populates="genus")

    family_id = Column(Integer, ForeignKey("family.id"))
    family = relationship("Family", back_populates="genuses")


class Family(Base):
    __tablename__ = "family"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    genuses = relationship("Genus", order_by=Genus.id, back_populates="family")

    order_id = Column(Integer, ForeignKey("order_.id"))
    order = relationship("Order", back_populates="families")


class Order(Base):
    __tablename__ = "order_"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    families = relationship("Family", order_by=Family.id, back_populates="order")

    class_id = Column(Integer, ForeignKey("class_.id"))
    class_ = relationship("Class", back_populates="orders")


class Class(Base):
    __tablename__ = "class_"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    orders = relationship("Order", order_by=Order.id, back_populates="class_")

    phylum_id = Column(Integer, ForeignKey("phylum.id"))
    phylum = relationship("Phylum", back_populates="classes")


class Phylum(Base):
    __tablename__ = "phylum"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    classes = relationship("Class", order_by=Class.id, back_populates="phylum")

    kingdom_id = Column(Integer, ForeignKey("kingdom.id"))
    kingdom = relationship("Kingdom", back_populates="phylums")


class Kingdom(Base):
    __tablename__ = "kingdom"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    phylums = relationship("Phylum", order_by=Phylum.id, back_populates="kingdom")
