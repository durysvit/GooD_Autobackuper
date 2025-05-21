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

from exception import (
    PathFromIsNoneException,
    PathFromIsBlankException,
    FolderIDIsNoneException,
    FolderIDIsBlankException,
    AccountIsNoneException,
    AccountIsBlankException,
    TimeIsNoneException,
    TimeIsBlankException
)


class Rule:
    """Class representing a rule."""
    def __init__(self, pathFrom: str, folderID: str, account: str, time: str):
        """
        Initializes a Rule instance with the given parameters.
        Args:
            pathFrom (str): source path to copy from.
            folderID (str): target Google Drive folder ID.
            account (str): associated account name.
            time (str): time when the rule should be triggered.
        Raises:
            PathFromIsNoneException: if pathFrom is None.
            PathFromIsBlankException: if pathFrom is an empty string.
            FolderIDIsNoneException: if folderID is None.
            FolderIDIsBlankException: if folderID is an empty string.
            AccountIsNoneException: if account is None.
            AccountIsBlankException: if account is an empty string.
            TimeIsNoneException: if time is None.
            TimeIsBlankException: if time is an empty string.
        """

        self.pathFrom = pathFrom
        self.folderID = folderID
        self.account = account
        self.time = time

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

    def copy(self) -> "Rule":
        return Rule(
            pathFrom=self.pathFrom,
            folderID=self.folderID,
            account=self.account,
            time=self.time
        )

    def __str__(self) -> str:
        return f"Rule(pathForm={self.pathForm}, folderID={self.folderID}," + \
            f" account={self.account}, time={self.time})"
