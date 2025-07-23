from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, TIMESTAMP, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta

DATABASE_URL = "postgresql://postgres:123456789@localhost:5432/etsy-clone"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# -------- TABLE DEFINITIONS --------

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    full_name = Column(String)
    is_active = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    role = Column(String)

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    price = Column(Integer)
    discount_percentage = Column(Float)
    rating = Column(Float)
    stock = Column(Integer)
    brand = Column(String)
    thumbnail = Column(String)
    images = Column(String)
    is_published = Column(Boolean)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    category_id = Column(Integer, ForeignKey("categories.id"))

class Cart(Base):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    total_amount = Column(Float)

class CartItem(Base):
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True)
    card_id = Column(Integer)
    product_id = Column(Integer)
    quantity = Column(Float)
    subtotal = Column(Float)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    cart_id = Column(Integer)
    status = Column(String)
    total_amount = Column(Float)
    shipping_address = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    paid_at = Column(TIMESTAMP)

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    provider = Column(String)
    transaction_id = Column(String)
    status = Column(String)
    amount = Column(Float)
    currency = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    paid_at = Column(TIMESTAMP)
    payment_metadata = Column(JSON)

class Refund(Base):
    __tablename__ = 'refunds'
    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer)
    refund_amount = Column(Float)
    reason = Column(String)
    status = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    refunded_at = Column(TIMESTAMP)

class ShippingInfo(Base):
    __tablename__ = 'shipping_info'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    full_name = Column(String)
    phone = Column(String)
    address_line = Column(String)
    city = Column(String)
    district = Column(String)
    ward = Column(String)
    postal_code = Column(String)
    country = Column(String)
    shipping_method = Column(String)
    tracking_number = Column(String)
    shipping_status = Column(String)
    shipped_at = Column(TIMESTAMP)
    delivered_at = Column(TIMESTAMP)

class Coupon(Base):
    __tablename__ = 'coupons'
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    description = Column(String)
    discount_type = Column(String)
    discount_value = Column(Float)
    max_uses = Column(Integer)
    max_discount_amount = Column(Float)
    min_order_amount = Column(Float)
    valid_from = Column(TIMESTAMP)
    valid_to = Column(TIMESTAMP)
    is_active = Column(Boolean)

class OrderDiscount(Base):
    __tablename__ = 'order_discounts'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    coupon_id = Column(Integer)
    discount_amount = Column(Float)

class PaymentMethod(Base):
    __tablename__ = 'payment_methods'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    provider = Column(String)
    is_active = Column(Boolean)

class UserCard(Base):
    __tablename__ = 'user_cards'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    payment_method_id = Column(Integer)
    card_number = Column(String)
    card_holder_name = Column(String)
    expiry_month = Column(Integer)
    expiry_year = Column(Integer)
    last4 = Column(String)
    is_default = Column(Boolean)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

# -------- CREATE TABLES --------
Base.metadata.create_all(engine)

# -------- INSERT DEMO DATA --------
with SessionLocal() as session:
    session.add_all([
        User(username="john_doe", email="john@example.com", password="hashed123", full_name="John Doe", is_active="true", role="customer"),
        User(username="admin_user", email="admin@example.com", password="hashed456", full_name="Admin User", is_active="true", role="admin"),
        Category(name="Electronics"),
        Category(name="Books"),
        Coupon(code="WELCOME10", description="10% off", discount_type="percentage", discount_value=10.0,
            max_uses=100, max_discount_amount=50.0, min_order_amount=100.0,
            valid_from=datetime.utcnow(), valid_to=datetime.utcnow() + timedelta(days=30), is_active=True)
    ])
    session.commit()
