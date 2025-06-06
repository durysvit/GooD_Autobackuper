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

"""Module containing the RuleRepository class."""

import os
import csv
from const.const import RULES_FILE_PATH, NUMBER_OF_RULE_ATTRIBUTES
from model.Rule import Rule
from exception.exceptions import (
    PathToRulesFileDoesNotExistException,
    MalformedRuleAttributesException,
)


class RuleRepository:
    """
    The model of the RuleRepository - the model manages the rules and the
    rules file.
    """
    def loadRules(self) -> list[Rule]:
        """
        Loads the rules to the list from RULES_FILE.
        Raises:
            PathToRulesFileDoesNotExistException: raises if path to rules file
            does not exist.
            MalformedRuleAttributesException: raises if the number of rule
            attributes is incorrect.
        Returns:
            list[Rule]: the list of rules from RULES_FILE.
        """
        if not os.path.exists(RULES_FILE_PATH):
            raise PathToRulesFileDoesNotExistException()

        PATH_FROM_ELEMENT = 0
        FOLDER_ID_ELEMNT = 1
        ACCOUNT_NAME_ELEMENT = 2
        TIME_ELEMENT = 3
        WEEKDAY_ELEMENT = 4
        DAY_OF_MONTH_ELEMENT = 5

        listOfRules = []
        with open(RULES_FILE_PATH, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < NUMBER_OF_RULE_ATTRIBUTES:
                    raise MalformedRuleAttributesException(row)

                weekday = row[WEEKDAY_ELEMENT] if \
                    row[WEEKDAY_ELEMENT].strip() else None
                dayOfMonth = None if not row[DAY_OF_MONTH_ELEMENT].strip() \
                    else int(row[DAY_OF_MONTH_ELEMENT])

                rule = Rule(
                    row[PATH_FROM_ELEMENT],
                    row[FOLDER_ID_ELEMNT],
                    row[ACCOUNT_NAME_ELEMENT],
                    row[TIME_ELEMENT],
                    weekday,
                    dayOfMonth
                )
                listOfRules.append(rule)

        return listOfRules

    def saveRules(self, listOfRules: list[Rule]) -> None:
        """
        Saves rules in RULES_FILE.
        Args:
            listOfRules (list[Rule]): the list of rules.
        Raises:
            PathToRulesFileDoesNotExistException: raises if path to rules file
            does not exist.
        """

        if not os.path.exists(RULES_FILE_PATH):
            raise PathToRulesFileDoesNotExistException()

        with open(RULES_FILE_PATH, mode='w', newline='') as file:
            for rule in listOfRules:
                csv.writer(file).writerow(rule.toRow())

    def deleteRule(self, rule: Rule) -> None:
        """
        Deletes the rule from RULE_FILE.
        Raises:
            MalformedRuleAttributesException: raises if the number of rule
            attributes is incorrect.
            PathToRulesFileDoesNotExistException: raises if path to rules file
            does not exist.
        """
        listOfRules = self.loadRules()
        filteredListOfRules = [i for i in listOfRules if i != rule]
        self.saveRules(filteredListOfRules)

    def saveUniqueRules(self, newRules: list[Rule]) -> None:
        """
        Saves the unique rules to RULE_FILE.
        Raises:
            MalformedRuleAttributesException: raises if the number of rule
            attributes is incorrect.
            PathToRulesFileDoesNotExistException: raises if path to rules file
            does not exist.
        """
        if not os.path.exists(RULES_FILE_PATH):
            raise PathToRulesFileDoesNotExistException()

        existingRules = self.loadRules()

        combinedRules = set(existingRules) | set(newRules)

        with open(RULES_FILE_PATH, mode='w', newline='') as file:
            writer = csv.writer(file)
            for rule in combinedRules:
                writer.writerow(rule.toRow())
