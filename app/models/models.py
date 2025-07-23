from sqlalchemy import JSON, Boolean, Column, Integer, String, ForeignKey, Float, ARRAY, Enum
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_active = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)
    role = Column(Enum("admin", "user", name="user_roles"), nullable=False, server_default="user")
    # Relationship
    carts = relationship("Cart", back_populates="user")
    orders = relationship("Order", back_populates="user")
    user_cards = relationship("UserCard", back_populates="user")

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)
    total_amount = Column(Float, nullable=False)
    # Relationship
    user = relationship("User", back_populates="carts")
    cart_items = relationship("CartItem", back_populates="cart")
    orders = relationship("Order", back_populates="cart")

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)
    # Relationship
    cart = relationship("Cart", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    # Relationship
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    discount_percentage = Column(Float, nullable=False)
    rating = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    brand = Column(String, nullable=False)
    thumbnail = Column(String, nullable=False)
    images = Column(ARRAY(String), nullable=False)
    is_published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    # Relationship
    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False)  # 'pending', 'paid', etc.
    total_amount = Column(Float, nullable=False)
    shipping_address = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))
    paid_at = Column(TIMESTAMP(timezone=True))

    user = relationship("User", back_populates="orders")
    cart = relationship("Cart", back_populates="orders")
    payments = relationship("Payment", back_populates="order")
    shipping_info = relationship("ShippingInfo", back_populates="order", uselist=False)
    order_discounts = relationship("OrderDiscount", back_populates="order")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    provider = Column(String)  # Stripe, VNPay, Momo, etc.
    transaction_id = Column(String)
    status = Column(String)  # 'pending', 'success', 'failed'
    amount = Column(Float)
    currency = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))
    paid_at = Column(TIMESTAMP(timezone=True))
    payment_metadata = Column(JSON)

    order = relationship("Order", back_populates="payments")
    refunds = relationship("Refund", back_populates="payment")

class Refund(Base):
    __tablename__ = "refunds"

    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("payments.id", ondelete="CASCADE"), nullable=False)
    refund_amount = Column(Float)
    reason = Column(String)
    status = Column(String)  # 'pending', 'success', 'failed'
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))
    refunded_at = Column(TIMESTAMP(timezone=True))

    payment = relationship("Payment", back_populates="refunds")

class ShippingInfo(Base):
    __tablename__ = "shipping_info"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
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
    shipping_status = Column(String)  # 'pending', 'shipped', etc.
    shipped_at = Column(TIMESTAMP(timezone=True))
    delivered_at = Column(TIMESTAMP(timezone=True))

    order = relationship("Order", back_populates="shipping_info")

class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    description = Column(String)
    discount_type = Column(String)  # 'percentage', 'fixed'
    discount_value = Column(Float)
    max_uses = Column(Integer)
    max_discount_amount = Column(Float)
    min_order_amount = Column(Float)
    valid_from = Column(TIMESTAMP(timezone=True))
    valid_to = Column(TIMESTAMP(timezone=True))
    is_active = Column(Boolean)

    order_discounts = relationship("OrderDiscount", back_populates="coupon")

class OrderDiscount(Base):
    __tablename__ = "order_discounts"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    coupon_id = Column(Integer, ForeignKey("coupons.id", ondelete="CASCADE"), nullable=False)
    discount_amount = Column(Float)

    order = relationship("Order", back_populates="order_discounts")
    coupon = relationship("Coupon", back_populates="order_discounts")

class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True)
    name = Column(String)  # Credit Card, VNPay, etc.
    provider = Column(String)
    is_active = Column(Boolean)

    user_cards = relationship("UserCard", back_populates="payment_method")

class UserCard(Base):
    __tablename__ = "user_cards"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    payment_method_id = Column(Integer, ForeignKey("payment_methods.id", ondelete="CASCADE"), nullable=False)
    card_number = Column(String)
    card_holder_name = Column(String)
    expiry_month = Column(Integer)
    expiry_year = Column(Integer)
    last4 = Column(String)
    is_default = Column(Boolean)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))

    user = relationship("User", back_populates="user_cards")
    payment_method = relationship("PaymentMethod", back_populates="user_cards")