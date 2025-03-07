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

import os
import time
import datetime
import pickle
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from exception.FileNotUploadedException import *
from exception.NotExistFolderIDException import *

ONE_MINUT_IN_SECONDS = 60
TOKEN_FILE = "token.pickle"
CREDENTIALS_FILE = "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]

# The class of Google Drive worker. 
class FileCopyWorker(QThread):
    updateSignal = pyqtSignal()

    # Parameter rules is a list of rules.
    def __init__(self, rules):
        super().__init__()
        self.rules = rules # Can be empty
        self.driveService = self.connectToGoogleDrive()

    # Saves user authorization data for automatic authorization in the future.
    # Raises FileExistsError if TOKEN_FILE doesn't exsist.
    # Raises FileExistsError if CREDENTIAL_FILE doesn't exsist.
    def connectToGoogleDrive(self):
        creds = None
        
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, "rb") as token:
                creds = pickle.load(token)
        else:
            QMessageBox.critical(
                None,
                "Error",
                str(FileExistsError("FileExistsError: " + TOKEN_FILE + 
                    " does not exsist.")),
                QMessageBox.Ok
            )

        if not os.path.exists(CREDENTIALS_FILE):
            QMessageBox.critical(
                None,
                "Error",
                str(FileExistsError("FileExistsError: " + CREDENTIALS_FILE +
                    " does not exsist.")),
                QMessageBox.Ok
            )
            return
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE,
                    SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(TOKEN_FILE, "wb") as token:
                pickle.dump(creds, token)

        driveService = build("drive", "v3", credentials=creds)
        return driveService

    # Checks the time to start copying.
    def run(self):
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
                            str(FileExistsError("FileExistsError: " +
                                pathFrom + " does not exist.")),
                            QMessageBox.Ok
                        )
                        return

            self.updateSignal.emit()

            time.sleep(ONE_MINUT_IN_SECONDS)

    # Uploads files from a list of file paths to a Google Drive folder by its 
    # ID.
    # Raises FileNotUploadedException if a file fails to upload to Google 
    # Drive.
    # Parameter source is a list of file paths.
    # Parameter destinationFolderID is the ID of the destination folder.
    def uploadToGoogleDrive(self, source, destinationFolderID):
        for filename in os.listdir(source):
            filePath = os.path.join(source, filename)

            if os.path.isfile(filePath):
                self.uploadFile(filePath, destinationFolderID)

    # Uploads a single file to the given Google Drive folder by its ID.
    # Raises FileNotUploadedException if in the file has not been uploaded to 
    # Google Drive.
    # Parameter filePath is a file path.
    # Parameter destinationFolderID is the destination folder ID.
    def uploadFile(self, filePath, destinationFolderID):
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
    
    # Checks whether a folder with a given ID exists.
    # Parameter folderID is the Google Drive folder ID. 
    def isFolderIDExists(self, folderID):
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
            return False