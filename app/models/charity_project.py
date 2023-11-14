from sqlalchemy import Column, String, Text

from app.models.basic import InvestmentModel


class CharityProject(InvestmentModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'CharityProject(name {self.name}, '
            f'{super().__repr__()})'
        )
