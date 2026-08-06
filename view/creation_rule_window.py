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

from view.google_drive_folder_picker import GoogleDriveFolderPicker
from PyQt5.QtCore import Qt
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
    QStyle,
    QComboBox,
    QSpinBox
)


class CreationRuleWindow(QDialog):
    """The class of creation rules of autobackup."""
    def __init__(self, drive_service):
        super().__init__()
        self.setWindowTitle("Create rules")
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint
        )

        self.path_from_input = QLineEdit()
        self.path_from_input.setPlaceholderText("Path from")
        self.path_from_input.setReadOnly(True)

        self.folder_id_input = QLineEdit()
        self.folder_id_input.setPlaceholderText("Folder ID")
        self.folder_id_input.setReadOnly(True)

        icon = self.style().standardIcon(QStyle.SP_DirOpenIcon)

        self.browser_path_from_button = QPushButton()
        self.browser_path_from_button.setIcon(icon)
        self.browser_path_from_button.clicked.connect(self.select_folder)

        self.browser_folder_id_button = QPushButton()
        self.browser_folder_id_button.setIcon(icon)
        self.browser_folder_id_button.clicked.connect(
            self.select_google_folder
        )

        self.account_input = QLineEdit()
        self.account_input.setPlaceholderText("Account")

        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")

        self.weekday_combobox = QComboBox()
        self.weekday_combobox.setPlaceholderText("Weekday")
        self.weekday_combobox.addItems(
            ['', "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                "Saturday", "Sunday"]
        )

        MIN_DAY_OF_MONTH = 0
        MAX_DAY_OF_MONTH = 31
        self.month_day_spinbox = QSpinBox()
        self.month_day_spinbox.setMinimum(MIN_DAY_OF_MONTH)
        self.month_day_spinbox.setMaximum(MAX_DAY_OF_MONTH)

        self.add_button = QPushButton("&Add", self)
        self.add_button.clicked.connect(self.add_time)

        self.confirm_button = QPushButton("&Confirm", self)

        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_from_input)
        path_layout.addWidget(self.browser_path_from_button)

        folder_id_layout = QHBoxLayout()
        folder_id_layout.addWidget(self.folder_id_input)
        folder_id_layout.addWidget(self.browser_folder_id_button)

        layout = QVBoxLayout()
        layout.addLayout(path_layout)
        layout.addLayout(folder_id_layout)
        layout.addWidget(self.account_input)
        layout.addWidget(self.time_edit)
        layout.addWidget(self.add_button)

        self.time_list = QListWidget()
        layout.addWidget(self.time_list)

        layout.addWidget(QLabel("Weekday:"))
        layout.addWidget(self.weekday_combobox)
        layout.addWidget(QLabel("Day of month:"))
        layout.addWidget(self.month_day_spinbox)
        layout.addWidget(self.confirm_button)

        self.weekday_combobox.currentTextChanged.connect(
            self.toggle_day_of_month
        )
        self.month_day_spinbox.valueChanged.connect(self.toggle_weekday)
        self.setLayout(layout)
        self.time_list.installEventFilter(self)

        self.driveService = drive_service

    def add_time(self) -> None:
        """Adds unique value of the time to list."""
        time_value = self.time_edit.time().toString("HH:mm")
        time_list = [
            self.time_list.item(i).text() for i in range(
                self.time_list.count()
            )
        ]
        if time_value not in time_list:
            self.time_list.addItem(time_value)

    def remove_selected_time(self) -> None:
        """Removes selected time from the list of the time."""
        selected_items = self.time_list.selectedItems()
        for item in selected_items:
            self.time_list.takeItem(self.time_list.row(item))

    def select_folder(self) -> None:
        """Selects folder."""
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.path_from_input.setText(folder_path)

    def select_google_folder(self):
        """Selects Google Drive folder."""
        dialog = GoogleDriveFolderPicker(self.driveService)
        dialog.folder_selected.connect(
            lambda folderID: self.folder_id_input.setText(folderID)
        )
        dialog.exec_()

    def toggle_weekday(self, value: int) -> None:
        """
        Disables weekdayComboBox if dayOfMonth is selected, else enables it.
        Args:
            value (int): is the number of month or 0.
        """
        if value != 0:
            self.weekday_combobox.setDisabled(True)
        else:
            self.weekday_combobox.setDisabled(False)

    def toggle_month_day(self, text: str) -> None:
        """
        Disables dayOfMonthSpinBox if weekday is selected, else enables it.
        Args:
            text (str): is the name of weekday or empty string.
        """
        if text.strip():
            self.month_day_spinbox.setDisabled(True)
        else:
            self.month_day_spinbox.setDisabled(False)

    def get_inputs(self) -> dict:
        """
        Returns the rules data.
        Returns:
            dict: the dict of the rules' data.
        """
        return {
            "path_from": self.path_from_input.text().strip(),
            "folder_id": self.folder_id_input.text().strip(),
            "account": self.account_input.text().strip(),
            "time_list": [
                self.time_list.item(i).text() for i in range(
                    self.time_list.count()
                )
            ],
            "weekday": self.weekday_combobox.currentText(),
            "day_of_month": int(self.month_day_spinbox.text())
        }

    def eventFilter(self, source, event):
        """
        Adds response to Delete key press and time selection in the table.
        """
        if source == self.time_list and event.type() == event.KeyPress:
            if event.key() == Qt.Key_Delete:
                self.remove_selected_time()
        return super().eventFilter(source, event)
