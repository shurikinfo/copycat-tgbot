import logging

from googleapiclient.discovery import build
from googleapiclient.errors import Error as googleError

from copycat_tgbot.cache import RedisCache
from copycat_tgbot.constants import GOOGLE_SHEETS_STATISTICS_TITLE
from copycat_tgbot.error import GoogleError
from copycat_tgbot.utils import generate_excel_range, sheet_to_dict

logger = logging.getLogger(__name__)


class GoogleSheetsService:
    """Сервис для работы с Google Sheets"""

    SERVICE_NAME = "sheets"

    def __init__(self, credentials, cache: RedisCache):
        self.service = build("sheets", "v4", credentials=credentials)
        self.spreadsheet_id = None
        self.cache = cache

    def create_sheets(self, file_name: str, sheets: dict):
        """Создание нового документа Spreadsheet"""
        spreadsheet_details = {
            "properties": {"title": file_name},
            "sheets": [
                {
                    "properties": {"title": title},
                    "data": [
                        {
                            "rowData": [
                                {
                                    "values": [
                                        {"userEnteredValue": {"stringValue": column}}
                                        for column in columns
                                    ]
                                }
                            ]
                        }
                    ],
                }
                for title, columns in sheets.items()
            ],
        }
        try:
            spreadsheet = (
                self.service.spreadsheets()
                .create(body=spreadsheet_details, fields="spreadsheetId")
                .execute()
            )
            spreadsheet_id = spreadsheet.get("spreadsheetId")
        except googleError as e:
            logger.debug(e)
            raise GoogleError("Ошибка при создании Spreadsheet-документа")

        logger.info(
            f"Ссылка на новую таблицу: https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
        )
        return spreadsheet_id

    def append_to_sheet(self, values: list | list[list], sheet_title: str):
        """Добавление информации в лист"""
        try:
            appended = (
                self.service.spreadsheets()
                .values()
                .append(
                    spreadsheetId=self.spreadsheet_id,
                    range=f"{sheet_title}!A1:{generate_excel_range(len(values))}1",
                    valueInputOption="USER_ENTERED",
                    body={"values": values},
                )
                .execute()
            )
            logger.info(appended)

            self.cache.invalidate_cache(
                "get_values",
                spreadsheet_id=self.spreadsheet_id,
                sheet_title=sheet_title,
            )

            return appended
        except googleError as e:
            logger.debug(e)
            raise GoogleError(
                f"Ошибка при добавлении информации в лист: {self.spreadsheet_id}:{sheet_title}"
            )

    def create_statistics_sheet(
        self,
        sheets_titles: list[str],
        sheet_title: str = GOOGLE_SHEETS_STATISTICS_TITLE,
    ) -> None:
        counter_rows_titles = [
            f"{sheet}_rows" for sheet in sheets_titles if sheet != sheet_title
        ]
        counter_rows_function = [
            f"=COUNTA({sheet}!B:B)" for sheet in sheets_titles if sheet != sheet_title
        ]

        result = self.append_to_sheet(
            values=[
                counter_rows_titles,
                counter_rows_function,
            ],
            sheet_title=sheet_title,
        )
        if result:
            logger.info(
                f"Добавлена страница статистики {self.spreadsheet_id}:{sheet_title}"
            )

    def get_values_cached(self, spreadsheet_id: str, sheet_title: str):
        @self.cache.cached()
        def get_values(spreadsheet_id: str, sheet_title: str):
            try:
                return sheet_to_dict(
                    self.service.spreadsheets()
                    .values()
                    .get(spreadsheetId=spreadsheet_id, range=sheet_title)
                    .execute()
                    .get("values")
                )
            except googleError as e:
                logger.debug(e)
                raise GoogleError(
                    f"Ошибка при получении данных из {spreadsheet_id}:{sheet_title}"
                )

        return get_values(spreadsheet_id=spreadsheet_id, sheet_title=sheet_title)


def init_sheets_service(credentials, cache):
    return GoogleSheetsService(credentials, cache)
