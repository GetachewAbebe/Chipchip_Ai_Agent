from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum as SqlEnum
from sqlalchemy.orm import relationship, declarative_base
import enum
import datetime

Base = declarative_base()

# Enums for customer segmentation and registration channel
class SegmentEnum(enum.Enum):
    student = "Student"
    professional = "Working Professional"
    homemaker = "Homemaker"

class ChannelEnum(enum.Enum):
    organic = "Organic"
    referral = "Referral"
    paid_ad = "Paid Ad"
    influencer = "Influencer"

# -------------------------------
# Customer Table
# -------------------------------
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    signup_date = Column(DateTime, default=datetime.datetime.utcnow)
    segment = Column(SqlEnum(SegmentEnum), default=SegmentEnum.student)
    registration_channel = Column(SqlEnum(ChannelEnum), default=ChannelEnum.organic)

    orders = relationship("Order", back_populates="customer")
    group_leader_map = relationship("CustomerGroupLeaderMap", back_populates="customer", uselist=False)

# -------------------------------
# Group Leader Table
# -------------------------------
class GroupLeader(Base):
    __tablename__ = "group_leaders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    joined_date = Column(DateTime, default=datetime.datetime.utcnow)

    customers = relationship("CustomerGroupLeaderMap", back_populates="group_leader")

# -------------------------------
# Many-to-One Mapping Table
# -------------------------------
class CustomerGroupLeaderMap(Base):
    __tablename__ = "customer_group_leader_map"

    customer_id = Column(Integer, ForeignKey("customers.id"), primary_key=True)
    group_leader_id = Column(Integer, ForeignKey("group_leaders.id"), primary_key=True)

    customer = relationship("Customer", back_populates="group_leader_map")
    group_leader = relationship("GroupLeader", back_populates="customers")

# -------------------------------
# Product Table
# -------------------------------
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    type = Column(String, nullable=False)  # e.g., "fresh produce", "stationery"
    price = Column(Float, nullable=False)

    order_items = relationship("OrderItem", back_populates="product")

# -------------------------------
# Order Table
# -------------------------------
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    order_datetime = Column(DateTime, default=datetime.datetime.utcnow)
    total_amount = Column(Float, nullable=False)

    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

# -------------------------------
# OrderItem Table
# -------------------------------
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
