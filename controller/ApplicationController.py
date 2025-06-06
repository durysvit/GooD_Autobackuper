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

"""Module containing the main ApplicationController class."""

from view.MainWindow import MainWindow
from view.CreationRuleWindow import CreationRuleWindow
from model.Rule import Rule
from model.RuleRepository import RuleRepository
from model.CredentialsRepository import CredentialsRepository
from worker.FileCopyWorker import FileCopyWorker
from util.reportException import reportException
from controller.CreationRuleController import (
    CreationRuleController
)
from exception.exceptions import (
    NoRuleSelectedInTableException,
    TokenFileDoesNotExistException,
    ListOfRulesIsEmptyException,
    PathToRulesFileDoesNotExistException,
    MalformedRuleAttributesException,
)


class ApplicationController:
    """
    The class of the ApplicationController - the application controller binds
    windows, worker, models and services.
    """
    def __init__(self, view: MainWindow, ruleModel: RuleRepository,
                 credentialsModel: CredentialsRepository,
                 worker: FileCopyWorker, driveService):
        """
        Initializes a Rule instance with the given parameters.
        Args:
            view (MainWindow): is the main window.
            ruleModel (RuleRepository): is the rule management model.
            credentialsModel (CredentialsRepository): is the credentials
            management model.
            worker (FileCopyWorker): is the Google Drive backup worker.
            driveService: is the authorized service.
        """
        self.view = view
        self.ruleModel = ruleModel
        self.credentialsModel = credentialsModel
        self.worker = worker
        self.driveService = driveService

        self.view.createRulesButton.clicked.connect(
            self.displayCreationRuleWindow
        )
        self.view.deleteSelectedRuleButton.clicked.connect(
            self.deleteSelectedRuleFromTable
        )
        self.view.deleteTokenFileAction.triggered.connect(self.deleteTokenFile)
        self.view.updateTableAction.triggered.connect(self.updateTable)

        self.worker.updateSignal.connect(self.loadRulesToTable)
        self.worker.errorOccured.connect(self.handleWorkerError)
        self.worker.start()

    def displayCreationRuleWindow(self) -> None:
        """Displays the CreateRuleWindow."""
        creationRuleWindow = CreationRuleWindow(self.driveService)
        creationRuleController = CreationRuleController(
            self.ruleModel,
            creationRuleWindow
        )
        creationRuleWindow.exec_()

    def loadRulesToTable(self) -> None:
        """
        Loads rules to the table from RULES_FILE.
        Raises:
            PathToRulesFileDoesNotExistException: raises if path to rules file
            does not exist.
            MalformedRuleAttributesException: raises if the number of rule
            attributes is incorrect.
            ListOfRulesIsEmptyException: raises if the list of rules is empty.
        """
        self.view.resetTable()

        listOfRules = []
        try:
            listOfRules = self.ruleModel.loadRules()
        except (
            PathToRulesFileDoesNotExistException,
            MalformedRuleAttributesException,
        ) as exception:
            reportException(exception)

        try:
            self.view.addRulesToTable(listOfRules)
        except ListOfRulesIsEmptyException as exception:
            reportException(exception)

    def deleteSelectedRuleFromTable(self) -> None:
        """
        Deletes the selected rule from the table and file RULES_FILE_PATH.
        Raises:
            NoRuleSelectedInTableException: raise if no row was selected to
            delete.
            PathToRulesFileDoesNotExistException: raises if path to rules file
            does not exist.
            MalformedRuleAttributesException: raises if the number of rule
            attributes is incorrect.
        """
        selectedRow = 0
        try:
            selectedRow = self.view.getSelectedRow()
        except NoRuleSelectedInTableException as exception:
            reportException(exception)
            return

        rulesData = self.view.getSelectedRuleFromTable(selectedRow)

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
        except (
            PathToRulesFileDoesNotExistException,
            MalformedRuleAttributesException,
        ) as exception:
            reportException(exception)

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
            reportException(exception)

    def updateTable(self) -> None:
        """Updates the table."""
        self.loadRulesToTable()

    def handleWorkerError(self, exception) -> None:
        """Handles worker exceptions."""
        reportException(exception)
