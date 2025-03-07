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

# Thrown if in the file has not been uploaded to Google Drive.
class FileNotUploadedException(Exception):
    def __init__(self):
        super().__init__(
            "FileNotUploadedException: the file has not been uploaded to "
                "Google Drive."
            )