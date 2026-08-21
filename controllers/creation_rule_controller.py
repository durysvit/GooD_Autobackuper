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

"""Module containing the CreationRuleController class."""

from views.creation_rule_window import CreationRuleWindow
from core.model import Rule
from repositories.rule_repository import RuleRepository
from util.report_exception import report_exception
from exceptions.exceptions import (
    PathFromLineEditIsEmptyException,
    FolderIDLineEditIsEmptyException,
    AccountLineEditIsEmptyException,
    TimeListIsEmptyException,
)


class CreationRuleController:
    def __init__(self, model: RuleRepository, view: CreationRuleWindow):
        self.model = model
        self.view = view

        self.view.confirm_button.clicked.connect(self.add_rules)

    def add_rules(self) -> None:
        """
        Adds the rules to the file RULES_FILE_PATH.
        Raises:
            PathFromLineEditIsEmptyException: the path from line edit is empty.
            FolderIDLineEditIsEmptyException: the folder ID line dit is empty.
            AccountLineEditIsEmptyException: the account line edit is empty.
            TimeListIsEmptyException: the time list line edit is empty.
        """
        try:
            list_of_rules = self.get_rule_data()
            self.model.save_unique_rules(list_of_rules)
            self.view.accept()
        except (
            PathFromLineEditIsEmptyException,
            FolderIDLineEditIsEmptyException,
            AccountLineEditIsEmptyException,
            TimeListIsEmptyException
        ) as exception:
            report_exception(exception)

    def get_rule_data(self) -> list[Rule]:
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
            rules_list (list[Rule]): list of rules.
        """
        inputs = self.view.get_inputs()

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
        day_of_month = inputs["day_of_month"] if inputs["day_of_month"] != 0 \
            else None
        rules_list = []

        for time in inputs["timeList"]:
            rule = Rule(
                inputs["pathFrom"],
                inputs["folderID"],
                inputs["account"],
                time,
                weekday,
                day_of_month
            )
            rules_list.append(rule)

        return rules_list
