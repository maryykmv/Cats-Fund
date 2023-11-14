from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

EXAMPLE_FULL_AMOUNT = 100
EXAMPLE_COMMENTARY = 'Комментарий'
DEFAUL_INVESTED_AMOUNT = 0


class DonationBase(BaseModel):
    full_amount: PositiveInt = Field(
        ...,
        example=EXAMPLE_FULL_AMOUNT
    )
    comment: Optional[str] = Field(
        None,
        example=EXAMPLE_COMMENTARY
    )

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationCreate):
    user_id: int
    invested_amount: int = Field(DEFAUL_INVESTED_AMOUNT)
    fully_invested: bool
    close_date: Optional[datetime]
