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

from service.GoogleDriveService import GoogleDriveService
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
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
    folderSelected = pyqtSignal(str)

    def __init__(self, driveService):
        """
        Initializes the folder picker window.
        Args:
            driveService (Service): is the auth drive service.
        """
        super().__init__()
        self.driveService = driveService
        self.setWindowTitle("Select Google Drive Folder")
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint
        )
        self.selectedFolderID = None

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemExpanded.connect(self.loadSubfoldersLazy)

        self.confirmButton = QPushButton("Select")
        self.confirmButton.clicked.connect(self.confirm)

        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        layout.addWidget(self.confirmButton)
        self.setLayout(layout)

        self.populateRoot()

    def onItemClicked(self, item) -> None:
        """Saves the selected item."""
        self.selectedFolderID = item.data(0, Qt.UserRole)

    def populateRoot(self) -> None:
        rootItem = QTreeWidgetItem(["Root"])
        rootItem.setData(0, Qt.UserRole, "root")
        rootItem.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
        rootItem.setData(0, Qt.UserRole + 1, False)
        self.tree.addTopLevelItem(rootItem)
        self.tree.expandItem(rootItem)
        self.tree.setCurrentItem(rootItem)

    def loadSubfoldersLazy(self, item):
        """Loads subfolders lazy."""
        isLoaded = item.data(0, Qt.UserRole + 1)
        if isLoaded:
            return

        parentID = item.data(0, Qt.UserRole)
        subfolders = GoogleDriveService.listFolders(
            self.driveService,
            parentID
        )
        for folder in subfolders:
            child = QTreeWidgetItem([folder["name"]])
            child.setData(0, Qt.UserRole, folder["id"])
            child.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            child.setData(0, Qt.UserRole + 1, False)
            item.addChild(child)
        item.setData(0, Qt.UserRole + 1, True)

    def confirm(self) -> None:
        """Accepts the selected folder."""
        selected = self.tree.currentItem()
        if selected:
            folderID = selected.data(0, Qt.UserRole)
            self.folderSelected.emit(folderID)
            self.accept()
