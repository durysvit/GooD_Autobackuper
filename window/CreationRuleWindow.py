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

"""Module containing the CreationRuleWindow class."""

import os
import csv
from PyQt5.QtWidgets import (
    QDialog,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QTimeEdit,
    QLabel,
    QFileDialog,
    QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyle
from util.displayCriticalMessage import displayCriticalMessage
from logger.logger import logger
from const.const import RULES_FILE
from exception.exceptions import (
    PathFromLineEditIsEmptyException,
    FolderIDLineEditIsEmptyException,
    AccountLineEditIsEmptyException,
    TimeListIsEmptyException,
)


class CreationRuleWindow(QDialog):
    """The class of creation rules of autobackup."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create rule")
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint
        )

        self.pathFromInput = QLineEdit()
        self.pathFromInput.setReadOnly(True)

        self.browseButton = QPushButton()
        self.browseButton.setIcon(
            self.style().standardIcon(QStyle.SP_DirOpenIcon)
        )
        self.browseButton.clicked.connect(self.selectFolder)

        self.folderIDInput = QLineEdit()
        self.accountInput = QLineEdit()

        self.timeEdit = QTimeEdit()
        self.timeEdit.setDisplayFormat("HH:mm")
        self.timeList = QListWidget()

        self.weekdayComboBox = QComboBox()
        self.weekdayComboBox.addItems(
            ['', "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                "Saturday", "Sunday"]
        )

        MIN_DAY_OF_MONTH = 1
        MAX_DAY_OF_MONTH = 31
        self.dayOfMonthComboBox = QComboBox()
        self.dayOfMonthComboBox.addItem('')
        self.dayOfMonthComboBox.addItems(
            [str(i) for i in range(MIN_DAY_OF_MONTH, MAX_DAY_OF_MONTH + 1)]
        )

        self.addButton = QPushButton("&Add", self)
        self.addButton.clicked.connect(self.addTime)

        self.confirmButton = QPushButton("&Confirm", self)
        self.confirmButton.clicked.connect(self.confirmSelection)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Path from:"))

        pathLayout = QHBoxLayout()
        pathLayout.addWidget(self.pathFromInput)
        pathLayout.addWidget(self.browseButton)

        layout.addLayout(pathLayout)
        layout.addWidget(QLabel("Folder ID:"))
        layout.addWidget(self.folderIDInput)
        layout.addWidget(QLabel("Account:"))
        layout.addWidget(self.accountInput)
        layout.addWidget(QLabel("Time:"))
        layout.addWidget(self.timeEdit)
        layout.addWidget(self.addButton)
        layout.addWidget(self.timeList)
        layout.addWidget(QLabel("Weekday:"))
        layout.addWidget(self.weekdayComboBox)
        layout.addWidget(QLabel("Day of month:"))
        layout.addWidget(self.dayOfMonthComboBox)
        layout.addWidget(self.confirmButton)

        self.weekdayComboBox.currentTextChanged.connect(self.toggleDayOfMonth)
        self.dayOfMonthComboBox.currentTextChanged.connect(self.toggleWeekday)
        self.setLayout(layout)
        self.timeList.installEventFilter(self)

    def addTime(self) -> None:
        """Adds unique value of the time to list."""
        timeValue = self.timeEdit.time().toString("HH:mm")
        timeList = [
            self.timeList.item(i).text() for i in range(
                self.timeList.count()
            )
        ]
        if timeValue not in timeList:
            self.timeList.addItem(timeValue)

    def confirmSelection(self) -> None:
        """
        Confirms, adds the rule to the file RULES_FILE.
        Raises:
            EmptyLineEditInCreationRuleException: raise if one of lineEdit is
            empty.
            EmptyTimeListException: raise if the time list is empty.
        """
        if not self.pathFromInput.text().strip():
            message = str(PathFromLineEditIsEmptyException())
            logger.error(message)
            displayCriticalMessage(message)
            return
        elif not self.folderIDInput.text().strip():
            message = str(FolderIDLineEditIsEmptyException()),
            logger.error(message)
            displayCriticalMessage(message)
            return
        elif not self.accountInput.text().strip():
            message = str(AccountLineEditIsEmptyException()),
            logger.error(message)
            displayCriticalMessage(message)
            return
        elif self.timeList.count() == 0:
            message = str(TimeListIsEmptyException()),
            logger.error(message)
            displayCriticalMessage(message)
            return

        pathFrom = self.pathFromInput.text()
        folderID = self.folderIDInput.text()
        account = self.accountInput.text()
        times = [
            self.timeList.item(i).text() for i in range(self.timeList.count())
        ]
        weekday = self.weekdayComboBox.currentText()
        dayOfMonth = self.dayOfMonthComboBox.currentText()

        existingEntries = set()
        if os.path.exists(RULES_FILE):
            with open(RULES_FILE, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    existingEntries.add(tuple(row))

        with open(RULES_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            for time in times:
                newEntry = (pathFrom, folderID, account, time, weekday,
                            dayOfMonth)
                if newEntry not in existingEntries:
                    writer.writerow(newEntry)
                    existingEntries.add(newEntry)

        self.accept()

    def eventFilter(self, source, event):  # docstrings
        """
        Adds response to Delete key press and time selection in the table.
        Args:
            source (...): ...
            event (...): ...
        """
        if source == self.timeList and event.type() == event.KeyPress:
            if event.key() == Qt.Key_Delete:
                self.removeSelectedTime()
        return super().eventFilter(source, event)

    def removeSelectedTime(self) -> None:
        """Removes selected time from the list of the time."""
        selectedItems = self.timeList.selectedItems()
        for item in selectedItems:
            self.timeList.takeItem(self.timeList.row(item))

    def selectFolder(self) -> None:
        """Selects folder."""
        folderPath = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folderPath:
            self.pathFromInput.setText(folderPath)

    def toggleDayOfMonth(self, text: str) -> None:
        """
        Disables dayOfMonthComboBox if weekday is selected, else enables it.
        """
        if text.strip():
            self.dayOfMonthComboBox.setDisabled(True)
        else:
            self.dayOfMonthComboBox.setDisabled(False)

    def toggleWeekday(self, text: str) -> None:
        """
        Disables weekdayComboBox if dayOfMonth is selected, else enables it.
        """
        if text.strip():
            self.weekdayComboBox.setDisabled(True)
        else:
            self.weekdayComboBox.setDisabled(False)
