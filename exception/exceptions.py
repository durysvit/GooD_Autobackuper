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

"""Module containing exceptions."""


class AccountIsBlankException(Exception):
    def __init__(self):
        """Raises if account is blank."""
        super().__init__("AccountIsBlankException: account is blank.")


class AccountIsNoneException(Exception):
    def __init__(self):
        """Raises if account is None."""
        super().__init__("AccountIsNoneException: account is None.")


class CredentialsFileDoesNotExistException(Exception):
    def __init__(self):
        """Raises if credentials file does not exist"""
        super().__init__(
            "CredentialsFileDoesNotExistException: the credentials file does" +
            " not exist."
        )


class FileNotUploadedException(Exception):
    def __init__(self):
        """Raises if in the file has not been uploaded to Google Drive."""
        super().__init__(
            "FileNotUploadedException: the file has not been uploaded to " +
            "Google Drive."
        )


class FolderIDDoesNotExistException(Exception):
    def __init__(self, folderID: str):
        """Raises if folder ID does not exist."""
        super().__init__(
            "FolderIDDoesNotExistException: " + folderID + " folder ID does " +
            "not exist"
        )


class FolderIDIsBlankException(Exception):
    def __init__(self):
        """Raises if folderID is blank."""
        super().__init__("FolderIDIsBlankException: the folderID is blank.")


class FolderIDIsNoneException(Exception):
    def __init__(self):
        """Raises if folderID is None."""
        super().__init__("FolderIDIsNoneException: the folderID is None.")


class ListOfRulesIsEmptyException(Exception):
    def __init__(self):
        """Raises if the list of rules is empty."""
        super().__init__(
            "ListOfRulesIsEmptyException: the list of rules is empty"
        )


class ListOfRulesIsNoneException(Exception):
    def __init__(self):
        """Raises if the list of rules is None."""
        super().__init__(
            "ListOfRulesIsNoneException: the list of rules is None"
        )


class NoRuleSelectedInTableException(Exception):
    def __init__(self):
        """Raises if no rule was selected to delete."""
        super().__init__(
            "NoRowSelectedInTableException: no rule was selected to delete."
        )


class PathFromIsBlankException(Exception):
    def __init__(self):
        """Raises if pathFrom is blank."""
        super().__init__("PathFromIsBlankException: the pathFrom is blank.")


class PathFromIsNoneException(Exception):
    def __init__(self):
        """Raises if pathFrom is None."""
        super().__init__("PathFromIsNoneException: the pathFrom is None.")


class TimeIsBlankException(Exception):
    def __init__(self):
        """Raises if time is blank."""
        super().__init__("TimeIsBlankException: time is blank.")


class TimeIsNoneException(Exception):
    def __init__(self):
        """Raises if time is None."""
        super().__init__("TimeIsNoneException: time is None.")


class TimeListIsEmptyException(Exception):
    def __init__(self):
        """Raises if in the Creation rule window, the time list is empty."""
        super().__init__("TimeListIsEmptyException: the time list is empty.")


class TokenFileDoesNotExistException(Exception):
    def __init__(self):
        """Raises if token file does not exist."""
        super().__init__(
            "TokenFileDoesNotExistException: the token file does not exist."
        )


class TokenFileIsExpiredOrRevokedException(Exception):
    def __init__(self):
        """Raises if token file is expired or revoked."""
        super().__init__(
            "TokenFileIsExpiredOrRevokedException: the token file is " +
            "expired or revoked. Try delete token file and authorise again."
        )


class PathToRulesFileDoesNotExistException(Exception):
    def __init__(self):
        """Raises if path to rules file does not exist"""
        super().__ini__(
            "PathToRulesFileDoesNotExistException: path to rules file does " +
            "not exist."
        )


class WeekdayIsBlankException(Exception):
    """Raises if weekday is blank"""
    def __init__(self):
        super().__init__("WeekdayIsBlankException: weekday is blank.")


class WeekdayIsInvalidException(Exception):
    def __init__(self, message: str):
        """Raises if weekay is invalid."""
        super().__init__(
            "WeekdayIsInvalidException: " + message + " is invalid."
        )


class DayOfMonthOutOfRangeException(Exception):
    """Raises if day of month is out of range"""
    def __init__(self):
        super().__init__(
            "DayOfMonthOutOfRangeException: day of month must be in 1–31."
        )


class PathFromLineEditIsEmptyException(Exception):
    def __init__(self):
        """
        Raises if in the Creation rule window the path from line edit is empty.
        """
        super().__init__(
            "PathFromLineEditIsEmptyException: the path from line edit is " +
            "empty."
        )


class FolderIDLineEditIsEmptyException(Exception):
    def __init__(self):
        """
        Raises if in the Creation rule window the folder ID line edit is
        empty.
        """
        super().__init__(
            "FolderIDLineEditIsEmptyException: the folder ID line edit is " +
            "empty."
        )


class AccountLineEditIsEmptyException(Exception):
    def __init__(self):
        """
        Raises if in the Creation rule window the account line edit is empty.
        """
        super().__init__(
            "AccountLineEditIsEmptyException: the account line edit is empty."
        )


class MalformedRuleAttributesException(Exception):
    def __init__(self):
        """Raises if the number of rule attributes is incorrect."""
        super().__init__(
            "MalformedRuleAttributesException: the number of rule attributes" +
            "is incorrect."
        )
