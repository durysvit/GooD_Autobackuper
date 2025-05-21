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

"""Module containing the MainWindow class."""

import os
import csv
# import Rule
from PyQt5.QtCore import QTimer, QEvent
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
    QHeaderView,
    QSizePolicy,
    QSystemTrayIcon
)
from worker.FileCopyWorker import FileCopyWorker
from window.CreationRuleWindow import CreationRuleWindow
from util.displayCriticalMessage import displayCriticalMessage
from logger.logger import logger
from const.const import (
    ICON_FILE,
    TOKEN_FILE,
    DATA_DIRECTORY,
    RULES_FILE
)
from exception.exceptions import (
    NoRowSelectedInTableException,
    TokenFileDoesNotExistException,
    ListOfRulesIsNoneException,
    ListOfRulesIsEmptyException,
    PathToRulesFileDoesNotExistException
)


class MainWindow(QMainWindow):
    """The class of main window."""
    def __init__(self):
        """Initialize the main window."""
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

        deleteTokenFileAction = QAction("&Delete token file", self)
        deleteTokenFileAction.triggered.connect(self.__deleteTokenFile)
        deleteTokenFileMenuPoint = QMenu("File", self)
        deleteTokenFileMenuPoint.addAction(deleteTokenFileAction)
        menuBar = self.menuBar()
        menuBar.addMenu(deleteTokenFileMenuPoint)

        NUMBER_OF_COLUMNS = 6
        NUMBER_OF_ROWS = 0
        self.table = QTableWidget(NUMBER_OF_ROWS, NUMBER_OF_COLUMNS)
        self.table.setHorizontalHeaderLabels(
            ["Path from", "Folder ID", "Account", "Time", "Weekday",
                "Day of month"]
        )

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        tableLayout.addWidget(self.table)

        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        addButton = QPushButton("&Add")
        deleteSelectedButton = QPushButton("&Delete")

        addButton.clicked.connect(self.addRuleToRulesFile)
        deleteSelectedButton.clicked.connect(
            self.__deleteSelectedRuleFromTable
        )

        buttonsLayout.addWidget(deleteSelectedButton)
        buttonsLayout.addWidget(addButton)

        mainLayout.addLayout(tableLayout)
        mainLayout.addLayout(buttonsLayout)

        self.setCentralWidget(centralWidget)

        self.__resizeWindowInHalfOfScreen()
        self.__centerWindow()
        self.loadRulesToTable()

        self.rules = list(self.__loadRulesForDrive())

        try:
            self.fileCopyWorker = FileCopyWorker(self.rules)
            self.fileCopyWorker.updateSignal.connect(self.loadRulesToTable)
            self.fileCopyWorker.start()
        except ListOfRulesIsNoneException:
            logger.error(str(ListOfRulesIsNoneException()))
        except ListOfRulesIsEmptyException:
            logger.error(str(ListOfRulesIsEmptyException()))

        ONE_SECOND_IN_MILLISECONDS = 1000
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadRulesToTable)
        self.timer.start(ONE_SECOND_IN_MILLISECONDS)

    def __resizeWindowInHalfOfScreen(self) -> None:
        """Resizes the window to half the screen size."""
        screen = QDesktopWidget().screenGeometry()

        HALF_SCREEN = 2
        halfOfScreenByWidth = screen.width() // HALF_SCREEN
        halfOfScreenByHeight = screen.height() // HALF_SCREEN

        NO_MOVE = 0
        self.setGeometry(NO_MOVE, NO_MOVE, halfOfScreenByWidth,
                         halfOfScreenByHeight)

    def __centerWindow(self) -> None:
        """Centers the window in screen."""
        frameGeometry = self.frameGeometry()
        frameGeometry.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(frameGeometry.topLeft())

    def addRuleToRulesFile(self) -> None:
        """Adds a rule to the RULES_FILE."""
        creationRuleWindow = CreationRuleWindow()
        creationRuleWindow.exec_()
        self.loadRulesToTable()

    def loadRulesToTable(self) -> None:
        """
        Loads rule to the table from RULES_FILE.
        Raises:
            FileExistsError: raise if RULES_FILE doesn't exist.
        """
        selectedRow = self.table.currentRow()
        RESET_TABLE = 0
        self.table.setRowCount(RESET_TABLE)
        if not os.path.exists(DATA_DIRECTORY):
            os.makedirs(DATA_DIRECTORY)
        if not os.path.exists(RULES_FILE):  # os.create_dir()
            with open(RULES_FILE, "w") as file:
                pass
            return
        with open(RULES_FILE, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                self.__addRuleToTable(row)
        NO_ROW_SELECTED = -1
        if selectedRow != NO_ROW_SELECTED:
            self.table.selectRow(selectedRow)

    def __addRuleToTable(self, row: list) -> None:  # Is it a list?
        """
        Adds rule to the table.
        Args:
            row: row consists of strings like "pathFrom,folderID,account,time".
        """
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        for column, data in enumerate(row):
            self.table.setItem(rowPosition, column, QTableWidgetItem(data))

    def __deleteSelectedRuleFromTable(self) -> None:
        """
        Deletes the selected rule from the table and file RULES_FILE.
        Raises:
            NoRowSelectedInTable: raise if no row was selected to delete.
        """
        selectedRow = self.table.currentRow()

        NO_ROW_SELECTED = -1
        if selectedRow == NO_ROW_SELECTED:
            message = str(NoRowSelectedInTableException())
            logger.error(message)
            displayCriticalMessage(message)
            return

        PATH_FROM_COLUMN = 0
        FOLDER_ID_COLUMN = 1
        ACCOUNT_NAME_COLUMN = 2
        TIME_COLUMN = 3
        WEEKDAY_COLUMN = 4
        DAY_OF_MONTH_COLUMN = 5

        # rule = Rule( # Rule week and Rule month

        # )

        pathFrom = self.table.item(selectedRow, PATH_FROM_COLUMN).text()
        folderID = self.table.item(selectedRow, FOLDER_ID_COLUMN).text()
        account = self.table.item(selectedRow, ACCOUNT_NAME_COLUMN).text()
        time = self.table.item(selectedRow, TIME_COLUMN).text()
        weekday = self.table.item(selectedRow, WEEKDAY_COLUMN).text()
        dayOfMonth = self.table.item(selectedRow, DAY_OF_MONTH_COLUMN).text()

        self.table.removeRow(selectedRow)
        self.__removeRuleFromRulesFile(
            pathFrom, folderID, account, time, weekday, dayOfMonth
        )
        self.loadRulesToTable()

    def __removeRuleFromRulesFile(self, pathFrom: str, folderID: str,
                                  account: str, time: str, weekday: str,
                                  dayOfMonth: str) -> None:
        """
        Deletes the selected rule from file RULES_FILE.
        Args:
            pathFrom (str): source path to copy from.
            folderID (str): target Google Drive folder ID.
            account (str): associated account name.
            time (str): time when the rule should be triggered.
            weekday (str): weekday when the rule should be triggered.
            dayOfMonth (str): day of month when the rule should be triggered.
        Raises:
            FileExistsError: raise if RULES_FILE doesn't exist.
        """
        rows = []
        listOfAttributes = [pathFrom, folderID, account, time, weekday,
                            dayOfMonth]
        if not os.path.exists(RULES_FILE):  # REMOVE
            message = str(PathToRulesFileDoesNotExistException())
            logger.error(message)
            displayCriticalMessage(message)
            return
        with open(RULES_FILE, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row != listOfAttributes:
                    rows.append(row)
        with open(RULES_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    def __loadRulesForDrive(self) -> list:
        """
        Loads rules into a list.
        Returns:
            list: list of rules.
        """
        rules = []
        if os.path.exists(RULES_FILE):
            with open(RULES_FILE, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    rules.append(row)
        return rules

    def closeApplication(self) -> None:
        """Ends the program."""
        QApplication.quit()

    def closeEvent(self, event: QEvent) -> None:
        """
        Hides the program when the program is closed.
        Args:
            event (QEvent): hides event.
        """
        event.ignore()
        self.hide()

    def iconClicked(self, reason) -> None:
        """
        Opens the window.
        Args:
            reason (...): ...
        """
        if reason == QSystemTrayIcon.Trigger:
            self.show()
            self.activateWindow()

    def __deleteTokenFile(self) -> None:
        """Deletes token.pickle if it exists."""
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)
            message = TOKEN_FILE + " is deleted."
            logger.info(message)
            displayCriticalMessage(message)
        else:
            message = str(TokenFileDoesNotExistException())
            logger.info(message)
            displayCriticalMessage(message)
            pass
