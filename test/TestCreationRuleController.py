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

"""Module containing the TestCreationRuleController class."""

import unittest
from unittest.mock import Mock, patch

from controller.CreationRuleController import CreationRuleController
from exception.exceptions import (
    PathFromLineEditIsEmptyException,
    FolderIDLineEditIsEmptyException,
    AccountLineEditIsEmptyException,
    TimeListIsEmptyException
)


class TestCreationRuleController(unittest.TestCase):
    """The test class of TestCreationRuleController"""
    def setUp(self):
        self.mockModel = Mock()
        self.mockView = Mock()

        self.controller = CreationRuleController(
            self.mockModel,
            self.mockView
        )

    def testGetRuleDataSuccess(self):
        """Successful rule creation."""
        self.mockView.getInputs.return_value = {
            "pathFrom": "/path",
            "folderID": "123",
            "account": "acc",
            "timeList": ["10:00", "12:00"],
            "weekday": "",
            "dayOfMonth": 0
        }

        result = self.controller.getRuleData()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].time, "10:00")
        self.assertIsNone(result[0].weekday)
        self.assertIsNone(result[0].dayOfMonth)

    def testGetRuleDataEmptyPath(self):
        """The empty pathFrom field."""
        self.mockView.getInputs.return_value = {
            "pathFrom": "",
            "folderID": "123",
            "account": "acc",
            "timeList": ["10:00"],
            "weekday": "",
            "dayOfMonth": 0
        }

        with self.assertRaises(PathFromLineEditIsEmptyException):
            self.controller.getRuleData()

    def testGetRuleDataEmptyFolder(self):
        """The empty folderID field."""
        self.mockView.getInputs.return_value = {
            "pathFrom": "/path",
            "folderID": "",
            "account": "acc",
            "timeList": ["10:00"],
            "weekday": "",
            "dayOfMonth": 0
        }

        with self.assertRaises(FolderIDLineEditIsEmptyException):
            self.controller.getRuleData()

    def testGetRuleDataEmptyAccount(self):
        """The empty account field."""
        self.mockView.getInputs.return_value = {
            "pathFrom": "/path",
            "folderID": "123",
            "account": "",
            "timeList": ["10:00"],
            "weekday": "",
            "dayOfMonth": 0
        }

        with self.assertRaises(AccountLineEditIsEmptyException):
            self.controller.getRuleData()

    def testGetRuleDataEmptyTimeList(self):
        """The empty timeList field."""
        self.mockView.getInputs.return_value = {
            "pathFrom": "/path",
            "folderID": "123",
            "account": "acc",
            "timeList": [],
            "weekday": "",
            "dayOfMonth": 0
        }

        with self.assertRaises(TimeListIsEmptyException):
            self.controller.getRuleData()

    def testAddRulesSuccess(self):
        """Checking addRules."""
        self.mockView.getInputs.return_value = {
            "pathFrom": "/path",
            "folderID": "123",
            "account": "acc",
            "timeList": ["10:00"],
            "weekday": "",
            "dayOfMonth": 0
        }

        self.controller.addRules()

        self.mockModel.saveUniqueRules.assert_called_once()
        self.mockView.accept.assert_called_once()

    @patch("controller.CreationRuleController.reportException")
    def test_add_rules_exception(self, mock_report):
        """Checking addRules on error."""
        self.mockView.getInputs.return_value = {
            "pathFrom": "",
            "folderID": "123",
            "account": "acc",
            "timeList": ["10:00"],
            "weekday": "",
            "dayOfMonth": 0
        }

        self.controller.addRules()

        mock_report.assert_called_once()
        self.mockModel.saveUniqueRules.assert_not_called()