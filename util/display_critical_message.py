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

"""Module containing the displayCriticalMessage method."""

from PySide6.QtWidgets import QMessageBox


def display_critical_message(exception_message: str) -> None:
    """
    Displays a critical message box with the exceptions message.
    Args:
        exception_message (str): is the exceptions message.
    """
    QMessageBox.critical(
        None,
        "Error",
        str(exception_message),
        QMessageBox.Ok
    )
