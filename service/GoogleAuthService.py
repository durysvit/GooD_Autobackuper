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

"""Module containing the GoogleAuthService class."""

from model.CredentialsRepository import CredentialsRepository
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from const.const import CREDENTIALS_FILE, SCOPES
from exception.exceptions import TokenFileDoesNotExistException


class GoogleAuthService:
    """The class of GoogleAuthService - authorizes the user in the Google."""
    @staticmethod
    def getAuthorizedService(credentialsModel: CredentialsRepository) -> "Service":
        """
        Returns the drive service.
        Raises:
            TokenFileDoesNotExistException: raises if the token file does not
            exist (ignored).
        """
        credentials = None
        try:
            credentials = credentialsModel.loadCredentials()
        except TokenFileDoesNotExistException:
            ...
        if not credentials or not credentials.valid:
            if credentials and \
               credentials.expired and \
               credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE,
                    SCOPES
                )
                credentials = flow.run_local_server(port=0)
            credentialsModel.saveCredentials(credentials)
        return build("drive", "v3", credentials=credentials)
