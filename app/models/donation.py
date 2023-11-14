from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.basic import InvestmentModel


class Donation(InvestmentModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return (
            f'Donation(user_id {self.user_id}, '
            f'comment {self.comment}, '
            f'{super().__repr__()})'
        )
