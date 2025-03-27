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
Class of main window.
"""

import os
import csv
import const.const as const
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
    QMessageBox,
    QHeaderView,
    QSizePolicy,
    QSystemTrayIcon
)
from worker.FileCopyWorker import FileCopyWorker
from window.CreationRuleWindow import CreationRuleWindow
from exception.NoRowSelectedInTableException import (
    NoRowSelectedInTableException
)


class MainWindow(QMainWindow):
    """The class of main window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("GooD Autobackuper")
        self.setWindowIcon(QIcon(const.ICON_FILE))

        centralWidget = QWidget()
        mainLayout = QVBoxLayout(centralWidget)
        tableLayout = QVBoxLayout()
        buttonsLayout = QHBoxLayout()

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon(const.ICON_FILE))

        trayMenu = QMenu()

        exitAction = QAction("Exit", self)
        exitAction.triggered.connect(self.closeApplication)
        trayMenu.addAction(exitAction)

        self.trayIcon.setContextMenu(trayMenu)
        self.trayIcon.show()

        self.trayIcon.activated.connect(self.iconClicked)

        NUMBER_OF_COLUMNS = 4
        NUMBER_OF_ROWS = 0

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

    def resizeWindowInHalfOfScreen(self):
        """Resizes the window to half the screen size."""

        screen = QDesktopWidget().screenGeometry()

        HALF_SCREEN = 2

        halfOfScreenByWidth = screen.width() // HALF_SCREEN
        halfOfScreenByHeight = screen.height() // HALF_SCREEN

        NO_MOVE = 0

        self.setGeometry(
            NO_MOVE,
            NO_MOVE,
            halfOfScreenByWidth,
            halfOfScreenByHeight
        )

    def centerWindow(self):
        """Centers the window in screen."""

        frameGeometry = self.frameGeometry()

        frameGeometry.moveCenter(QDesktopWidget().availableGeometry().center())

        self.move(frameGeometry.topLeft())

    def addRuleToRulesFile(self):
        """Adds a rule to the PATH_TO_RULES_CSV."""

        creationRuleWindow = CreationRuleWindow()

        creationRuleWindow.exec_()

        self.loadRulesToTable()

    def loadRulesToTable(self):
        """
        Loads rule to the table from PATH_TO_RULES_CSV.
        Raises:
            FileExistsError: raise if PATH_TO_RULES_CSV doesn't exsist.
        """

        selectedRow = self.table.currentRow()

        RESET_TABLE = 0

        self.table.setRowCount(RESET_TABLE)

        if not os.path.exists(const.SOURCE_DIRECTORY):
            os.makedirs(const.SOURCE_DIRECTORY)

        if not os.path.exists(const.PATH_TO_RULES_CSV):
            with open(const.PATH_TO_RULES_CSV, 'w') as file:
                pass

            return

        with open(const.PATH_TO_RULES_CSV, mode="r", newline='') as file:
            reader = csv.reader(file)

            for row in reader:
                self.addRuleToTable(row)

        NO_ROW_SELECTED = -1

        if selectedRow != NO_ROW_SELECTED:
            self.table.selectRow(selectedRow)

    def addRuleToTable(self, row):
        """
        Adds rule to the table.
        Args:
            row: row consists of strings like "pathFrom,folderID,account,
                time".
        """

        rowPosition = self.table.rowCount()

        self.table.insertRow(rowPosition)

        for column, data in enumerate(row):
            self.table.setItem(rowPosition, column, QTableWidgetItem(data))

    def deleteSelectedRuleFromTable(self):
        """
        Deletes the selected rule from the table and file PATH_TO_RULES_CSV.
        Raises:
            NoRowSelectedInTable: raise if no row was selected to delete.
        """

        selectedRow = self.table.currentRow()

        NO_ROW_SELECTED = -1

        if selectedRow == NO_ROW_SELECTED:
            QMessageBox.critical(
                None,
                "Error",
                str(NoRowSelectedInTableException()),
                QMessageBox.Ok
            )
            return

        PATH_FROM_COLUMN = 0
        FOLDER_ID_COLUMN = 1
        ACCOUNT_NAME_COLUMN = 2
        TIME_COLUMN = 3

        pathFrom = self.table.item(selectedRow, PATH_FROM_COLUMN).text()
        pathTo = self.table.item(selectedRow, FOLDER_ID_COLUMN).text()
        account = self.table.item(selectedRow, ACCOUNT_NAME_COLUMN).text()
        time = self.table.item(selectedRow, TIME_COLUMN).text()

        self.table.removeRow(selectedRow)

        self.removeRuleFromRulesFile(pathFrom, pathTo, account, time)

        self.loadRulesToTable()

    def removeRuleFromRulesFile(self, pathFrom, pathTo, account, time):
        """
        Deletes the selected rule from file PATH_TO_RULES_CSV.
        Raises:
            FileExistsError: raise if PATH_TO_RULES_CSV doesn't exsist.
        """

        rows = []

        if not os.path.exists(const.PATH_TO_RULES_CSV):
            QMessageBox.critical(
                None,
                "Error",
                str(FileExistsError("FileExistsError: " +
                    const.PATH_TO_RULES_CSV +
                    " does not exsist.")),
                QMessageBox.Ok
            )
            return

        with open(const.PATH_TO_RULES_CSV, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row != [pathFrom, pathTo, account, time]:
                    rows.append(row)

        with open(const.PATH_TO_RULES_CSV, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    def loadRulesForDrive(self):
        """
        Loads rules into a list.
        Returns:
            list: list of rules.
        """

        rules = []

        if os.path.exists(const.PATH_TO_RULES_CSV):
            with open(const.PATH_TO_RULES_CSV, mode='r', newline='') as file:
                reader = csv.reader(file)

                for row in reader:
                    rules.append(row)

        return rules

    def closeApplication(self):
        """
        Ends the program.
        """

        QApplication.quit()

    def closeEvent(self, event):
        """
        Hides the program when the program is closed.
        """

        event.ignore()
        self.hide()

    def iconClicked(self, reason):
        """
        Opens the window.
        """

        if reason == QSystemTrayIcon.Trigger:
            self.show()
            self.activateWindow()
