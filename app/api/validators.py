from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


MESSAGE_PROJECT_EXISTS = 'Проект с таким именем уже существует!'
MESSAGE_PROJECT_NOT_FOUND = 'Проект не найден.'
MESSAGE_PROJECT_INVESTED_AMOUNT = 'Требуемая сумма проекта меньше внесенной.'
MESSAGE_PROJECT_NOT_REMOVE = (
    'В проект были внесены средства, не подлежит удалению!')
MESSAGE_PROJECT_NOT_EDIT_CLOCSED = 'Закрытый проект нельзя редактировать!'


async def check_charity_project_name_duplicate(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    charity_project_id = (
        await charity_project_crud.get_charity_project_id_by_name(
            charity_project_name, session
        )
    )
    if charity_project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=MESSAGE_PROJECT_EXISTS,
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        charity_project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=MESSAGE_PROJECT_NOT_FOUND
        )
    return charity_project


def check_charity_project_invested_amount(
        charity_project: CharityProject,
        new_invested_amount: int
):
    if charity_project.invested_amount > new_invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=MESSAGE_PROJECT_INVESTED_AMOUNT
        )


def check_charity_project_invested_amount_exists(
        charity_project: CharityProject
):
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=MESSAGE_PROJECT_NOT_REMOVE
        )


def check_charity_project_closed(charity_project: CharityProject):
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=MESSAGE_PROJECT_NOT_EDIT_CLOCSED
        )
