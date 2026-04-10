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

"""Module containing unit tests for Rule class."""

import unittest
from model.Rule import Rule
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


class TestRule(unittest.TestCase):
    """Unit tests for Rule class."""

    def setUp(self):
        """Set up valid default data."""
        self.validData = {
            "pathFrom": "/path",
            "folderID": "123",
            "account": "acc",
            "time": "10:00",
            "weekday": "Monday",
            "dayOfMonth": 10
        }

    def testCreateValidRule(self):
        """Test successful rule creation."""
        rule = Rule(**self.validData)
        self.assertEqual(rule.pathFrom, "/path")

    def testPathFromNone(self):
        """Test pathFrom None exception."""
        self.validData["pathFrom"] = None
        with self.assertRaises(PathFromIsNoneException):
            Rule(**self.validData)

    def testPathFromBlank(self):
        """Test pathFrom blank exception."""
        self.validData["pathFrom"] = "   "
        with self.assertRaises(PathFromIsBlankException):
            Rule(**self.validData)

    def testFolderIDNone(self):
        """Test folderID None exception."""
        self.validData["folderID"] = None
        with self.assertRaises(FolderIDIsNoneException):
            Rule(**self.validData)

    def testFolderIDBlank(self):
        """Test folderID blank exception."""
        self.validData["folderID"] = ""
        with self.assertRaises(FolderIDIsBlankException):
            Rule(**self.validData)

    def testAccountNone(self):
        """Test account None exception."""
        self.validData["account"] = None
        with self.assertRaises(AccountIsNoneException):
            Rule(**self.validData)

    def testAccountBlank(self):
        """Test account blank exception."""
        self.validData["account"] = ""
        with self.assertRaises(AccountIsBlankException):
            Rule(**self.validData)

    def testTimeNone(self):
        """Test time None exception."""
        self.validData["time"] = None
        with self.assertRaises(TimeIsNoneException):
            Rule(**self.validData)

    def testTimeBlank(self):
        """Test time blank exception."""
        self.validData["time"] = ""
        with self.assertRaises(TimeIsBlankException):
            Rule(**self.validData)

    def testWeekdayInvalid(self):
        """Test invalid weekday."""
        self.validData["weekday"] = "Invalid"
        with self.assertRaises(WeekdayIsInvalidException):
            Rule(**self.validData)

    def testWeekdayBlank(self):
        """Test blank weekday."""
        self.validData["weekday"] = ""
        with self.assertRaises(WeekdayIsBlankException):
            Rule(**self.validData)

    def testDayOfMonthInvalid(self):
        """Test invalid day of month."""
        self.validData["dayOfMonth"] = 40
        with self.assertRaises(DayOfMonthOutOfRangeException):
            Rule(**self.validData)

    def testToRow(self):
        """Test conversion to row."""
        rule = Rule(**self.validData)
        self.assertEqual(len(rule.toRow()), 6)

    def testCopy(self):
        """Test copy method."""
        rule = Rule(**self.validData)
        copyRule = rule.copy()
        self.assertEqual(rule, copyRule)

    def testEquality(self):
        """Test equality."""
        r1 = Rule(**self.validData)
        r2 = Rule(**self.validData)
        self.assertEqual(r1, r2)

    def testHash(self):
        """Test hash consistency."""
        r1 = Rule(**self.validData)
        r2 = Rule(**self.validData)
        self.assertEqual(hash(r1), hash(r2))


if __name__ == "__main__":
    unittest.main()
