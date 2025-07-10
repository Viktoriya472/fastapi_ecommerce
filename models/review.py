from app.backend.db import Base
from sqlalchemy import Column, Integer, Float, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    comment = Column(String, nullable=True)
    comment_date = Column(Date, default=datetime.now())
    grade = Column(Float)
    is_active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='review')
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship('Product', back_populates='review')
