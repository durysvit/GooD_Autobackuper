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

"""Module containing the CreationRuleWindowController class."""

from view.CreationRuleWindow import CreationRuleWindow
from model.Rule import Rule
from model.RuleRepository import RuleRepository
from logger.logger import logger
from util.displayCriticalMessage import displayCriticalMessage
from exception.exceptions import (
    PathFromLineEditIsEmptyException,
    FolderIDLineEditIsEmptyException,
    AccountLineEditIsEmptyException,
    TimeListIsEmptyException,
)


class CreationRuleWindowController:
    def __init__(self, model: RuleRepository, view: CreationRuleWindow):
        self.model = model
        self.view = view

        self.view.confirmButton.clicked.connect(self.addRules)

    def addRules(self) -> None:
        """
        Adds the rules to the file RULES_FILE_PATH.
        Raises:
            PathFromLineEditIsEmptyException: the path from line edit is empty.
            FolderIDLineEditIsEmptyException: the folder ID line dit is empty.
            AccountLineEditIsEmptyException: the account line edit is empty.
            TimeListIsEmptyException: the time list line edit is empty.
        """
        try:
            listOfRules = self.getRuleData()
            self.model.saveUniqueRules(listOfRules)
            self.view.accept()
        except (
            PathFromLineEditIsEmptyException,
            FolderIDLineEditIsEmptyException,
            AccountLineEditIsEmptyException,
            TimeListIsEmptyException
        ) as exception:
            logger.error(exception)
            displayCriticalMessage(exception)

    def getRuleData(self) -> list[Rule]:
        """
        Gets the rules data.
        Raises:
            PathFromLineEditIsEmptyException: raise if the path from line edit
            is empty.
            FolderIDLineEditIsEmptyException: raise if the folder ID line edit
            is empty.
            AccountLineEditIsEmptyException: raise if the account line edit is
            empty.
            TimeListIsEmptyException: raise if the time list is empty.
        Returns:
            listOfRules (list[Rule]): list of rules.
        """
        inputs = self.view.getInputs()

        if not inputs["pathFrom"]:
            raise PathFromLineEditIsEmptyException()
        if not inputs["folderID"]:
            raise FolderIDLineEditIsEmptyException()
        if not inputs["account"]:
            raise AccountLineEditIsEmptyException()
        if not inputs["timeList"]:
            raise TimeListIsEmptyException()

        weekday = inputs["weekday"] if inputs["weekday"].strip() \
            else None
        dayOfMonth = inputs["dayOfMonth"] if inputs["dayOfMonth"] != 0 \
            else None
        listOfRules = []

        for time in inputs["timeList"]:
            rule = Rule(
                inputs["pathFrom"],
                inputs["folderID"],
                inputs["account"],
                time,
                weekday,
                dayOfMonth
            )
            listOfRules.append(rule)

        return listOfRules
