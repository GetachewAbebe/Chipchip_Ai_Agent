from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Create the declarative base
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    channel = Column(String)
    acquisition_campaign = Column(String)
    signup_date = Column(DateTime)
    segment = Column(String)
    created_at = Column(DateTime)

    # Relationships
    orders = relationship("Order", back_populates="user")
    group_leader = relationship("GroupLeader", back_populates="user")

class GroupLeader(Base):
    __tablename__ = 'group_leaders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime)

    # Relationships
    user = relationship("User", back_populates="group_leader")
    orders = relationship("Order", back_populates="group_leader")

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String)
    price = Column(Float)
    is_fresh_produce = Column(Boolean)
    created_at = Column(DateTime)

    # Relationships
    order_items = relationship("OrderItem", back_populates="product")

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    group_leader_id = Column(Integer, ForeignKey('group_leaders.id'))
    timestamp = Column(DateTime)
    order_total_value = Column(Float)
    is_first_order = Column(Boolean)
    created_at = Column(DateTime)

    # Relationships
    user = relationship("User", back_populates="orders")
    group_leader = relationship("GroupLeader", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    created_at = Column(DateTime)

    # Relationships
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
