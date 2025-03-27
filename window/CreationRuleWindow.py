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

"""
The class of Creation rule window.
"""

import os
import csv
import const.const as const
from PyQt5.QtWidgets import (
    QDialog,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QTimeEdit,
    QLabel,
    QMessageBox,
    QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyle
from exception.EmptyLineEditException import EmptyLineEditException
from exception.EmptyTimeListException import EmptyTimeListException


class CreationRuleWindow(QDialog):
    """
    The class of creation rules of autobackup.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create rule")

        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint
        )

        self.pathFromInput = QLineEdit()

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
        layout.addWidget(self.confirmButton)

        self.setLayout(layout)

        self.timeList.installEventFilter(self)

    def addTime(self):
        """
        Adds unique value of the time to list.
        """

        timeValue = self.timeEdit.time().toString("HH:mm")

        timeList = [
            self.timeList.item(i).text() for i in range(
                self.timeList.count()
            )
        ]

        if timeValue not in timeList:
            self.timeList.addItem(timeValue)

    def confirmSelection(self):
        """
        Confirms, adds the rule to the file PATH_TO_RULES_CSV.
        Raises:
            EmptyLineEditInCreationRuleException: raise if one of lineEdit is
                 empty.
            EmptyTimeListException: raise if the time list is empty.
            FileExistsError: raise if path from doesn't exsist.
        """

        pathFrom = self.pathFromInput.text()
        folderID = self.folderIDInput.text()
        account = self.accountInput.text()
        times = [self.timeList.item(i).text() for i in range(
            self.timeList.count())]

        if not pathFrom.strip():
            QMessageBox.critical(
                None,
                "Error",
                str(EmptyLineEditException("Path from")),
                QMessageBox.Ok
            )
            return
        elif not os.path.exists(pathFrom):
            QMessageBox.critical(
                None,
                "Error",
                str(FileExistsError(
                    "FileExistsError: path from " + pathFrom +
                    " does not exist."
                )),
                QMessageBox.Ok
            )
            return
        elif not folderID.strip():
            QMessageBox.critical(
                None,
                "Error",
                str(EmptyLineEditException("Folder ID")),
                QMessageBox.Ok
            )
            return
        elif not account.strip():
            QMessageBox.critical(
                None,
                "Error",
                str(EmptyLineEditException("Account")),
                QMessageBox.Ok
            )
            return
        elif len(times) == 0:
            QMessageBox.critical(
                None,
                "Error",
                str(EmptyTimeListException()),
                QMessageBox.Ok
            )
            return

        existingEntries = set()

        if not os.path.exists(const.SOURCE_DIRECTORY):
            os.makedirs(const.SOURCE_DIRECTORY)

        if os.path.exists(const.PATH_TO_RULES_CSV):
            with open(const.PATH_TO_RULES_CSV, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    existingEntries.add(tuple(row))

        with open(const.PATH_TO_RULES_CSV, mode='a', newline='') as file:
            writer = csv.writer(file)
            for time in times:
                newEntry = (pathFrom, folderID, account, time)

                if newEntry not in existingEntries:
                    writer.writerow(newEntry)
                    existingEntries.add(newEntry)

        self.accept()

    def eventFilter(self, source, event):
        """
        Adds response to Delete key press and time selection in the table.
        """
        if source == self.timeList and event.type() == event.KeyPress:
            if event.key() == Qt.Key_Delete:
                self.removeSelectedTime()

        return super().eventFilter(source, event)

    def removeSelectedTime(self):
        """
        Removes selected time from the list of the time.
        """

        selectedItems = self.timeList.selectedItems()

        for item in selectedItems:
            self.timeList.takeItem(self.timeList.row(item))

    def selectFolder(self):
        """
        Selects folder.
        """

        folderPath = QFileDialog.getExistingDirectory(self, "Select Folder")

        if folderPath:
            self.pathFromInput.setText(folderPath)
