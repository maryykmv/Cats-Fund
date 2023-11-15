import copy
from datetime import datetime, timedelta

from aiogoogle import Aiogoogle
from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'
DEFAILT_MAJOR_DIMENSION = 'ROWS'
MAX_ROWS_COUNT = 100
MAX_COLUMNS_COUNT = 11
SPREADSHEET_BODY = dict(
    properties=dict(
        title='Отчет от',
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=MAX_ROWS_COUNT,
            columnCount=MAX_COLUMNS_COUNT,
        )
    ))]
)
TABLE_VALUES = [
    ['Отчет от', ],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
MESSAGE_VALUES_ERROR = (
    'Количество строк = {rows_count} и столбцов = {columns_count} '
    f'превышают {MAX_ROWS_COUNT}, {MAX_COLUMNS_COUNT}'
)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover(
        'sheets',
        'v4'
    )
    spreadsheet_body = copy.deepcopy(SPREADSHEET_BODY)
    spreadsheet_body['properties']['title'] += datetime.now().strftime(FORMAT)
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body))
    return response['spreadsheetId'], response['spreadsheetUrl']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover(
        'drive',
        'v3'
    )
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover(
        'sheets',
        'v4'
    )
    table_values = copy.deepcopy(TABLE_VALUES)
    table_values[0].append(datetime.now().strftime(FORMAT))
    table_values = [*table_values,
                    *[
                        [
                            charity_project['name'],
                            str(timedelta(days=charity_project['date_diff'])),
                            charity_project['description']
                        ]
                        for charity_project in charity_projects
                    ]
                    ]
    columns_count = max(map(len, table_values))
    rows_count = len(table_values)
    if (
        MAX_ROWS_COUNT < rows_count or
        MAX_COLUMNS_COUNT < columns_count
    ):
        raise ValueError(
            MESSAGE_VALUES_ERROR.format(
                rows_count=rows_count,
                columns_count=columns_count
            )
        )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{rows_count}C{columns_count}',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': DEFAILT_MAJOR_DIMENSION,
                'values': table_values
            }
        )
    )
