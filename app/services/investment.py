from datetime import datetime
from typing import List

from app.models import InvestmentModel


async def investing(
    target: InvestmentModel,
    sources: List[InvestmentModel],
) -> List[InvestmentModel]:
    updated = []
    for source in sources:
        amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount)
        if amount == 0:
            break
        for object in (target, source):
            object.invested_amount += amount
            if object.full_amount == object.invested_amount:
                object.fully_invested = True
                object.close_date = datetime.now()
        updated.append(object)
    return updated
