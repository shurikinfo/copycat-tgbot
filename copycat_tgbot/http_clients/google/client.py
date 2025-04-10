import json
import logging
from os import getenv

from google.oauth2.service_account import Credentials

from copycat_tgbot.constants import GOOGLE_CREDENTIALS_PATH, GOOGLE_SHEETS_FIELDS
from copycat_tgbot.error import GoogleError
from copycat_tgbot.http_clients.google.drive import (
    GoogleDriveService,
    init_drive_service,
)
from copycat_tgbot.http_clients.google.spreadsheets import (
    GoogleSheetsService,
    init_sheets_service,
)

logger = logging.getLogger(__name__)


class GoogleClient:
    """Клиент Google для работы с другими сервисами"""

    def __init__(self):
        self.credentials = None
        self.drive = None
        self.sheets = None

    def init_client(self, config, cache):
        """
        Указываем доступы для клиента и инициализируем сервисы

        :param config: Конфигурация приложения
        :param cache: Кэш приложения, с которым нужно работать
        :return:
        """

        services = (
            GoogleDriveService,
            GoogleSheetsService,
        )
        scopes = [
            config.get(f"{service.SERVICE_NAME.upper()}_URL") for service in services
        ]

        with open(GOOGLE_CREDENTIALS_PATH, "r") as gc:
            credentials = json.load(gc)

        self.credentials = Credentials.from_service_account_info(
            credentials, scopes=scopes
        )

        logger.debug(f"Инициализируем Google Drive")
        self.drive = GoogleDriveService(credentials=self.credentials)

        logger.debug(f"Инициализируем Google Sheets")
        self.sheets = GoogleSheetsService(credentials=self.credentials, cache=cache)

    def setup_client(self):
        """Получаем файлы, с которыми будем работать в рамках приложения"""
        file = self.drive.get_file(getenv("GOOGLE_FILE_NAME"))

        if not file:
            logger.debug("Не нашли документ, создаем новый")
            spreadsheet_id = self.sheets.create_sheets(
                file_name=getenv("GOOGLE_FILE_NAME"), sheets=GOOGLE_SHEETS_FIELDS
            )
            if spreadsheet_id:
                self.sheets.spreadsheet_id = spreadsheet_id
                self.sheets.create_statistics_sheet(
                    sheets_titles=GOOGLE_SHEETS_FIELDS.keys(),
                )
                self.drive.add_permissions(
                    file_id=spreadsheet_id,
                    permission_emails=getenv("GOOGLE_EMAILS").split(","),
                )

        else:
            # Проверим, что у указанных пользователей есть права для работы с файлом
            permissions = self.drive.get_permissions(file_id=file["id"])
            permissioned_emails = [
                list(permission.values())[0] for permission in permissions
            ]

            emails_to_add_permissions = []
            for email in getenv("GOOGLE_EMAILS").split(","):
                if email not in permissioned_emails:
                    emails_to_add_permissions.append(email)

            if len(emails_to_add_permissions) != 0:
                logger.info(
                    f"Нашли пользователей без доступа к документу: {emails_to_add_permissions}"
                )
                self.drive.add_permissions(
                    file_id=file["id"], permission_emails=emails_to_add_permissions
                )
            self.sheets.spreadsheet_id = file["id"]

        if not self.sheets.spreadsheet_id:
            raise GoogleError("Ошибка при получении файла Google Sheets")

        logger.debug("Сохраняем таблицу в кэш")
        self.sheets.get_values_cached(
            spreadsheet_id=self.sheets.spreadsheet_id, sheet_title="books"
        )
