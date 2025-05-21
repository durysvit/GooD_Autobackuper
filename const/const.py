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

"""Module containing the constants."""

import os

ICON_FILE = "GooD_Autobackuper.svg"
DATA_DIRECTORY = "./data"
RULES_FILE = os.path.join(DATA_DIRECTORY, "rules.csv")
SCOPES = ["https://www.googleapis.com/auth/drive"]
TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"
LOGGER_CONFIG_FILE = "./config/configLogger.json"
