"""Reporting queries."""
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func , select
from app.schemas import TopBook
from app.models import Book , Order , OrderItem


def top_books(db: Session, limit: int = 5) -> List[TopBook]:
    """Best-selling books.

    Rules: copies_sold sums quantities over ``paid`` orders only; books with no sales are
    excluded; sorted by copies_sold desc, then title asc; at most ``limit`` rows.
    """
    copies_sold = func.sum(OrderItem.quantity).label("copies_sold")
    query=(
        select(Book.id , Book.title , copies_sold)
        .join(OrderItem , OrderItem.book_id == Book.id)
        .join(Order , Order.id == OrderItem.order_id)
        .where(Order.status == "paid")
        .group_by(Book.id , Book.title)
        .having(copies_sold>0)
        .order_by(copies_sold.desc() , Book.title.asc())
        .limit(limit)

    )

    rows = db.execute(query).all()

    return [
        TopBook(book_id=row.id , title=row.title , copies_sold=row.copies_sold)
        for row in rows
    ]
