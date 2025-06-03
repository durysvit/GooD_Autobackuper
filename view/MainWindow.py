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
    QSystemTrayIcon,
    QAbstractItemView,
    QAbstractScrollArea,
)
from model.Rule import Rule
from worker.FileCopyWorker import FileCopyWorker
from const.const import ICON_FILE
from exception.exceptions import (
    ListOfRulesIsEmptyException,
    NoRuleSelectedInTableException
)


class MainWindow(QMainWindow):
    """The class of main window."""
    PATH_FROM_COLUMN = 0
    FOLDER_ID_COLUMN = 1
    ACCOUNT_NAME_COLUMN = 2
    TIME_COLUMN = 3
    WEEKDAY_COLUMN = 4
    DAY_OF_MONTH_COLUMN = 5

    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.setWindowTitle("GooD Autobackuper")
        self.setWindowIcon(QIcon(ICON_FILE))

        NUMBER_OF_COLUMNS = 6
        NUMBER_OF_ROWS = 0
        self.table = QTableWidget(NUMBER_OF_ROWS, NUMBER_OF_COLUMNS)
        self.table.setHorizontalHeaderLabels(
            ["Path from", "Folder ID", "Account", "Time", "Weekday",
             "Day of month"]
        )
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.createRulesButton = QPushButton("&Create rules")
        self.deleteSelectedRuleButton = QPushButton("&Delete")

        tableLayout = QVBoxLayout()
        tableLayout.addWidget(self.table)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.deleteSelectedRuleButton)
        buttonsLayout.addWidget(self.createRulesButton)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        mainLayout = QVBoxLayout(centralWidget)
        mainLayout.addLayout(tableLayout)
        mainLayout.addLayout(buttonsLayout)

        self.exitAction = QAction("Exit", self)
        trayMenu = QMenu()
        trayMenu.addAction(self.exitAction)
        self.exitAction.triggered.connect(self.closeApplication)
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon(ICON_FILE))
        self.trayIcon.setContextMenu(trayMenu)
        self.trayIcon.activated.connect(self.iconClicked)
        self.trayIcon.show()

        self.deleteTokenFileAction = QAction("&Delete token file", self)
        deleteTokenFileMenuPoint = QMenu("File", self)
        deleteTokenFileMenuPoint.addAction(self.deleteTokenFileAction)
        self.updateTableAction = QAction("&Update table", self)
        updateTableMenuPoint = QMenu("Table", self)
        updateTableMenuPoint.addAction(self.updateTableAction)
        menuBar = self.menuBar()
        menuBar.addMenu(deleteTokenFileMenuPoint)
        menuBar.addMenu(updateTableMenuPoint)

        self.__resizeWindowInHalfOfScreen()
        self.__centerWindow()
        # self.controller.loadRulesToTable()

        # rules = list(

        # self.fileCopyWorker = FileCopyWorker(rules)
        # self.fileCopyWorker.start()

        # ONE_SECOND_IN_MILLISECONDS = 1000
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.controller.loadRulesToTable)  # replace
        # self.timer.start(ONE_SECOND_IN_MILLISECONDS)

    def addRulesToTable(self, listOfRules: list[Rule]) -> None:
        """
        Adds rules to the table.
        Args:
            listOfRules (list[Rule]): is the list of rules.
        """
        if not listOfRules:
            raise ListOfRulesIsEmptyException()

        for rule in listOfRules:
            rowPosition = self.table.rowCount()
            self.table.insertRow(rowPosition)

            self.table.setItem(rowPosition, self.PATH_FROM_COLUMN,
                               QTableWidgetItem(rule.pathFrom))
            self.table.setItem(rowPosition, self.FOLDER_ID_COLUMN,
                               QTableWidgetItem(rule.folderID))
            self.table.setItem(rowPosition, self.ACCOUNT_NAME_COLUMN,
                               QTableWidgetItem(rule.account))
            self.table.setItem(rowPosition, self.TIME_COLUMN,
                               QTableWidgetItem(rule.time))
            self.table.setItem(rowPosition, self.WEEKDAY_COLUMN,
                               QTableWidgetItem(rule.weekday or ""))
            dayOfMonth = str(rule.dayOfMonth) if rule.dayOfMonth is not None \
                else ""
            self.table.setItem(rowPosition, self.DAY_OF_MONTH_COLUMN,
                               QTableWidgetItem(dayOfMonth))

    def closeApplication(self) -> None:
        """Ends the program."""
        QApplication.quit()

    def closeEvent(self, event: QEvent) -> None:
        """Hides the program when the program is closed."""
        event.ignore()
        self.hide()

    def iconClicked(self, reason) -> None:
        """Opens the window."""
        if reason == QSystemTrayIcon.Trigger:
            self.show()
            self.activateWindow()

    def getSelectedRow(self):
        """..."""
        NO_RULE_SELECTED = -1
        selectedRule = self.table.currentRow()
        if selectedRule == NO_RULE_SELECTED:
            raise NoRuleSelectedInTableException()
        return selectedRule

    def getSelectedRuleFromTable(self, selectedRow: int) -> Rule:
        """..."""
        return {
            "pathFrom": self.table.item(
                selectedRow,
                self.PATH_FROM_COLUMN
            ).text(),
            "folderID": self.table.item(
                selectedRow,
                self.FOLDER_ID_COLUMN
            ).text(),
            "account": self.table.item(
                selectedRow,
                self.ACCOUNT_NAME_COLUMN
            ).text(),
            "time": self.table.item(selectedRow, self.TIME_COLUMN).text(),
            "weekday": self.table.item(
                selectedRow,
                self.WEEKDAY_COLUMN
            ).text(),
            "dayOfMonth": self.table.item(
                selectedRow,
                self.DAY_OF_MONTH_COLUMN
            ).text()
        }

    def resetTable(self):
        RESET_TABLE = 0
        self.table.setRowCount(RESET_TABLE)

    def selectRow(self, selectedRow: int) -> None:
        self.table.selectRow(selectedRow)

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
