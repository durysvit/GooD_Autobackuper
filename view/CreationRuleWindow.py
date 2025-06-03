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
    QComboBox,
    QSpinBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyle


class CreationRuleWindow(QDialog):
    """The class of creation rules of autobackup."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create rule")
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint
        )

        self.pathFromInput = QLineEdit()
        self.pathFromInput.setPlaceholderText("Path from")
        self.pathFromInput.setReadOnly(True)

        self.browseButton = QPushButton()
        self.browseButton.setIcon(
            self.style().standardIcon(QStyle.SP_DirOpenIcon)
        )
        self.browseButton.clicked.connect(self.selectFolder)

        self.folderIDInput = QLineEdit()
        self.folderIDInput.setPlaceholderText("Folder ID")
        self.accountInput = QLineEdit()
        self.accountInput.setPlaceholderText("Account")

        self.timeEdit = QTimeEdit()
        self.timeEdit.setDisplayFormat("HH:mm")

        self.weekdayComboBox = QComboBox()
        self.weekdayComboBox.setPlaceholderText("Weekday")
        self.weekdayComboBox.addItems(
            ['', "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                "Saturday", "Sunday"]
        )

        MIN_DAY_OF_MONTH = 0
        MAX_DAY_OF_MONTH = 31
        self.dayOfMonthSpinBox = QSpinBox()
        self.dayOfMonthSpinBox.setMinimum(MIN_DAY_OF_MONTH)
        self.dayOfMonthSpinBox.setMaximum(MAX_DAY_OF_MONTH)

        self.addButton = QPushButton("&Add", self)
        self.addButton.clicked.connect(self.addTime)

        self.confirmButton = QPushButton("&Confirm", self)

        pathLayout = QHBoxLayout()
        pathLayout.addWidget(self.pathFromInput)
        pathLayout.addWidget(self.browseButton)

        layout = QVBoxLayout()
        layout.addLayout(pathLayout)
        layout.addWidget(self.folderIDInput)
        layout.addWidget(self.accountInput)
        layout.addWidget(self.timeEdit)
        layout.addWidget(self.addButton)

        self.timeList = QListWidget()
        layout.addWidget(self.timeList)

        layout.addWidget(QLabel("Weekday:"))
        layout.addWidget(self.weekdayComboBox)
        layout.addWidget(QLabel("Day of month:"))
        layout.addWidget(self.dayOfMonthSpinBox)
        layout.addWidget(self.confirmButton)

        self.weekdayComboBox.currentTextChanged.connect(self.toggleDayOfMonth)
        self.dayOfMonthSpinBox.valueChanged.connect(self.toggleWeekday)
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

    def eventFilter(self, source, event):
        """
        Adds response to Delete key press and time selection in the table.
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

    def toggleWeekday(self, value: int) -> None:
        """
        Disables weekdayComboBox if dayOfMonth is selected, else enables it.
        Args:
            value (int): is the number of month or 0.
        """
        if value != 0:
            self.weekdayComboBox.setDisabled(True)
        else:
            self.weekdayComboBox.setDisabled(False)

    def toggleDayOfMonth(self, text: str) -> None:
        """
        Disables dayOfMonthSpinBox if weekday is selected, else enables it.
        Args:
            text (str): is the name of weekday or empty string.
        """
        if text.strip():
            self.dayOfMonthSpinBox.setDisabled(True)
        else:
            self.dayOfMonthSpinBox.setDisabled(False)

    def getInputs(self) -> dict:
        return {
            "pathFrom": self.pathFromInput.text().strip(),
            "folderID": self.folderIDInput.text().strip(),
            "account": self.accountInput.text().strip(),
            "timeList": [
                self.timeList.item(i).text() for i in range(
                    self.timeList.count()
                )
            ],
            "weekday": self.weekdayComboBox.currentText(),
            "dayOfMonth": int(self.dayOfMonthSpinBox.text())
        }
