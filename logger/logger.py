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

"""Module containing the logger settings."""

import os
import json
from loguru import logger
from const.const import LOGGER_CONFIG_FILE

with open(LOGGER_CONFIG_FILE, "r") as loggerConfigFile:
    loggerConfig = json.load(loggerConfigFile)

os.makedirs(os.path.dirname(loggerConfig["logPath"]), exist_ok=True)

logger.remove()

logger.add(
    loggerConfig["logPath"],
    rotation=loggerConfig["rotation"],
    mode=loggerConfig["mode"],
    level=loggerConfig["level"],
    format=loggerConfig["format"]
)
