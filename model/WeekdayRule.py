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

"""Module containing the WeekdayRule class."""

from exception import (
    WeekdayIsBlankException,
    WeekdayIsNoneException
)


class WeekdayRule:
    """Class representing a weekday rule."""
    def __init__(self, pathFrom: str, folderID: str, account: str, time: str,
                 weekday: str):
        """
        Initializes a Rule instance with the given parameters.
        Args:
            pathFrom (str): source path to copy from.
            folderID (str): target Google Drive folder ID.
            account (str): associated account name.
            time (str): time when the rule should be triggered.
            weekday (str): day of the week (e.g., 'Monday' etc).
        Raises:
            PathFromIsNoneException: if pathFrom is None.
            PathFromIsBlankException: if pathFrom is an empty string.
            FolderIDIsNoneException: if folderID is None.
            FolderIDIsBlankException: if folderID is an empty string.
            AccountIsNoneException: if account is None.
            AccountIsBlankException: if account is an empty string.
            TimeIsNoneException: if time is None.
            TimeIsBlankException: if time is an empty string.
            WeekdayIsNoneException: if weekday is None.
            WeekdayIsBlankException: if weekday is an empty string.
        """
        super().__init__(pathFrom, folderID, account, time)
        self.weekday = weekday

    @property
    def weekday(self) -> str:
        return self.__weekday

    @weekday.setter
    def weekday(self, weekday: str) -> None:
        if weekday is None:
            raise WeekdayIsNoneException()
        if not weekday.strip():
            raise WeekdayIsBlankException()
        self.__weekday = weekday

    def __str__(self) -> str:
        return "Weekday(" + super(WeekdayRule, self).__str__() + \
            f"weekday={self.weekday})"
