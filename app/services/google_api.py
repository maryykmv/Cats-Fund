from datetime import datetime, timedelta

from aiogoogle import Aiogoogle
from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'
PERMISSION_TYPE = 'user'
PERMISSION_ROLE = 'writer'
DEFAILT_MAJOR_DIMENSION = 'ROWS'
DEFAULT_ROWS_COUNT = 100
DEFAULT_COLUMNS_COUNT = 11
VALUEIO = 'USER_ENTERED'
SHEET_SERVICE_NAME = 'sheets'
SHEET_SERVICE_VERSION = 'v4'
DRIVE_SERVICE_NAME = 'drive'
DRIVE_SERVICE_VERSION = 'v3'
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
            rowCount=DEFAULT_ROWS_COUNT,
            columnCount=DEFAULT_COLUMNS_COUNT,
        )
    ))]
)
TABLE_VALUES = [
    ['Отчет от', {}],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
MESSAGE_VALUES_ERROR = (
    f'Количество строк = {{rows_count}} и столбцов = {{colums_count}} '
    f'превышают {DEFAULT_ROWS_COUNT}, {DEFAULT_COLUMNS_COUNT}'
)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover(
        SHEET_SERVICE_NAME,
        SHEET_SERVICE_VERSION
    )
    spreadsheet_body = SPREADSHEET_BODY.copy()
    spreadsheet_body['properties']['title'] += now_date_time
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body))
    return response['spreadsheetId'], response['spreadsheetUrl']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': PERMISSION_TYPE,
        'role': PERMISSION_ROLE,
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover(
        DRIVE_SERVICE_NAME,
        DRIVE_SERVICE_VERSION
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
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover(
        SHEET_SERVICE_NAME,
        SHEET_SERVICE_VERSION
    )
    table_values = TABLE_VALUES.copy()
    table_values[0].append(now_date_time)
    table_values = [*table_values,
                    *[list(map(str,
                               [charity_project['name'],
                                timedelta(
                                    days=charity_project['date_diff']
                                ),
                                charity_project['description']]))
                        for charity_project in charity_projects]
                    ]
    columns_count = max(map(len, table_values))
    rows_count = len(table_values)
    if (
        DEFAULT_ROWS_COUNT < rows_count or
        DEFAULT_COLUMNS_COUNT < columns_count
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
            valueInputOption=VALUEIO,
            json={
                'majorDimension': DEFAILT_MAJOR_DIMENSION,
                'values': table_values
            }
        )
    )
