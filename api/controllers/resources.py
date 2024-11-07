from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas


def create_recipe(db: Session, recipe_data):
    db_recipe = models.Recipe(
        sandwich_id=recipe_data["sandwich_id"],
        resource_id=recipe_data["resource_id"],
        amount=recipe_data["amount"]
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def read_all(db: Session):
    return db.query(models.Recipe).all()

def read_one(db: Session, resource_id):
    return db.query(models.Recipe).filter(models.Recipe.id == resource_id).first()

def update(db: Session, resource_id, resource):
    db_resource = db.query(models.Recipe).filter(models.Recipe.id == resource_id)
    update_data = resource.model_dump(exclude_unset=True)
    db_resource.update(update_data, synchronize_session=False)
    db.commit()
    return db_resource.first()

def delete(db: Session, resource_id):
    db_resource = db.query(models.Recipe).filter(models.Recipe.id == resource_id)
    db_resource.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)