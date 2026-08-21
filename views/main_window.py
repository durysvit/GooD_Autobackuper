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

from PySide6.QtGui import QIcon, QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QMenu,
    QHeaderView,
    QSizePolicy,
    QSystemTrayIcon,
    QAbstractItemView,
)
from PySide6.QtGui import QAction
from core.model.Rule import Rule
from const.const import ICON_FILE
from exceptions.exceptions import (
    ListOfRulesIsEmptyException,
    NoRuleSelectedInTableException
)
from core.enums.TableColumn import TableColumn


class MainWindow(QMainWindow):
    """The class of main window."""
    def __init__(self):
        """Initializes the main window."""
        super().__init__()
        self.setWindowTitle("GooD Autobackuper")
        self.setWindowIcon(QIcon(ICON_FILE))

        self.table = QTableWidget(0, len(TableColumn))
        self.table.setHorizontalHeaderLabels(TableColumn.labels())
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
        self.tray_icon.activated.connect(self.icon_clicked)
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

            self.table.setItem(
                row_position,
                TableColumn.PATH_FROM,
                QTableWidgetItem(rule.path_from)
            )
            self.table.setItem(
                row_position,
                TableColumn.FOLDER_ID,
                QTableWidgetItem(rule.folder_id)
            )
            self.table.setItem(
                row_position,
                TableColumn.ACCOUNT_NAME,
                QTableWidgetItem(rule.account)
            )
            self.table.setItem(
                row_position,
                TableColumn.TIME,
                QTableWidgetItem(rule.time)
            )
            self.table.setItem(
                row_position,
                TableColumn.WEEKDAY,
                QTableWidgetItem(rule.weekday or "")
            )
            self.table.setItem(
                row_position,
                TableColumn.DAY_OF_MONTH,
                QTableWidgetItem(
                    str(rule.day_of_month) \
                        if rule.day_of_month is not None else ""
                )
            )

    @staticmethod
    def close_application() -> None:
        """Ends the program."""
        QApplication.quit()

    def closeEvent(self, event: QCloseEvent | None) -> None:
        """Hides (tray) the program when the program is closed."""
        if event is not None:
            event.ignore()
        self.hide()

    def icon_clicked(self, reason) -> None:
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
        selected_rule = self.table.currentRow()
        if selected_rule == -1:
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
                TableColumn.PATH_FROM
            ).text(),
            "folderID": self.table.item(
                selected_row,
                TableColumn.FOLDER_ID
            ).text(),
            "account": self.table.item(
                selected_row,
                TableColumn.ACCOUNT_NAME
            ).text(),
            "time": self.table.item(
                selected_row,
                TableColumn.TIME
            ).text(),
            "weekday": self.table.item(
                selected_row,
                TableColumn.WEEKDAY
            ).text(),
            "dayOfMonth": self.table.item(
                selected_row,
                TableColumn.DAY_OF_MONTH
            ).text()
        }

    def reset_table(self):
        """Resets the table."""
        self.table.clearContents()

    def select_row(self, selected_row: int) -> None:
        """Selects the row in the table."""
        self.table.selectRow(selected_row)

    def __resize_window_in_half_of_screen(self) -> None:
        """Resizes the window to half the screen size."""
        screen = self.screen().geometry()

        half_of_screen_by_width = screen.width() // 2
        half_of_screen_by_height = screen.height() // 2

        self.setGeometry(
            0,
            0,
            half_of_screen_by_width,
            half_of_screen_by_height
        )

    def __center_window(self) -> None:
        """Centers the window in screen."""
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(
            self.screen().availableGeometry().center()
        )
        self.move(frame_geometry.topLeft())
