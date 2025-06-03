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

"""Module containing the main MainWindowController class."""

from view.MainWindow import MainWindow
from view.CreationRuleWindow import CreationRuleWindow
from model.Rule import Rule
from model.RuleRepository import RuleRepository
from model.CredentialsRepository import CredentialsRepository
from controller.CreationRuleWindowController import (
    CreationRuleWindowController
)
from logger.logger import logger
from util.displayCriticalMessage import displayCriticalMessage
from exception.exceptions import (
    NoRuleSelectedInTableException,
    TokenFileDoesNotExistException,
    ListOfRulesIsEmptyException,
    PathToRulesFileDoesNotExistException,
)


class MainWindowController:
    """The class of MainWindowController."""
    def __init__(self, ruleModel: RuleRepository,
                 credentialsModel: CredentialsRepository, view: MainWindow):
        """
        Initializes a Rule instance with the given parameters.
        Args:
            ruleModel (RuleRepository): ...
            view (MainWindow): ...
        """
        self.ruleModel = ruleModel
        self.view = view

        self.view.createRulesButton.clicked.connect(
            self.displayCreateRuleWindow
        )
        self.view.deleteSelectedRuleButton.clicked.connect(
            self.deleteSelectedRuleFromTable
        )
        self.view.deleteTokenFileAction.triggered.connect(self.deleteTokenFile)
        self.view.updateTableAction.triggered.connect(self.updateTable)
        # self.view.fileCopyWorker.updateSignal.connect(self.loadRulesToTable)

        self.loadRulesToTable()

    def displayCreateRuleWindow(self) -> None:
        """Displays the CreateRuleWindow."""
        creationRuleWindow = CreationRuleWindow()
        creationRuleWindowController = CreationRuleWindowController(
            self.ruleModel,
            creationRuleWindow
        )
        creationRuleWindow.exec_()

    def loadRulesToTable(self) -> None:
        """
        Loads rules to the table from RULES_FILE.
        Raises:
            PathToRulesFileDoesNotExistException: raise if path to rules file
            does not exist.
        """
        self.view.resetTable()

        listOfRules = self.ruleModel.loadRules()

        try:
            self.view.addRulesToTable(listOfRules)
        except ListOfRulesIsEmptyException as exception:
            logger.error(exception)
            displayCriticalMessage(exception)
            return

    def deleteSelectedRuleFromTable(self) -> None:
        """
        Deletes the selected rule from the table and file RULES_FILE_PATH.
        Raises:
            NoRuleSelectedInTableException: raise if no row was selected to
            delete.
        """
        try:
            selectedRule = self.view.getSelectedRow()
        except NoRuleSelectedInTableException as exception:
            logger.error(exception)
            displayCriticalMessage(exception)
            return

        rulesData = self.view.getSelectedRuleFromTable(selectedRule)

        weekday = rulesData["weekday"] if rulesData["weekday"].strip() \
            else None
        dayOfMonth = int(rulesData["dayOfMonth"]) if \
            rulesData["dayOfMonth"].strip() else None

        rule = Rule(
            rulesData["pathFrom"],
            rulesData["folderID"],
            rulesData["account"],
            rulesData["time"],
            weekday,
            dayOfMonth
        )

        try:
            self.ruleModel.deleteRule(rule)
        except PathToRulesFileDoesNotExistException as exception:
            logger.error(exception)
            displayCriticalMessage(exception)

        self.loadRulesToTable()

        # try:
        #     selectedRow = self.view.getSelectedRow()
        #     self.view.selectRow(selectedRow)
        # except NoRuleSelectedInTableException as exception:
        #     logger.error(exception)
        #     displayCriticalMessage(exception)
        #     return

    def deleteTokenFile(self) -> None:
        """
        Deletes token.json.
        Raises:
            TokenFileDoesNotExistException: raise if the token.json is not
            exist.
        """
        try:
            self.credentialsModel.deleteTokenFile()
        except TokenFileDoesNotExistException as exception:
            logger.error(exception)
            displayCriticalMessage(exception)

    def updateTable(self) -> None:
        """Updated the table."""
        self.loadRulesToTable()
