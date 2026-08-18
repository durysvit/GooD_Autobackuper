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
# Version 2.1.0.

"""Application entry point."""

import sys
from PySide6.QtWidgets import QApplication
from infrastructure.initializer.initializer import initialize_environment
from infrastructure.logger.logger import logger
from application.containers.Container import Container


def main():
    """Application entry point."""
    logger.info("Start an application.")

    initialize_environment()
    
    application = QApplication(sys.argv)

    container = Container()
    container.init_resources()

    main_window = container.main_window()
    controller = container.application_controller()

    main_window.show()
    exit_code = application.exec()

    logger.info("End the application.")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
