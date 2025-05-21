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

"""Module containing the DayOfMonthRule class."""

from exception import (
    DayOfMonthIsNoneException,
    DayOfMonthOutOfRangeException
)


class DayOfMonthRule:
    """Class representing a day of month rule."""
    def __init__(self, pathFrom: str, folderID: str, account: str, time: str,
                 dayOfMonth: int):
        """
        Initializes a Rule instance with the given parameters.
        Args:
            pathFrom (str): source path to copy from.
            folderID (str): target Google Drive folder ID.
            account (str): associated account name.
            time (str): time when the rule should be triggered.
            dayOfMonth (int): day of the month (1–31).
        Raises:
            PathFromIsNoneException: if pathFrom is None.
            PathFromIsBlankException: if pathFrom is an empty string.
            FolderIDIsNoneException: if folderID is None.
            FolderIDIsBlankException: if folderID is an empty string.
            AccountIsNoneException: if account is None.
            AccountIsBlankException: if account is an empty string.
            TimeIsNoneException: if time is None.
            TimeIsBlankException: if time is an empty string.
            DayOfMonthIsNoneException: if dayOfMonth is None.
            DayOfMonthOutOfRangeException: if dayOfMonth is not in 1–31.
        """
        super().__init__(pathFrom, folderID, account, time)
        self.dayOfMonth = dayOfMonth

    @property
    def dayOfMonth(self) -> int:
        return self.__dayOfMonth

    @dayOfMonth.setter
    def dayOfMonth(self, dayOfMonth: int) -> None:
        MIN_DAY_OF_MONTH = 1
        MAX_DAY_OF_MONTH = 31
        if dayOfMonth is None:
            raise DayOfMonthIsNoneException()
        if not (MIN_DAY_OF_MONTH <= dayOfMonth <= MAX_DAY_OF_MONTH):
            raise DayOfMonthOutOfRangeException()
        self.__dayOfMonth = dayOfMonth

    def __str__(self) -> str:
        return "DayOfMonthRule(" + super(DayOfMonthRule, self).__str__() + \
            f"dayOfMonth={self.dayOfMonth})"
