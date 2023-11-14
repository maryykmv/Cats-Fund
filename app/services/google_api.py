from datetime import datetime, timedelta

from aiogoogle import Aiogoogle
from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'
NOW_DATE_TIME = datetime.now().strftime(FORMAT)
LOCALE = 'ru_RU'
DEFAULT_SHEET_ID = 0
DEFAULT_SHEET_TITLE = 'Лист1'
DEFAULT_SHEET_TYPE = 'GRID'
ROW_COUNT = 50
COLUMN_COUNT = 5
SPREADSHEET_BODY = {
        'properties': {'title': f'Отчет от {NOW_DATE_TIME}',
                       'locale': LOCALE},
        'sheets': [{'properties': {'sheetType': DEFAULT_SHEET_TYPE,
                                   'sheetId': DEFAULT_SHEET_ID,
                                   'title': DEFAULT_SHEET_TITLE,
                                   'gridProperties': {
                                       'rowCount': ROW_COUNT,
                                       'columnCount': COLUMN_COUNT}}}]
    }
PERMISSION_TYPE = 'user'
PERMISSION_ROLE = 'writer'
PERMISSIONS_BODY = {'type': PERMISSION_TYPE,
                    'role': PERMISSION_ROLE,
                    'emailAddress': settings.email}
TABLE_VALUES = [
    ['Отчет от', NOW_DATE_TIME],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
DEFAILT_MAJOR_DIMENSION = 'ROWS'
UPDATE_BODY = {
        'majorDimension': DEFAILT_MAJOR_DIMENSION,
        'values': TABLE_VALUES
    }
RANGE = 'A1:C50'
VALUEIO = 'USER_ENTERED'
SHEET_SERVICE_NAME = 'sheets'
SHEET_SERVICE_VERSION = 'v4'
DRIVE_SERVICE_NAME = 'drive'
DRIVE_SERVICE_VERSION = 'v3'


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover(
        SHEET_SERVICE_NAME,
        SHEET_SERVICE_VERSION
    )
    spreadsheet_body = SPREADSHEET_BODY
    return (await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)))['spreadsheetId']


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = PERMISSIONS_BODY
    service = await wrapper_services.discover(
        DRIVE_SERVICE_NAME,
        DRIVE_SERVICE_VERSION
    )
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover(
        SHEET_SERVICE_NAME,
        SHEET_SERVICE_VERSION
    )
    for charity_project in charity_projects:
        new_row = [
            charity_project['name'],
            str(timedelta(days=charity_project['date_diff'])),
            charity_project['description']
        ]
        TABLE_VALUES.append(new_row)
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=RANGE,
            valueInputOption=VALUEIO,
            json=UPDATE_BODY
        )
    )
