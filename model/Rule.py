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

"""Module containing the Rule class."""

from exception.exceptions import (
    PathFromIsNoneException,
    PathFromIsBlankException,
    FolderIDIsNoneException,
    FolderIDIsBlankException,
    AccountIsNoneException,
    AccountIsBlankException,
    TimeIsNoneException,
    TimeIsBlankException,
    WeekdayIsBlankException,
    WeekdayIsInvalidException,
    DayOfMonthOutOfRangeException
)


class Rule:
    """Class representing a rule."""
    def __init__(self, pathFrom: str, folderID: str, account: str, time: str,
                 weekday: str | None = None, dayOfMonth: int | None = None):
        """
        Initializes a Rule instance with the given parameters.
        Args:
            pathFrom (str): source path to copy from.
            folderID (str): target Google Drive folder ID.
            account (str): associated account name.
            time (str): time when the rule should be triggered.
            weekday (str, None): weekday when the rule should be triggered
            (optional).
            dayOfMonth(int, None): day of month when the rule should be
            triggered (optional).
        Raises:
            PathFromIsNoneException: if pathFrom is None.
            PathFromIsBlankException: if pathFrom is an empty string.
            FolderIDIsNoneException: if folderID is None.
            FolderIDIsBlankException: if folderID is an empty string.
            AccountIsNoneException: if account is None.
            AccountIsBlankException: if account is an empty string.
            TimeIsNoneException: if time is None.
            TimeIsBlankException: if time is an empty string.
            WeekdayIsBlankException: if weekday is an empty string.
            WeekdayIsInvalidException: if weekday is not in "Monday" ...
            "Sunday".
            DayOfMonthOutOfRangeException: if dayOfMonth is not in 1–31.
        """
        self.pathFrom = pathFrom
        self.folderID = folderID
        self.account = account
        self.time = time
        self.weekday = weekday
        self.dayOfMonth = dayOfMonth

    @property
    def pathFrom(self) -> str:
        return self.__pathFrom

    @pathFrom.setter
    def pathFrom(self, pathFrom: str) -> None:
        if pathFrom is None:
            raise PathFromIsNoneException()
        if not pathFrom.strip():
            raise PathFromIsBlankException()
        self.__pathFrom = pathFrom

    @property
    def folderID(self) -> str:
        return self.__folderID

    @folderID.setter
    def folderID(self, folderID: str) -> None:
        if folderID is None:
            raise FolderIDIsNoneException()
        if not folderID.strip():
            raise FolderIDIsBlankException()
        self.__folderID = folderID

    @property
    def account(self) -> str:
        return self.__account

    @account.setter
    def account(self, account: str) -> None:
        if account is None:
            raise AccountIsNoneException()
        if not account.strip():
            raise AccountIsBlankException()
        self.__account = account

    @property
    def time(self) -> str:
        return self.__time

    @time.setter
    def time(self, time: str) -> None:
        if time is None:
            raise TimeIsNoneException()
        if not time.strip():
            raise TimeIsBlankException()
        self.__time = time

    @property
    def weekday(self) -> str:
        return self.__weekday

    @weekday.setter
    def weekday(self, weekday: str | None) -> None:
        if weekday is None:
            self.__weekday = None
            return
        if not weekday.strip():
            raise WeekdayIsBlankException()

        weekdayList = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                       "Saturday", "Sunday"]
        if weekday not in weekdayList:
            raise WeekdayIsInvalidException(weekday)
        self.__weekday = weekday

    @property
    def dayOfMonth(self) -> int:
        return self.__dayOfMonth

    @dayOfMonth.setter
    def dayOfMonth(self, dayOfMonth: int | None) -> None:
        if dayOfMonth is None:
            self.__dayOfMonth = None
            return

        MIN_DAY_OF_MONTH = 1
        MAX_DAY_OF_MONTH = 31
        if not (MIN_DAY_OF_MONTH <= dayOfMonth <= MAX_DAY_OF_MONTH):
            raise DayOfMonthOutOfRangeException()
        self.__dayOfMonth = dayOfMonth

    def toRow(self) -> list:
        return [
            self.pathFrom,
            self.folderID,
            self.account,
            self.time,
            self.weekday,
            self.dayOfMonth
        ]

    def copy(self) -> "Rule":
        return Rule(
            pathFrom=self.pathFrom,
            folderID=self.folderID,
            account=self.account,
            time=self.time,
            weekday=self.weekday,
            dayOfMonth=self.dayOfMonth
        )

    def __str__(self) -> str:
        return f"Rule(pathFrom={self.pathFrom},folderID={self.folderID}," + \
            f"account={self.account},time={self.time}," + \
            f"weekday={self.weekday},dayOfMonth={self.dayOfMonth})"

    def __eq__(self, other: "Rule") -> bool:
        return (
            self.pathFrom == other.pathFrom and
            self.folderID == other.folderID and
            self.account == other.account and
            self.time == other.time and
            self.weekday == other.weekday and
            self.dayOfMonth == other.dayOfMonth
        )

    def __hash__(self) -> int:
        return hash((
            self.pathFrom,
            self.folderID,
            self.account,
            self.time,
            self.weekday,
            self.dayOfMonth
        ))
