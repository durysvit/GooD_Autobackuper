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
from PyQt5.QtWidgets import QApplication
from infrastructure.initializer import initialize_environment
from view.main_window import MainWindow
from model.repositories.RuleRepository import RuleRepository
from model.repositories.CredentialsRepository import CredentialsRepository
from controllers.application_controller import ApplicationController
from worker.file_copy_worker import FileCopyWorker
from service.google_auth_service import GoogleAuthService
from infrastructure.logger import logger


def main():
    """Application entry point."""
    logger.info("Start an application.")
    
    initialize_environment()
    
    application = QApplication(sys.argv)
    
    credentials_repository = CredentialsRepository()
    
    drive_service = GoogleAuthService.get_authorized_service(
        credentials_repository
        )
    
    rule_repository = RuleRepository()
    
    list_of_rules = rule_repository.load_rules()
    
    main_window = MainWindow()
    worker = FileCopyWorker(drive_service, list_of_rules)
    application_controller = ApplicationController(
        main_window,
        rule_repository,
        credentials_repository,
        worker,
        drive_service
    )
    
    main_window.show()
    exit_code = application.exec_()
    
    logger.info("End the application.")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
