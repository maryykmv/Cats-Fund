from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_name_duplicate, check_charity_project_exists,
    check_charity_project_closed, check_charity_project_invested_amount,
    check_charity_project_invested_amount_exists)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services.investment import investing

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров. Создавать проекты."""
    await check_charity_project_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        charity_project, session, False)
    session.add_all(
        await investing(new_charity_project,
                        await donation_crud.get_not_fully_invested(session)))
    await session.commit()
    await session.refresh(new_charity_project)
    return new_charity_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров. Изменять название и описание существующего
    проекта, устанавливать для него новую требуемую сумму
    (но не меньше уже внесённой)."""
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    check_charity_project_closed(charity_project)
    if obj_in.name:
        await check_charity_project_name_duplicate(obj_in.name, session)
    if obj_in.full_amount:
        check_charity_project_invested_amount(
            charity_project,
            obj_in.full_amount
        )
    update_charity_project = await charity_project_crud.update(
        charity_project, obj_in, session, False
    )
    session.add_all(
        await investing(
            update_charity_project,
            (await donation_crud.get_not_fully_invested(session))))
    await session.commit()
    await session.refresh(charity_project)
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров. Удалять проекты,
    в которые не было внесено средств"""
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    check_charity_project_invested_amount_exists(charity_project)
    return await charity_project_crud.remove(
        charity_project, session
    )
