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

"""Module containing the GoogleDriveFolderPicker class."""

from service.google_drive_service import GoogleDriveService
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem
)


class GoogleDriveFolderPicker(QDialog):
    """
    The class of GoogleDriveFolderPicker - manager for selecting from the
    directory hierarchy in Google Drive.
    """
    folder_selected = Signal(str)

    def __init__(self, drive_service):
        """
        Initializes the folder picker window.
        Args:
            drive_service (Service): is the auth drive service.
        """
        super().__init__()
        self.drive_service = drive_service
        self.setWindowTitle("Select Google Drive Folder")
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint
        )
        self.selected_folder_id = None

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemExpanded.connect(self.load_subfolders_lazy)

        self.confirm_button = QPushButton("Select")
        self.confirm_button.clicked.connect(self.confirm)

        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        layout.addWidget(self.confirm_button)
        self.setLayout(layout)

        self.populate_root()

    def on_item_clicked(self, item) -> None:
        """Saves the selected item."""
        self.selected_folder_id = item.data(0, Qt.ItemDataRole.UserRole)

    def populate_root(self) -> None:
        root_item = QTreeWidgetItem(["Root"])
        root_item.setData(0, Qt.ItemDataRole.UserRole, "root")
        root_item.setChildIndicatorPolicy(
            QTreeWidgetItem.ChildIndicatorPolicy.ShowIndicator
        )
        root_item.setData(0, Qt.ItemDataRole.UserRole + 1, False)
        self.tree.addTopLevelItem(root_item)
        self.tree.expandItem(root_item)
        self.tree.setCurrentItem(root_item)

    def load_subfolders_lazy(self, item):
        """Loads subfolders lazy."""
        is_loaded = item.data(0, Qt.ItemDataRole.UserRole + 1)
        if is_loaded:
            return

        parent_id = item.data(0, Qt.ItemDataRole.UserRole)
        subfolders = GoogleDriveService.list_folders(
            self.drive_service,
            parent_id
        )
        for folder in subfolders:
            child = QTreeWidgetItem([folder["name"]])
            child.setData(0, Qt.ItemDataRole.UserRole, folder["id"])
            child.setChildIndicatorPolicy(
                QTreeWidgetItem.ChildIndicatorPolicy.ShowIndicator
            )
            child.setData(0, Qt.ItemDataRole.UserRole + 1, False)
            item.addChild(child)
        item.setData(0, Qt.ItemDataRole.UserRole + 1, True)

    def confirm(self) -> None:
        """Accepts the selected folder."""
        selected_folder = self.tree.currentItem()
        if selected_folder:
            folder_id = selected_folder.data(0, Qt.ItemDataRole.UserRole)
            self.folder_selected.emit(folder_id)
            self.accept()
