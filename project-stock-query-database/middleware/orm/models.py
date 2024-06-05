from sqlalchemy import Column, Integer, String, Numeric, Boolean, Date, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from .database import engine
from sqlalchemy.ext.declarative import declarative_base

# 創建基礎模型
Base = declarative_base()
# 定義數據庫模型


class Taiex(Base):
    __tablename__ = 'taiex'

    transaction_date = Column(Date, primary_key=True)
    open_price = Column(Numeric(10, 2), nullable=False)
    close_price = Column(Numeric(10, 2), nullable=False)
    high_price = Column(Numeric(10, 2), nullable=False)
    low_price = Column(Numeric(10, 2), nullable=False)


class DealDate(Base):
    __tablename__ = 'deal_date'

    transaction_date = Column(Date, primary_key=True)

    daily_deal = relationship("DailyDeal", back_populates='deal_date')
    legal_persons = relationship('LegalPerson', back_populates='deal_date')
    leader = relationship('Leader', back_populates='deal_date')


class Stock(Base):
    __tablename__ = 'stock'

    stock_id = Column(String(10), primary_key=True)
    stock_name = Column(String(30), nullable=False, unique=True)
    enabled = Column(Boolean, default=True)
    listed = Column(Boolean, nullable=False)

    daily_deal = relationship('DailyDeal', back_populates='stock')
    eps = relationship('Eps', back_populates='stock')
    legal_persons = relationship('LegalPerson', back_populates='stock')
    monthly_revenue = relationship('MonthlyRevenue', back_populates='stock')
    leader = relationship('Leader', back_populates='stock')


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

    stock = relationship('Stock', back_populates='daily_deal')
    deal_date = relationship("DealDate", back_populates='daily_deal')


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
    stock_id = Column(String(10), ForeignKey(
        'stock.stock_id'), primary_key=True)
    current_month_revenue = Column(Integer, nullable=False)
    previous_month_revenue = Column(Integer, nullable=False)
    previous_year_same_month_revenue = Column(Integer, nullable=False)
    month_over_month_revenue = Column(Numeric(precision=15, scale=3))
    year_over_year_revenue = Column(Numeric(precision=15, scale=3))
    current_year_cumulative_revenue = Column(Integer, nullable=False)
    previous_year_cumulative_revenue = Column(Integer, nullable=False)
    compare_cumulative_revenue = Column(Numeric(precision=15, scale=3))

    stock = relationship('Stock', back_populates='monthly_revenue')


class LegalPerson(Base):
    __tablename__ = 'legal_person'

    transaction_date = Column(Date, ForeignKey(
        'deal_date.transaction_date'), primary_key=True)
    stock_id = Column(String(10), ForeignKey(
        'stock.stock_id'), primary_key=True)
    stock_name = Column(String(30), nullable=False)
    foreign_investors = Column(Integer, nullable=False)  # 外資
    investment_trust = Column(Integer, nullable=False)  # 投信
    dealer = Column(Integer, nullable=False)  # 自營商

    stock = relationship('Stock', back_populates='legal_persons')
    deal_date = relationship("DealDate", back_populates='legal_persons')


class Leader(Base):
    __tablename__ = 'leader'
    transaction_date = Column(Date, ForeignKey(
        'deal_date.transaction_date'), primary_key=True)
    stock_id = Column(String(10), ForeignKey(
        'stock.stock_id'), primary_key=True)
    leader_difference = Column(Integer, nullable=False)  # 主力買賣超
    buyers_sellers_number_difference = Column(Integer, nullable=False)  # 買賣家數差
    five_day_concentration = Column(Numeric(10, 2), nullable=False)  # 五日集中度
    ten_day_concentration = Column(Numeric(10, 2), nullable=False)  # 十日集中度

    stock = relationship('Stock', back_populates='leader')
    deal_date = relationship("DealDate", back_populates='leader')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

    def __repr__(self):
        return f"<User(name='{self.name}', age={self.age})>"


# 創建表
Base.metadata.create_all(engine)
