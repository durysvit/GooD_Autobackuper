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

"""Module containing the CredentialsRepository class."""

import os
from const.const import TOKEN_FILE, SCOPES
from google.oauth2.credentials import Credentials
from exception.exceptions import (
    TokenFileDoesNotExistException,
)


class CredentialsRepository:
    """The model of the CredentialsRepository."""
    def loadCredentials(self) -> Credentials:
        """
        Loads TOKEN_FILE.
        Raises:
            TokenFileDoesNotExistException: raises if the token file does not
            exist.
        """
        if not os.path.exists(TOKEN_FILE):
            raise TokenFileDoesNotExistException()
        return Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    def saveCredentials(self, credentials: Credentials) -> None:
        """Saves TOKEN_FILE."""
        with open(TOKEN_FILE, 'w') as credentialsFile:
            credentialsFile.write(credentials.to_json())

    def deleteTokenFile(self) -> None:
        """
        Deletes TOKEN_FILE.
        Raises:
            TokenFileDoesNotExistException: raises if the token file does not
            exist.
        """
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)
        else:
            raise TokenFileDoesNotExistException()
