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

"""Module containing the reportException method."""

from infrastructure.logger import logger
from util.display_critical_message import display_critical_message


def report_exception(exception: Exception) -> None:
    """Reports exceptions - logs and displays message"""
    logger.error(exception)
    display_critical_message(str(exception))
