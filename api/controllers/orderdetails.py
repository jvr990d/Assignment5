from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import models, schemas


def create_order_detail(db: Session, order_detail_data: schemas.OrderDetailCreate):
    # Creating a new OrderDetail instance with required fields
    db_order_detail = models.OrderDetail(
        order_id=order_detail_data.order_id,
        sandwich_id=order_detail_data.sandwich_id,
        amount=order_detail_data.amount
    )
    db.add(db_order_detail)
    db.commit()
    db.refresh(db_order_detail)
    return db_order_detail


def read_all_order_details(db: Session):
    return db.query(models.OrderDetail).all()


def read_one_order_detail(db: Session, order_detail_id: int):
    order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id).first()
    if order_detail is None:
        raise HTTPException(status_code=404, detail="OrderDetail not found")
    return order_detail


def update_order_detail(db: Session, order_detail_id: int, order_detail_data: schemas.OrderDetailUpdate):
    db_order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id)
    if not db_order_detail.first():
        raise HTTPException(status_code=404, detail="OrderDetail not found")

    update_data = order_detail_data.model_dump(exclude_unset=True)
    db_order_detail.update(update_data, synchronize_session=False)
    db.commit()
    return db_order_detail.first()


def delete_order_detail(db: Session, order_detail_id: int):
    db_order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id)
    if not db_order_detail.first():
        raise HTTPException(status_code=404, detail="OrderDetail not found")

    db_order_detail.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
