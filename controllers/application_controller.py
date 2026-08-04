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

from view.main_window import MainWindow
from view.creation_rule_window import CreationRuleWindow
from model.Rule import Rule
from model.repositories.RuleRepository import RuleRepository
from model.repositories.CredentialsRepository import CredentialsRepository
from worker.file_copy_worker import FileCopyWorker
from util.report_exception import report_exception
from controllers.creation_rule_controller import (
    CreationRuleController
)
from exceptions.exceptions import (
    NoRuleSelectedInTableException,
    TokenFileDoesNotExistException,
    ListOfRulesIsEmptyException,
    PathToRulesFileDoesNotExistException,
    MalformedRuleAttributesException,
)


class ApplicationController:
    """
    The class of the ApplicationController - the application controllers binds
    windows, worker, models and services.
    """
    def __init__(self, view: MainWindow, rule_model: RuleRepository,
                 credentials_model: CredentialsRepository,
                 worker: FileCopyWorker, drive_service):
        """
        Initializes a Rule instance with the given parameters.
        Args:
            view (MainWindow): is the main window.
            rule_model (RuleRepository): is the rules management model.
            credentials_model (CredentialsRepository): is the credentials
            management model.
            worker (FileCopyWorker): is the Google Drive backup worker.
            drive_service: is the authorized service.
        """
        self.view = view
        self.rule_model = rule_model
        self.credentials_model = credentials_model
        self.worker = worker
        self.drive_service = drive_service

        self.view.create_rule_Button.clicked.connect(
            self.display_creation_rule_window
        )
        self.view.delete_selected_rule_button.clicked.connect(
            self.delete_selected_rule_from_table
        )
        self.view.delete_token_file_action.triggered.connect(
            self.delete_token_file
        )
        self.view.update_table_action.triggered.connect(self.update_table)

        self.worker.update_signal.connect(self.load_rules_to_table)
        self.worker.error_occurred.connect(self.handle_worker_error)
        self.worker.start()

    def display_creation_rule_window(self) -> None:
        """Displays the CreateRuleWindow."""
        creation_rule_window = CreationRuleWindow(self.drive_service)
        CreationRuleController(
            self.rule_model,
            creation_rule_window
        )
        creation_rule_window.exec_()

    def load_rules_to_table(self) -> None:
        """
        Loads rules to the table from RULES_FILE.
        Raises:
            PathToRulesFileDoesNotExistException: raises if path to rules file
            does not exist.
            MalformedRuleAttributesException: raises if the number of rules
            attributes is incorrect.
            ListOfRulesIsEmptyException: raises if the list of rules is empty.
        """
        self.view.reset_table()

        rules_list = []
        try:
            rules_list = self.rule_model.load_rules()
        except (
            PathToRulesFileDoesNotExistException,
            MalformedRuleAttributesException,
        ) as exception:
            report_exception(exception)

        try:
            self.view.add_rules_to_table(rules_list)
        except ListOfRulesIsEmptyException as exception:
            report_exception(exception)

    def delete_selected_rule_from_table(self) -> None:
        """
        Deletes the selected rules from the table and file RULES_FILE_PATH.
        Raises:
            NoRuleSelectedInTableException: raise if no row was selected to
            delete.
            PathToRulesFileDoesNotExistException: raises if path to rules file
            does not exist.
            MalformedRuleAttributesException: raises if the number of rules
            attributes is incorrect.
        """
        selected_row = 0
        try:
            selected_row = self.view.get_selected_row()
        except NoRuleSelectedInTableException as exception:
            report_exception(exception)
            return

        rules_data = self.view.get_selected_rule_from_table(selected_row)

        weekday = rules_data["weekday"] if rules_data["weekday"].strip() \
            else None
        day_of_month = int(rules_data["day_of_month"]) if \
            rules_data["day_of_month"].strip() else None

        rule = Rule(
            rules_data["pathFrom"],
            rules_data["folderID"],
            rules_data["account"],
            rules_data["time"],
            weekday,
            day_of_month
        )

        try:
            self.rule_model.delete_rule(rule)
        except (
            PathToRulesFileDoesNotExistException,
            MalformedRuleAttributesException,
        ) as exception:
            report_exception(exception)

    def delete_token_file(self) -> None:
        """
        Deletes token.json.
        Raises:
            TokenFileDoesNotExistException: raise if the token.json is not
            exist.
        """
        try:
            self.credentials_model.delete_token_file()
        except TokenFileDoesNotExistException as exception:
            report_exception(exception)

    def update_table(self) -> None:
        """Updates the table."""
        self.load_rules_to_table()

    def handle_worker_error(self, exception) -> None:
        """Handles worker exceptions."""
        report_exception(exception)
