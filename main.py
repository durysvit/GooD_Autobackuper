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
# Version 2.0.0.

"""Module containing the entry point."""

import sys
from PyQt5.QtWidgets import QApplication
from app.initializer import initializeEnvironment
from view.MainWindow import MainWindow
from model.RuleRepository import RuleRepository
from model.CredentialsRepository import CredentialsRepository
from controller.ApplicationController import ApplicationController
from worker.FileCopyWorker import FileCopyWorker
from service.GoogleAuthService import GoogleAuthService
from logger.logger import logger

if __name__ == "__main__":
    logger.info("Start an application.")

    initializeEnvironment()

    application = QApplication(sys.argv)

    credentialsRepository = CredentialsRepository()

    driveService = GoogleAuthService.getAuthorizedService(
        credentialsRepository
    )

    ruleRepository = RuleRepository()

    listOfRules = ruleRepository.loadRules()

    mainWindow = MainWindow()
    worker = FileCopyWorker(driveService, listOfRules)
    applicationController = ApplicationController(
        mainWindow,
        ruleRepository,
        credentialsRepository,
        worker,
        driveService
    )

    mainWindow.show()

    exitCode = application.exec_()

    logger.info("End the application.")

    sys.exit(exitCode)
