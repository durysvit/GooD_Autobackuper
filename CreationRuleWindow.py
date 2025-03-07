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

import os
import csv
from PyQt5.QtWidgets import (
    QDialog,
    QPushButton, 
    QVBoxLayout, 
    QLineEdit,
    QListWidget,
    QTimeEdit,
    QLabel,
    QMessageBox
)
from PyQt5.QtCore import Qt
from exception.EmptyLineEditException import *
from exception.EmptyTimeListException import *

SOURCE_DIRECTORY = "./source"
PATH_TO_RULES_CSV = SOURCE_DIRECTORY + "/rules.csv"

# The class of creation rules of autobackup.
class CreationRuleWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create rule")

        self.setWindowFlags(self.windowFlags() &
             ~Qt.WindowType.WindowContextHelpButtonHint)

        self.pathFromInput = QLineEdit()
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
        layout.addWidget(self.pathFromInput)
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

    # Adds unique value of the time to list.
    def addTime(self):
        timeValue = self.timeEdit.time().toString("HH:mm")
        
        timeList = [
            self.timeList.item(i).text() for i in range(
                self.timeList.count()
            )
        ]
        
        if timeValue not in timeList: 
            self.timeList.addItem(timeValue)

    # Confirms, adds the rule to the file PATH_TO_RULES_CSV.
    # Thrown EmptyLineEditInCreationRuleException if one of lineEdit is empty. 
    # Thrown EmptyTimeListException if the time list is empty.
    # Thrown FileExistsError if path from doesn't exsist.
    def confirmSelection(self):
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
                str(FileExistsError("FileExistsError: path from " +
                    pathFrom + " does not exist.")),
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
        
        if not os.path.exists(SOURCE_DIRECTORY):
            os.makedirs(SOURCE_DIRECTORY)

        if os.path.exists(PATH_TO_RULES_CSV):
            with open(PATH_TO_RULES_CSV, mode="r", newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    existingEntries.add(tuple(row))

        with open(PATH_TO_RULES_CSV, mode='a', newline='') as file:
            writer = csv.writer(file)
            for time in times:
                newEntry = (pathFrom, folderID, account, time)

                if newEntry not in existingEntries:
                    writer.writerow(newEntry)
                    existingEntries.add(newEntry)

        self.accept() 

    # Adds response to Delete key press and time selection in the table.
    def eventFilter(self, source, event):
        if source == self.timeList and event.type() == event.KeyPress:
            if event.key() == Qt.Key_Delete:
                self.removeSelectedTime()

        return super().eventFilter(source, event)

    # Removes selected time from the list of the time.
    def removeSelectedTime(self):
        selectedItems = self.timeList.selectedItems()

        for item in selectedItems:
            self.timeList.takeItem(self.timeList.row(item))
