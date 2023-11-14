from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject

LABEL_FIELD = 'date_diff'


class CRUDCharityProject(CRUDBase):
    async def get_charity_project_id_by_name(
            self,
            charity_project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_charity_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name
            )
        )
        return db_charity_project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> list[dict[str, int]]:
        closed_charity_projects = await session.execute(
            select(
                [CharityProject.name,
                 (
                  func.julianday(CharityProject.close_date) -
                  func.julianday(CharityProject.create_date)
                  ).label(LABEL_FIELD),
                 CharityProject.description]
            ).where(CharityProject.fully_invested).order_by(LABEL_FIELD))
        return closed_charity_projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
