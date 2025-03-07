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
import shutil
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget, 
    QPushButton, 
    QVBoxLayout, 
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QMenu,
    QAction,
    QDesktopWidget,
    QDialog,
    QMessageBox,
    QHeaderView,
    QSizePolicy,
    QSystemTrayIcon
)
from FileCopyWorker import *
from CreationRuleWindow import *
from exception.NoRowSelectedInTableException import *

ICON_FILE = "GooD_Autobackuper.svg"

# The class of main window.
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GooD Autobackuper")
        self.setWindowIcon(QIcon(ICON_FILE))

        centralWidget = QWidget()
        mainLayout = QVBoxLayout(centralWidget)
        tableLayout = QVBoxLayout()
        buttonsLayout = QHBoxLayout()

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon(ICON_FILE))

        trayMenu = QMenu()

        exitAction = QAction("Exit", self)
        exitAction.triggered.connect(self.closeApplication)
        trayMenu.addAction(exitAction)

        self.trayIcon.setContextMenu(trayMenu)
        self.trayIcon.show()

        self.trayIcon.activated.connect(self.iconClicked)

        NUMBER_OF_COLUMNS = 4; NUMBER_OF_ROWS = 0

        self.table = QTableWidget(NUMBER_OF_ROWS, NUMBER_OF_COLUMNS)
        self.table.setHorizontalHeaderLabels(
            ["Path from", "Folder ID", "Account", "Time"]
        )

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        tableLayout.addWidget(self.table)

        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        addButton = QPushButton("&Add")
        deleteSelectedButton = QPushButton("&Delete")

        addButton.clicked.connect(self.addRuleToRulesFile)
        deleteSelectedButton.clicked.connect(self.deleteSelectedRuleFromTable)

        buttonsLayout.addWidget(deleteSelectedButton)
        buttonsLayout.addWidget(addButton)

        mainLayout.addLayout(tableLayout)
        mainLayout.addLayout(buttonsLayout)

        self.setCentralWidget(centralWidget)

        self.resizeWindowInHalfOfScreen()
        self.centerWindow()
        self.loadRulesToTable()

        self.rules = self.loadRulesForDrive()

        self.fileCopyWorker = FileCopyWorker(self.rules)
        self.fileCopyWorker.updateSignal.connect(self.loadRulesToTable)
        self.fileCopyWorker.start()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadRulesToTable)

        ONE_SECOND_IN_MILLISECONDS = 1000

        self.timer.start(ONE_SECOND_IN_MILLISECONDS)

    # Resizes the window to half the screen size.
    def resizeWindowInHalfOfScreen(self):
        HALF_SCREEN = 2; NO_MOVE = 0

        screen = QDesktopWidget().screenGeometry()

        halfOfScreenByWidth = screen.width() // HALF_SCREEN
        halfOfScreenByHeight = screen.height() // HALF_SCREEN

        self.setGeometry(NO_MOVE, NO_MOVE, halfOfScreenByWidth,
            halfOfScreenByHeight)

    # Centers the window in screen.
    def centerWindow(self):
        frameGeometry = self.frameGeometry()

        frameGeometry.moveCenter(QDesktopWidget().availableGeometry().center())

        self.move(frameGeometry.topLeft())

    # Adds a rule to the PATH_TO_RULES_CSV.
    def addRuleToRulesFile(self):
        creationRuleWindow = CreationRuleWindow()

        creationRuleWindow.exec_()

        self.loadRulesToTable()

    # Loads rule to the table from PATH_TO_RULES_CSV.
    # Thrown FileExistsError if PATH_TO_RULES_CSV doesn't exsist.
    def loadRulesToTable(self):
        RESET_TABLE = 0; NO_ROW_SELECTED = -1

        selectedRow = self.table.currentRow()

        self.table.setRowCount(RESET_TABLE)

        if not os.path.exists(SOURCE_DIRECTORY):
            os.makedirs(SOURCE_DIRECTORY)

        if not os.path.exists(PATH_TO_RULES_CSV):
            with open(PATH_TO_RULES_CSV, 'w') as file:
                pass

            return

        with open(PATH_TO_RULES_CSV, mode="r", newline='') as file:
            reader = csv.reader(file)

            for row in reader:
                self.addRuleToTable(row)
        
        if selectedRow != NO_ROW_SELECTED:
            self.table.selectRow(selectedRow)

    # Adds rule to the table.
    # Parameter row consists of strings like "pathFrom,folderID,account,time".
    def addRuleToTable(self, row):
        rowPosition = self.table.rowCount()

        self.table.insertRow(rowPosition)

        for column, data in enumerate(row):
            self.table.setItem(rowPosition, column, QTableWidgetItem(data))

    # Deletes the selected rule from the table and file PATH_TO_RULES_CSV.
    # Thrown NoRowSelectedInTable if no row was selected to delete.
    def deleteSelectedRuleFromTable(self):
        NO_ROW_SELECTED = -1; PATH_FROM_COLUMN = 0; FOLDER_ID_COLUMN = 1
        ACCOUNT_NAME_COLUMN = 2; TIME_COLUMN = 3

        selectedRow = self.table.currentRow()

        if selectedRow == NO_ROW_SELECTED:
            QMessageBox.critical(
                None,
                "Error",
                str(NoRowSelectedInTableException()), 
                QMessageBox.Ok
            )
            return

        pathFrom = self.table.item(selectedRow, PATH_FROM_COLUMN).text()
        pathTo = self.table.item(selectedRow, FOLDER_ID_COLUMN).text()
        account = self.table.item(selectedRow, ACCOUNT_NAME_COLUMN).text()
        time = self.table.item(selectedRow, TIME_COLUMN).text()

        self.table.removeRow(selectedRow)

        self.removeRuleFromRulesFile(pathFrom, pathTo, account, time)

        self.loadRulesToTable()

    # Deletes the selected rule from file PATH_TO_RULES_CSV.
    # Thrown FileExistsError if PATH_TO_RULES_CSV doesn't exsist.
    def removeRuleFromRulesFile(self, pathFrom, pathTo, account, time):
        rows = []

        if not os.path.exists(PATH_TO_RULES_CSV):
            QMessageBox.critical(
                None,
                "Error",
                str(FileExistsError("FileExistsError: " + PATH_TO_RULES_CSV +
                    " does not exsist.")),
                QMessageBox.Ok
            )
            return

        with open(PATH_TO_RULES_CSV, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row != [pathFrom, pathTo, account, time]:
                    rows.append(row)

        with open(PATH_TO_RULES_CSV, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
    
    # Loads rules into a list.
    def loadRulesForDrive(self):
        rules = []

        if os.path.exists(PATH_TO_RULES_CSV):
            with open(PATH_TO_RULES_CSV, mode='r', newline='') as file:
                reader = csv.reader(file)

                for row in reader:
                    rules.append(row)

        return rules
    
    # Ends the program.
    def closeApplication(self):
       QApplication.quit() 
    
    # Hides the program when the program is closed.
    def closeEvent(self, event):
        event.ignore()
        self.hide()

    # Opens the window.
    def iconClicked(self, reason):
        if reason == QSystemTrayIcon.Trigger:  
            self.show()
            self.activateWindow()