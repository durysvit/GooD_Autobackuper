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

from enum import IntEnum


class TableColumn(IntEnum):
    PATH_FROM = 0
    FOLDER_ID = 1
    ACCOUNT_NAME = 2
    TIME = 3
    WEEKDAY = 4
    DAY_OF_MONTH = 5

    @classmethod
    def labels(cls) -> list[str]:
        return [
            "Path from",
            "Folder ID",
            "Account",
            "Time",
            "Weekday",
            "Day of month"
        ]
