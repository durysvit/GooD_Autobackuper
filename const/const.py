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

import os

ICON_FILE = "GooD_Autobackuper.svg"

SOURCE_DIRECTORY = "./source"
PATH_TO_RULES_CSV = os.path.join(SOURCE_DIRECTORY, "rules.csv")

ONE_MINUT_IN_SECONDS = 60

SCOPES = ["https://www.googleapis.com/auth/drive"]

TOKEN_FILE = "token.pickle"
CREDENTIALS_FILE = "credentials.json"
