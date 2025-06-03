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

# Folders
RULE_DIRECTORY = "rule"
CONFIG_DIRECTORY = "config"

# Files
ICON_FILE = "GooD_Autobackuper.svg"
RULES_FILE = "rules.csv"
LOGGER_CONFIG_FILE = "configLogger.json"

# Confidential files
TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"

# Scopes
SCOPES = ["https://www.googleapis.com/auth/drive"]

# Paths
RULES_FILE_PATH = os.path.join(RULE_DIRECTORY, RULES_FILE)
LOGGER_CONFIG_FILE_PATH = os.path.join(CONFIG_DIRECTORY, LOGGER_CONFIG_FILE)

# Numbers
NUMBER_OF_RULE_ATTRIBUTES = 6
