from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship, declarative_base
import enum
import datetime

Base = declarative_base()

class SegmentEnum(enum.Enum):
    student = "Student"
    professional = "Working Professional"
    homemaker = "Homemaker"

class ChannelEnum(enum.Enum):
    organic = "Organic"
    referral = "Referral"
    paid_ad = "Paid Ad"
    influencer = "Influencer"

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    signup_date = Column(DateTime, default=datetime.datetime.utcnow)
    segment = Column(Enum(SegmentEnum), default=SegmentEnum.student)
    registration_channel = Column(Enum(ChannelEnum), default=ChannelEnum.organic)

    orders = relationship("Order", back_populates="customer")
    group_leader = relationship("CustomerGroupLeaderMap", back_populates="customer", uselist=False)


class GroupLeader(Base):
    __tablename__ = "group_leaders"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    joined_date = Column(DateTime, default=datetime.datetime.utcnow)

    customers = relationship("CustomerGroupLeaderMap", back_populates="group_leader")


class CustomerGroupLeaderMap(Base):
    __tablename__ = "customer_group_leader_map"
    customer_id = Column(Integer, ForeignKey("customers.id"), primary_key=True)
    group_leader_id = Column(Integer, ForeignKey("group_leaders.id"), primary_key=True)

    customer = relationship("Customer", back_populates="group_leader")
    group_leader = relationship("GroupLeader", back_populates="customers")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category = Column(String)
    type = Column(String)  # e.g., "fresh produce", "stationery"
    price = Column(Float)

    order_items = relationship("OrderItem", back_populates="product")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    order_datetime = Column(DateTime, default=datetime.datetime.utcnow)
    total_amount = Column(Float)

    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
