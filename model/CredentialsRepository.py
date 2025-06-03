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
from const.const import TOKEN_FILE
from exception.exceptions import TokenFileDoesNotExistException


class CredentialsRepository:
    """The model of the CredentialsRepository."""
    @staticmethod
    def deleteTokenFile(self) -> None:
        """Deletes token.json."""
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)
        else:
            raise TokenFileDoesNotExistException()
