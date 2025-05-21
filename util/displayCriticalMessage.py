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

from PyQt5.QtWidgets import QMessageBox


def displayCriticalMessage(exceptionMessage: str) -> None:
    """
    Displays a critical message box with the exception message.
    Args:
        exceptionMessage (str): is an exception message.
    """
    QMessageBox.critical(
        None,
        "Error",
        exceptionMessage,
        QMessageBox.Ok
    )
