from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

EXAMPLE_NAME = 'Проект №1'
EXAMPLE_DESCRIPTION = 'Описание Проекта №1'
EXAMPLE_FULL_AMOUNT = 500
MIN_LENGTH = 1
MAX_LENGTH = 100
DEFAUL_FULL_AMOUNT = 0
DEFAUL_INVESTED_AMOUNT = 0


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=MIN_LENGTH,
        max_length=MAX_LENGTH
    )
    description: Optional[str] = Field(
        None,
        min_length=MIN_LENGTH,
        max_length=MAX_LENGTH
    )
    full_amount: Optional[PositiveInt] = Field(
        DEFAUL_FULL_AMOUNT,
        example=EXAMPLE_FULL_AMOUNT
    )

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        min_length=MIN_LENGTH,
        max_length=MAX_LENGTH,
        example=EXAMPLE_NAME
    )
    description: str = Field(
        ...,
        min_length=MIN_LENGTH,
        example=EXAMPLE_DESCRIPTION
    )
    full_amount: PositiveInt = Field(
        ...,
        example=EXAMPLE_FULL_AMOUNT
    )
    invested_amount: int = Field(DEFAUL_INVESTED_AMOUNT)


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int = Field(DEFAUL_INVESTED_AMOUNT)
    fully_invested: bool = Field(False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    ...
