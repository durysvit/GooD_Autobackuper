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
The class of NotExistFolderIDException.
"""


class NotExistFolderIDException(Exception):
    def __init__(self, folderID):
        """
        Raises if folder ID does not exsist.
        """

        super().__init__(
            "NotExistFolderIDException: " + folderID + " folder ID does not"
            " exist"
        )
