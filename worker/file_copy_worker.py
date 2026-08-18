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
from PySide6.QtCore import QThread, Signal
from model.Rule import Rule
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from exceptions.exceptions import (
    FileNotUploadedException,
    FolderIDDoesNotExistException,
    ListOfRulesIsNoneException,
    DriveServiceInNoneException,
)


class FileCopyWorker(QThread):
    """The class of Google Drive worker."""
    update_signal = Signal()
    error_occurred = Signal(str)

    def __init__(self, drive_service, rules_list: list[Rule]):
        """
        Initializes the file copy worker.
        Args:
            rules_list (list[Rule]): list of rules.
        Raises:
            ListOfRulesIsNoneException: raise if the list of rules is None.
            DriveServiceInNoneException: raises if the drive service is None.
        """
        super().__init__()
        if rules_list is None:
            raise ListOfRulesIsNoneException()
        if drive_service is None:
            raise DriveServiceInNoneException()

        self.drive_service = drive_service
        self.rules_list = rules_list

    def run(self) -> None:
        """Checks the time, the date to start copying."""
        while True:
            for rule in self.rules_list:
                now = datetime.datetime.now()
                current_weekday = now.strftime("%A")
                current_day_of_month = now.day
                current_time = now.strftime("%H:%M")

                should_check = True

                if rule.weekday and rule.weekday.strip():
                    if rule.weekday.lower() != current_weekday.lower():
                        should_check = False

                if rule.day_of_month:
                    if rule.day_of_month != current_day_of_month:
                        should_check = False

                if should_check and current_time == rule.time:
                    try:
                        if not self.__is_folder_id_exists(rule.folder_id):
                            raise FolderIDDoesNotExistException(rule.folder_id)
                    except (
                        FolderIDDoesNotExistException,
                        HttpError
                    ) as exception:
                        self.error_occurred.emit(str(exception))
                        continue
                    try:
                        self.__upload_to_google_drive(
                            rule.path_from,
                            rule.folder_id
                        )
                    except FileNotUploadedException as exception:
                        self.error_occurred.emit(str(exception))
                        continue
            self.update_signal.emit()
            WORKER_CHECK_TIME = 60
            time.sleep(WORKER_CHECK_TIME)

    def __upload_to_google_drive(self, file_path: str, folder_id: str) -> None:
        """
        Uploads files from a list of file paths to a Google Drive folder by its
        ID.
        Args:
            source: is a file path.
            folder_id: is the ID of the destination folder.
        Raises:
            FileNotUploadedException: raise if the file has not been uploaded
            to Google Drive.
        """
        if os.path.isfile(file_path):
            try:
                self.__upload_file(file_path, folder_id)
            except Exception as exception:
                raise FileNotUploadedException() from exception

    def __upload_file(self, file_path: str, folder_id: str) -> None:
        """
        Uploads a single file to the given Google Drive folder by its ID.
        Args:
            file_path: is a file path.
            folder_id: is the destination folder ID.
        """
        file_name = os.path.basename(file_path)

        query = f"'{folder_id}' in parents and name = '{file_name}' and " + \
            "trashed = false"
        response = self.drive_service.files().list(
            q=query,
            spaces="drive",
            fields="files(id)"
        ).execute()
        files = response.get("files", [])

        media = MediaFileUpload(file_path, mimetype="application/octet-stream")

        if files:
            file_id = files[0]["id"]
            self.drive_service.files().update(
                fileId=file_id,
                media_body=media
            ).execute()
        else:
            metadata = {
                "name": file_name,
                "parents": [folder_id]
            }
            self.drive_service.files().create(
                body=metadata,
                media_body=media,
                fields="id"
            ).execute()

    def __is_folder_id_exists(self, folder_id: str) -> bool:
        """
        Checks whether a folder with a given ID exists.
        Args:
            folder_id: is the Google Drive folder ID.
        Raises:
            HttpError: raise if the folder ID doesn't exist.
        """
        try:
            self.drive_service.files().get(
                fileId=folder_id,
                fields="id, name, mimeType"
            ).execute()
            return True
        except HttpError as exception:
            if exception.resp.status == 404:
                return False
            raise FolderIDDoesNotExistException(folder_id) from exception
