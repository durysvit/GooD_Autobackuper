# Automated Backup System for Google Drive - GooD Autobackuper.
#
# Copyright (C) 2025 durysvit
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# Email argnullo@gmail.com.
#
# Version 1.5.0.

"""Module containing the entry point."""

import sys
from PyQt5.QtWidgets import QApplication
from window.MainWindow import MainWindow
from logger.logger import logger

if __name__ == "__main__":
    logger.info("Start an application.")

    application = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    logger.info("End the application.")

    sys.exit(application.exec_())
