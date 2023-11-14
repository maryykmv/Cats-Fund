from datetime import datetime


from sqlalchemy import Column, Boolean, DateTime, Integer, CheckConstraint

from app.core.db import Base


class InvestmentModel(Base):
    __abstract__ = True

    __table_args__ = (
        CheckConstraint('full_amount>0', name='full_amount_check'),
        CheckConstraint(
            'invested_amount<=full_amount', name='invested_amount_check'),
        CheckConstraint('invested_amount>=0', name='invested_amount_check'),
    )

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    def __init__(
            self, name=None, description=None, full_amount=0,
            invested_amount=0, comment=None, user_id=0):
        self.name = name
        self.description = description
        self.full_amount = full_amount
        self.invested_amount = invested_amount
        self.user_id = user_id
        self.comment = comment

    def __repr__(self):
        return (
            f'full_amount {self.full_amount}, '
            f'invested_amount {self.invested_amount}, '
            f'create_date {self.create_date}, '
            f'close_date {self.close_date}'
        )
