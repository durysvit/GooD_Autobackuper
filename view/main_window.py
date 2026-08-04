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

from PyQt5.QtGui import QIcon, QCloseEvent
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
)
from model.Rule import Rule
from const.const import ICON_FILE
from exceptions.exceptions import (
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
        """Initializes the main window."""
        super().__init__()
        self.setWindowTitle("GooD Autobackuper")
        self.setWindowIcon(QIcon(ICON_FILE))

        NUMBER_OF_COLUMNS = 6
        NUMBER_OF_ROWS = 0
        self.table = QTableWidget(NUMBER_OF_ROWS, NUMBER_OF_COLUMNS)
        self.table.setHorizontalHeaderLabels(
            [
                "Path from",
                "Folder ID",
                "Account",
                "Time",
                "Weekday",
                "Day of month"
            ]
        )
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.create_rule_Button = QPushButton("&Create rules")
        self.delete_selected_rule_button = QPushButton("&Delete")

        table_layout = QVBoxLayout()
        table_layout.addWidget(self.table)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.delete_selected_rule_button)
        buttons_layout.addWidget(self.create_rule_Button)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.addLayout(table_layout)
        main_layout.addLayout(buttons_layout)

        self.exit_action = QAction("Exit", self)
        tray_menu = QMenu()
        tray_menu.addAction(self.exit_action)
        self.exit_action.triggered.connect(self.close_application)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(ICON_FILE))
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.iconClicked)
        self.tray_icon.show()

        self.delete_token_file_action = QAction("&Delete token file", self)
        delete_token_file_menu_point = QMenu("File", self)
        delete_token_file_menu_point.addAction(self.delete_token_file_action)
        self.update_table_action = QAction("&Update table", self)
        update_table_menu_point = QMenu("Table", self)
        update_table_menu_point.addAction(self.update_table_action)
        menu_bar = self.menuBar()
        menu_bar.addMenu(delete_token_file_menu_point)
        menu_bar.addMenu(update_table_menu_point)

        self.__resize_window_in_half_of_screen()
        self.__center_window()

    def add_rules_to_table(self, rules_list: list[Rule]) -> None:
        """
        Adds rules to the table.
        Args:
            rules_list (list[Rule]): is the list of rules.
        Raises:
            ListOfRulesIsEmptyException: raises if the list of rules is empty.
        """
        if not rules_list:
            raise ListOfRulesIsEmptyException()

        for rule in rules_list:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            self.table.setItem(row_position, self.PATH_FROM_COLUMN,
                               QTableWidgetItem(rule.path_from))
            self.table.setItem(row_position, self.FOLDER_ID_COLUMN,
                               QTableWidgetItem(rule.folder_id))
            self.table.setItem(row_position, self.ACCOUNT_NAME_COLUMN,
                               QTableWidgetItem(rule.account))
            self.table.setItem(row_position, self.TIME_COLUMN,
                               QTableWidgetItem(rule.time))
            self.table.setItem(row_position, self.WEEKDAY_COLUMN,
                               QTableWidgetItem(rule.weekday or ""))
            day_of_month = str(rule.day_of_month) \
                if rule.day_of_month is not None else ""
            self.table.setItem(row_position, self.DAY_OF_MONTH_COLUMN,
                               QTableWidgetItem(day_of_month))

    @staticmethod
    def close_application() -> None:
        """Ends the program."""
        QApplication.quit()

    def closeEvent(self, event: QCloseEvent | None) -> None:
        """Hides (tray) the program when the program is closed."""
        if event is not None:
            event.ignore()
        self.hide()

    def iconClicked(self, reason) -> None:
        """Opens the window."""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show()
            self.activateWindow()

    def get_selected_row(self) -> int:
        """
        Returns the selected row in the table.
        Raises:
            NoRuleSelectedInTableException: raise if no row was selected to
            delete.
        Returns:
            int: selected rules.
        """
        NO_RULE_SELECTED = -1
        selected_rule = self.table.currentRow()
        if selected_rule == NO_RULE_SELECTED:
            raise NoRuleSelectedInTableException()
        return selected_rule

    def get_selected_rule_from_table(self, selected_row: int) -> dict:
        """
        Returns the selected rules (data) from the table.
        Args:
            selected_row (int): the selected data from the table.
        Returns:
            dict: the dict of the rules from table.
        """
        return {
            "pathFrom": self.table.item(
                selected_row,
                self.PATH_FROM_COLUMN
            ).text(),
            "folderID": self.table.item(
                selected_row,
                self.FOLDER_ID_COLUMN
            ).text(),
            "account": self.table.item(
                selected_row,
                self.ACCOUNT_NAME_COLUMN
            ).text(),
            "time": self.table.item(selected_row, self.TIME_COLUMN).text(),
            "weekday": self.table.item(
                selected_row,
                self.WEEKDAY_COLUMN
            ).text(),
            "dayOfMonth": self.table.item(
                selected_row,
                self.DAY_OF_MONTH_COLUMN
            ).text()
        }

    def reset_table(self):
        """Resets the table."""
        RESET_TABLE = 0
        self.table.setRowCount(RESET_TABLE)

    def select_row(self, selected_row: int) -> None:
        """Selects the row in the table."""
        self.table.selectRow(selected_row)

    def __resize_window_in_half_of_screen(self) -> None:
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

    def __center_window(self) -> None:
        """Centers the window in screen."""
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(frame_geometry.topLeft())
