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
from model.Rule import Rule
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from exception.exceptions import (
    FileNotUploadedException,
    FolderIDDoesNotExistException,
    ListOfRulesIsNoneException,
    DriveServiceInNoneException,
)


class FileCopyWorker(QThread):
    """The class of Google Drive worker."""
    updateSignal = pyqtSignal()
    errorOccured = pyqtSignal(str)

    def __init__(self, driveService: "Service", listOfRules: list[Rule]):
        """
        Initializes the file copy worker.
        Args:
            listOfRules (list[Rule]): list of rules.
        Raises:
            ListOfRulesIsNoneException: raise if the list of rules is None.
            DriveServiceInNoneException: raises if the drive service is None.
        """
        super().__init__()
        if listOfRules is None:
            raise ListOfRulesIsNoneException()
        if driveService is None:
            raise DriveServiceInNoneException()

        self.driveService = driveService
        self.listOfRules = listOfRules

    def run(self) -> None:
        """Checks the time, the date to start copying."""
        while True:
            for rule in self.listOfRules:
                now = datetime.datetime.now()
                currentWeekday = now.strftime("%A")
                currentDayOfMonth = now.day
                currentTimeStr = now.strftime("%H:%M")

                shouldCheck = True

                if rule.weekday and rule.weekday.strip():
                    if rule.weekday.lower() != currentWeekday.lower():
                        shouldCheck = False

                if rule.dayOfMonth:
                    if rule.dayOfMonth != currentDayOfMonth:
                        shouldCheck = False

                if shouldCheck and currentTimeStr == rule.time:
                    try:
                        if not self.__isFolderIDExists(rule.folderID):
                            raise FolderIDDoesNotExistException(rule.folderID)
                    except (
                        FolderIDDoesNotExistException,
                        HttpError
                    ) as exception:
                        self.errorOccured.emit(str(exception))
                        continue
                    try:
                        self.__uploadToGoogleDrive(
                            rule.pathFrom,
                            rule.folderID
                        )
                    except FileNotUploadedException as exception:
                        self.errorOccured.emit(str(exception))
                        continue
            self.updateSignal.emit()
            WORKER_CHECK_TIME = 60
            time.sleep(WORKER_CHECK_TIME)

    def __uploadToGoogleDrive(self, source: list, folderID: str) -> None:
        """
        Uploads files from a list of file paths to a Google Drive folder by its
        ID.
        Args:
            source: is a list of file paths.
            folderID: is the ID of the destination folder.
        Raises:
            FileNotUploadedException: raise if the file has not been uploaded
            to Google Drive.
        """
        for filename in os.listdir(source):
            filePath = os.path.join(source, filename)
            if os.path.isfile(filePath):
                try:
                    self.__uploadFile(filePath, folderID)
                except Exception:
                    raise FileNotUploadedException()

    def __uploadFile(self, filePath: str, folderID: str) -> None:
        """
        Uploads a single file to the given Google Drive folder by its ID.
        Args:
            filePath: is a file path.
            folderID: is the destination folder ID.
        """
        fileName = os.path.basename(filePath)

        query = f"'{folderID}' in parents and name = '{fileName}' and " + \
            "trashed = false"
        response = self.driveService.files().list(
            q=query,
            spaces="drive",
            fields="files(id)"
        ).execute()
        files = response.get("files", [])

        media = MediaFileUpload(filePath, mimetype="application/octet-stream")

        if files:
            fileId = files[0]["id"]
            self.driveService.files().update(
                fileId=fileId,
                media_body=media
            ).execute()
        else:
            metadata = {"name": fileName, "parents": [folderID]}
            self.driveService.files().create(
                body=metadata,
                media_body=media,
                fields="id"
            ).execute()

    def __isFolderIDExists(self, folderID: str) -> bool:
        """
        Checks whether a folder with a given ID exists.
        Args:
            folderID: is the Google Drive folder ID.
        Raises:
            HttpError: raise if the folder ID doesn't exist.
        """
        try:
            self.driveService.files().get(
                fileId=folderID,
                fields="id, name, mimeType"
            ).execute()
            return True
        except HttpError as e:
            if e.resp.status == 404:
                return False
            raise FolderIDDoesNotExistException(folderID)
