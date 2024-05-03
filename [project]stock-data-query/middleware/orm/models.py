from sqlalchemy import Column, Integer, String, Numeric, Boolean, Date, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from .database import engine
from sqlalchemy.ext.declarative import declarative_base

# 創建基礎模型
Base = declarative_base()


class DealDate(Base):
    __tablename__ = 'deal_date'

    transaction_date = Column(Date, primary_key=True)


class Stock(Base):
    __tablename__ = 'stock'

    stock_id = Column(String(10), primary_key=True)
    stock_name = Column(String(30), nullable=False, unique=True)
    enabled = Column(Boolean, default=True)

    daily_deals = relationship('DailyDeal', back_populates='stock')
    eps = relationship('Eps', back_populates='stock')
    legal_persons = relationship('LegalPerson', back_populates='stock')


class DailyDeal(Base):
    __tablename__ = 'daily_deal'

    transaction_date = Column(Date, ForeignKey(
        'deal_date.transaction_date'), primary_key=True)
    stock_id = Column(String(10), ForeignKey(
        'stock.stock_id'), primary_key=True)
    stock_name = Column(String(30), nullable=False)
    volume = Column(Integer, nullable=False)
    open_price = Column(Numeric(10, 2), nullable=False)
    close_price = Column(Numeric(10, 2), nullable=False)
    high_price = Column(Numeric(10, 2), nullable=False)
    low_price = Column(Numeric(10, 2), nullable=False)

    stock = relationship('Stock', back_populates='daily_deals')


class Eps(Base):
    __tablename__ = 'eps'

    season = Column(String(10), primary_key=True)
    stock_id = Column(String(10), ForeignKey(
        'stock.stock_id'), primary_key=True)
    stock_name = Column(String(30), nullable=False)
    eps_data = Column(Numeric(10, 3), nullable=False)

    stock = relationship('Stock', back_populates='eps')


class MonthlyRevenue(Base):
    __tablename__ = 'monthly_revenue'

    year = Column(Integer, primary_key=True)
    month = Column(Integer, primary_key=True)
    stock_id = Column(String(10), primary_key=True)
    current_month_revenue = Column(BigInteger)
    previous_month_revenue = Column(BigInteger)
    previous_year_same_month_revenue = Column(BigInteger)
    month_over_month_revenue = Column(Numeric(precision=15, scale=3))
    year_over_year_revenue = Column(Numeric(precision=15, scale=3))
    current_year_cumulative_revenue = Column(BigInteger)
    previous_year_cumulative_revenue = Column(BigInteger)
    compare_cumulative_revenue = Column(Numeric(precision=15, scale=3))


class LegalPerson(Base):
    __tablename__ = 'legal_person'

    transaction_date = Column(Date, ForeignKey(
        'deal_date.transaction_date'), primary_key=True)
    stock_id = Column(String(10), ForeignKey(
        'stock.stock_id'), primary_key=True)
    stock_name = Column(String(30), nullable=False)
    foreign_investors = Column(Integer, nullable=False)
    investment_trust = Column(Integer, nullable=False)
    dealer = Column(Integer, nullable=False)

    stock = relationship('Stock', back_populates='legal_persons')

# 定義數據庫模型


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

    def __repr__(self):
        return f"<User(name='{self.name}', age={self.age})>"


# 創建表
Base.metadata.create_all(engine)
