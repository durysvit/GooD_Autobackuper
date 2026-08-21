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

from dependency_injector import containers, providers
from repositories.credentials_repository import CredentialsRepository
from repositories.rule_repository import RuleRepository
from service.google_auth_service import GoogleAuthService
from worker.file_copy_worker import FileCopyWorker
from views.main_window import MainWindow
from controllers.application_controller import ApplicationController


class Container(containers.DeclarativeContainer):
    credentials_repository = providers.Singleton(CredentialsRepository)
    rule_repository = providers.Singleton(RuleRepository)
    
    drive_service = providers.Resource(
        GoogleAuthService.get_authorized_service,
        credentials_repository=credentials_repository,
    )
    
    rules_list = providers.Callable(rule_repository.provided.load_rules())
    
    file_copy_worker = providers.Factory(
        FileCopyWorker,
        drive_service=drive_service,
        rules_list=rules_list,
    )
    
    main_window = providers.Singleton(MainWindow)
    
    application_controller = providers.Singleton(
        ApplicationController,
        view=main_window,
        rule_repository=rule_repository,
        credentials_repository=credentials_repository,
        worker=file_copy_worker,
        drive_service=drive_service,
    )
