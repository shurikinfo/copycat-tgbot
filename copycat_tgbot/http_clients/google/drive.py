import logging

from googleapiclient.discovery import build
from googleapiclient.errors import Error as googleError

logger = logging.getLogger(__name__)


class GoogleDriveService:
    """Сервис для работы с Google Drive"""

    SERVICE_NAME = "drive"

    def __init__(self, credentials):
        self.service = build("drive", "v3", credentials=credentials)

    def add_permissions(self, permission_emails: list, file_id: str):
        """Навесить прав для некоторых пользователей"""
        permissions = []
        for email in permission_emails:
            body_data = {"type": "user", "role": "writer", "emailAddress": email}
            try:
                permissions.append(
                    self.service.permissions()
                    .create(fileId=file_id, body=body_data)
                    .execute()
                )
                logger.info(f"Навесили права для пользователя: {email}")
            except googleError as e:
                logger.error(f"Не смогли навесить прав для пользователя: {email}")
                logger.debug(e)
        return permissions

    def get_permissions(self, file_id: str) -> dict:
        try:
            return (
                self.service.permissions()
                .list(fileId=file_id, fields="permissions(emailAddress)")
                .execute()
                .get("permissions")
            )
        except googleError as e:
            logger.error(f"Не смогли получить список доступов к файлу: {file_id}")
            logger.debug(e)
            return {}

    def get_file(self, file_name: str):
        try:
            spreadsheet = (
                self.service.files()
                .list(
                    pageSize=1,
                    fields="files(id, name)",
                    q=f"name='{file_name}' and mimeType='application/vnd.google-apps.spreadsheet' and trashed=false",
                )
                .execute()
            )
            file = spreadsheet.get("files", [])
        except googleError as e:
            logger.error(e)
            return False
        if not file:
            return False
        return file[0]


def init_drive_service(credentials) -> GoogleDriveService:
    return GoogleDriveService(credentials)
