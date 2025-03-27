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

"""
The class of file copy worker.
"""

import os
import time
import datetime
import pickle
import const.const as const
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from exception.FileNotUploadedException import FileNotUploadedException
from exception.NotExistFolderIDException import NotExistFolderIDException


class FileCopyWorker(QThread):
    """
    The class of Google Drive worker.
    """

    updateSignal = pyqtSignal()

    def __init__(self, rules):
        """
        Args:
            rules: is a list of rules.
        """

        super().__init__()
        self.rules = rules  # Can be empty.
        self.driveService = self.connectToGoogleDrive()

    def connectToGoogleDrive(self):
        """
        Saves user authorization data for automatic authorization in the
        future.
        Raises:
            FileExistsError: raise if TOKEN_FILE doesn't exsist.
            FileExistsError: raise if CREDENTIAL_FILE doesn't exsist.
        """

        creds = None

        if os.path.exists(const.TOKEN_FILE):
            with open(const.TOKEN_FILE, "rb") as token:
                creds = pickle.load(token)
        else:
            QMessageBox.critical(
                None,
                "Error",
                str(FileExistsError(
                    "FileExistsError: " + const.TOKEN_FILE +
                    " does not exsist."
                )),
                QMessageBox.Ok
            )

        if not os.path.exists(const.CREDENTIALS_FILE):
            QMessageBox.critical(
                None,
                "Error",
                str(FileExistsError(
                    "FileExistsError: " + const.CREDENTIALS_FILE +
                    " does not exsist."
                )),
                QMessageBox.Ok
            )
            return

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    const.CREDENTIALS_FILE,
                    const.SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(const.TOKEN_FILE, "wb") as token:
                pickle.dump(creds, token)

        driveService = build("drive", "v3", credentials=creds)
        return driveService

    def run(self):
        """
        Checks the time to start copying.
        """

        while True:
            now = datetime.datetime.now()
            nowStr = now.strftime("%H:%M:%S")

            for rule in self.rules:
                pathFrom, folderID, Account, timeToCopy = rule
                targetTime = datetime.datetime.strptime(timeToCopy, "%H:%M")
                targetTimeStr = targetTime.strftime("%H:%M")

                if nowStr[:5] == targetTimeStr:
                    if os.path.exists(pathFrom):
                        if not self.isFolderIDExists(folderID):
                            QMessageBox.critical(
                                None,
                                "Error",
                                str(NotExistFolderIDException(folderID)),
                                QMessageBox.Ok
                            )
                            return
                        self.uploadToGoogleDrive(pathFrom, folderID)
                    else:
                        QMessageBox.critical(
                            None,
                            "Error",
                            str(FileExistsError(
                                "FileExistsError: " + pathFrom +
                                " does not exist."
                            )),
                            QMessageBox.Ok
                        )
                        return

            self.updateSignal.emit()

            time.sleep(const.ONE_MINUT_IN_SECONDS)

    def uploadToGoogleDrive(self, source, destinationFolderID):
        """
        Uploads files from a list of file paths to a Google Drive folder by
        its ID.
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
                self.uploadFile(filePath, destinationFolderID)

    def uploadFile(self, filePath, destinationFolderID):
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
            'name': os.path.basename(filePath),
            'parents': [destinationFolderID]
        }

        media = MediaFileUpload(filePath, mimetype='application/octet-stream')

        try:
            self.driveService.files().create(
                body=fileMetadata,
                media_body=media,
                fields='id'
            ).execute()
        except HttpError as exception:
            QMessageBox.critical(
                None,
                "Error",
                str(FileNotUploadedException() + exception),
                QMessageBox.Ok
            )

    def isFolderIDExists(self, folderID):
        """
        Checks whether a folder with a given ID exists.
        Args:
            folderID: is the Google Drive folder ID.
        """

        try:
            fileMetadata = self.driveService.files().get(
                fileId=folderID,
                fields='id, name, mimeType'
            ).execute()

            if fileMetadata.get("mimeType") == "application/" + \
                    "vnd.google-apps.folder":
                return True
            else:
                return False
        except HttpError as error:
            QMessageBox.critical(
                None,
                "Error",
                str(error),
                QMessageBox.Ok
            )
            return False
