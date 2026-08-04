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

"""Module containing the GoogleDriveService class."""


class GoogleDriveService:
    """The class of Google Drive Service."""
    @staticmethod
    def list_folders(service, parent_id="root") -> list[dict]:
        """
        Returns the directory hierarchy in Google Drive.
        Args:
            service (Service): is the drive service.
            parent_id (str): is the parent ID.
        Returns:
            list[dict]: the directory hierarchy in Google Drive.
        """
        query = f"'{parent_id}' in parents and mimeType = " + \
            "'application/vnd.google-apps.folder' and trashed = false"
        result = service.files().list(
            q=query,
            fields="files(id, name)"
        ).execute()
        return result.get("files", [])
