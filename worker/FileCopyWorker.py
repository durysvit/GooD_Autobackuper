# This file is part of GooD Autobackuper.
#
# GooD Autobackuper program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

"""Module containing the FileCopyWorker class."""

import os
import time
import datetime
from PyQt5.QtCore import QThread, pyqtSignal
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from util.displayCriticalMessage import displayCriticalMessage
from logger.logger import logger
from const.const import TOKEN_FILE, CREDENTIALS_FILE, SCOPES
from exception.exceptions import (
    FileNotUploadedException,
    FolderIDDoesNotExistException,
    TokenFileDoesNotExistException,
    CredentialsFileDoesNotExistException,
    TokenFileIsExpiredOrRevokedException,
    ListOfRulesIsEmptyException,
    ListOfRulesIsNoneException
)


class FileCopyWorker(QThread):
    """The class of Google Drive worker."""
    updateSignal = pyqtSignal()

    def __init__(self, rules: list):
        """
        Args:
            rules: list of rules.
        Raises:
            ListOfRulesIsNoneException: raise if the list of rules is None.
            ListOfRulesIsEmptyException: raise if the list of rules is empty.
            TokenFileIsExpiredOrRevokedException: raise if token file is
            expired or revoked. This exception is caught and logged internally.
        """
        super().__init__()
        try:
            self.driveService = self.__connectToGoogleDrive()
        except RefreshError:
            message = str(TokenFileIsExpiredOrRevokedException())
            logger.error(message)
            displayCriticalMessage(message)
            return
        if rules is None:
            raise ListOfRulesIsNoneException()
        if not rules:
            raise ListOfRulesIsEmptyException()

        self.rules = rules

    def __connectToGoogleDrive(self) -> None:
        """
        Saves user authorization data for automatic authorization in the
        future.
        Raises:
            TokenFileDoesNotExistException: raise if TOKEN_FILE doesn't exist.
            CredentialsFileDoesNotExistException: raise if CREDENTIAL_FILE
            doesn't exist.
        """
        creds = None
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        else:
            logger.error(TokenFileDoesNotExistException())
        if not os.path.exists(CREDENTIALS_FILE):
            logger.error(CredentialsFileDoesNotExistException())
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE,
                    SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())
        driveService = build("drive", "v3", credentials=creds)
        return driveService

    def run(self) -> None:
        """Checks the time to start copying."""
        while True:  # replace True
            for rule in self.rules:
                pathFrom, folderID, Account, timeToCopy, weekday, dayOfMonth \
                    = rule

                now = datetime.datetime.now()
                currentWeekday = now.strftime("%A")
                currentDayOfMonth = now.day
                currentTimeStr = now.strftime("%H:%M")

                targetTimeStr = datetime.datetime.strptime(
                    timeToCopy,
                    "%H:%M"
                ).strftime("%H:%M")

                targetTime = datetime.datetime.strptime(timeToCopy, "%H:%M")
                targetTimeStr = targetTime.strftime("%H:%M")

                shouldCheck = True

                if weekday.strip():
                    if weekday != currentWeekday:
                        shouldCheck = False

                if dayOfMonth.strip():
                    try:
                        targetDay = int(dayOfMonth)
                        if targetDay != currentDayOfMonth:
                            shouldCheck = False
                    except ValueError:  # Create new exception
                        logger.error(f"Invalid dayOfMonth value: {dayOfMonth}")
                        continue

                if shouldCheck and currentTimeStr == targetTimeStr:
                    if not self.__isFolderIDExists(folderID):
                        message = str(FolderIDDoesNotExistException(folderID))
                        logger.error(message)
                        displayCriticalMessage(message)
                        return
                    self.__uploadToGoogleDrive(pathFrom, folderID)
            self.updateSignal.emit()
            WORKER_CHECK_TIME = 60
            time.sleep(WORKER_CHECK_TIME)

    def __uploadToGoogleDrive(self, source: list,
                              destinationFolderID: str) -> None:
        """
        Uploads files from a list of file paths to a Google Drive folder by its
         ID.
        Args:
            source: is a list of file paths.
            destinationFolderID: is the ID of the destination folder.
        Raises:
            FileNotUploadedException: raise if a file fails to upload to
            Google Drive.
        """
        for filename in os.listdir(source):
            filePath = os.path.join(source, filename)
            if os.path.isfile(filePath):
                self.__uploadFile(filePath, destinationFolderID)

    def __uploadFile(self, filePath: str, destinationFolderID: str) -> None:
        """
        Uploads a single file to the given Google Drive folder by its ID.
        Args:
            filePath: is a file path.
            destinationFolderID: is the destination folder ID.
        Raises:
            FileNotUploadedException: raise if in the file has not been
            uploaded to Google Drive.
        """
        fileMetadata = {
            "name": os.path.basename(filePath),
            "parents": [destinationFolderID]
        }
        media = MediaFileUpload(filePath, mimetype="application/octet-stream")
        try:
            self.driveService.files().create(
                body=fileMetadata,
                media_body=media,
                fields="id"
            ).execute()
        except HttpError as exception:
            message = str(FileNotUploadedException() + exception)
            logger.error(message)
            displayCriticalMessage(message)
            return
        except Exception as exception:
            logger.error(exception)
            displayCriticalMessage(exception)
            return

    def __isFolderIDExists(self, folderID: str) -> bool:
        """
        Checks whether a folder with a given ID exists.
        Args:
            folderID: is the Google Drive folder ID.
        Raises:
            HttpError: raise if ...
        """
        try:
            fileMetadata = self.driveService.files().get(
                fileId=folderID,
                fields="id, name, mimeType"
            ).execute()
            MIME_TYPE = "application/vnd.google-apps.folder"
            if fileMetadata.get("mimeType") == MIME_TYPE:
                return True
            else:
                return False
        except HttpError as exception:
            logger.error(exception)
            displayCriticalMessage(exception)
            return False
