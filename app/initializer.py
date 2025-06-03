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

"""Module containing the initializer of the environment."""

import os
from const.const import RULE_DIRECTORY, RULES_FILE_PATH


def initializeEnvironment():
    """Creates the RULE_DIRECTORY and RULES_FILE."""
    if not os.path.exists(RULE_DIRECTORY):
        os.makedirs(RULE_DIRECTORY)

    if not os.path.exists(RULES_FILE_PATH):
        open(RULES_FILE_PATH, 'w').close()
