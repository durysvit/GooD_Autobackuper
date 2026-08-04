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

from exceptions.exceptions import (
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
    """Class representing a rules."""
    def __init__(self, path_from: str, folder_id: str, account: str, time: str,
                 weekday: str | None = None, day_of_month: int | None = None):
        """
        Initializes a Rule instance with the given parameters.
        Args:
            path_from (str): source path to copy from.
            folder_id (str): target Google Drive folder ID.
            account (str): associated account name.
            time (str): time when the rules should be triggered.
            weekday (str, None): weekday when the rules should be triggered
                (optional).
            day_of_month(int, None): day of month when the rules should be
                triggered (optional).
        Raises:
            PathFromIsNoneException: if path_from is None.
            PathFromIsBlankException: if path_from is an empty string.
            FolderIDIsNoneException: if folder_id is None.
            FolderIDIsBlankException: if folder_id is an empty string.
            AccountIsNoneException: if account is None.
            AccountIsBlankException: if account is an empty string.
            TimeIsNoneException: if time is None.
            TimeIsBlankException: if time is an empty string.
            WeekdayIsBlankException: if weekday is an empty string.
            WeekdayIsInvalidException: if weekday is not in "Monday" ...
                "Sunday".
            DayOfMonthOutOfRangeException: if day_of_month is not in 1–31.
        """
        self.path_from = path_from
        self.folder_id = folder_id
        self.account = account
        self.time = time
        self.weekday = weekday
        self.day_of_month = day_of_month

    @property
    def path_from(self) -> str:
        return self.__pathFrom

    @path_from.setter
    def path_from(self, path_from: str) -> None:
        if path_from is None:
            raise PathFromIsNoneException()
        if not path_from.strip():
            raise PathFromIsBlankException()
        self.__pathFrom = path_from

    @property
    def folder_id(self) -> str:
        return self.__folderID

    @folder_id.setter
    def folder_id(self, folder_id: str) -> None:
        if folder_id is None:
            raise FolderIDIsNoneException()
        if not folder_id.strip():
            raise FolderIDIsBlankException()
        self.__folderID = folder_id

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
    def weekday(self) -> str | None:
        return self.__weekday

    @weekday.setter
    def weekday(self, weekday: str | None) -> None:
        if weekday is None:
            self.__weekday = None
        else:
            if not weekday.strip():
                raise WeekdayIsBlankException()

            weekdays_list = [
                "Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"
            ]

            if weekday not in weekdays_list:
                raise WeekdayIsInvalidException(weekday)

            self.__weekday = weekday

    @property
    def day_of_month(self) -> int | None:
        return self.__dayOfMonth

    @day_of_month.setter
    def day_of_month(self, day_of_month: int | None) -> None:
        if day_of_month is None:
            self.__dayOfMonth = None
        else:
            MIN_DAY_OF_MONTH = 1
            MAX_DAY_OF_MONTH = 31
            if not MIN_DAY_OF_MONTH <= day_of_month <= MAX_DAY_OF_MONTH:
                raise DayOfMonthOutOfRangeException()

            self.__dayOfMonth = day_of_month

    def to_row(self) -> list:
        return [
            self.path_from,
            self.folder_id,
            self.account,
            self.time,
            self.weekday,
            self.day_of_month
        ]

    def copy(self) -> "Rule":
        return Rule(
            path_from=self.path_from,
            folder_id=self.folder_id,
            account=self.account,
            time=self.time,
            weekday=self.weekday,
            day_of_month=self.day_of_month
        )

    def __str__(self) -> str:
        return f"Rule(pathFrom={self.path_from},folderID={self.folder_id}," + \
            f"account={self.account},time={self.time}," + \
            f"weekday={self.weekday},dayOfMonth={self.day_of_month})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rule):
            return NotImplemented

        return (
                self.path_from == other.path_from and
                self.folder_id == other.folder_id and
                self.account == other.account and
                self.time == other.time and
                self.weekday == other.weekday and
                self.day_of_month == other.day_of_month
        )

    def __hash__(self) -> int:
        return hash((
            self.path_from,
            self.folder_id,
            self.account,
            self.time,
            self.weekday,
            self.day_of_month
        ))
