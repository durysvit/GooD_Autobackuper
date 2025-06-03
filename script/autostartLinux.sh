#!/bin/bash

PROJECT_DIR=$(dirname "$(realpath "$0")")
EXE_PATH="$PROJECT_DIR/GooD_Autobackuper"
APP_NAME="GooD_Autobackuper"
ICON_PATH="$PROJECT_DIR/GooD_Autobackuper.svg"
AUTOSTART_DIR="$HOME/.config/autostart"
DESKTOP_FILE="$AUTOSTART_DIR/$APP_NAME.desktop"

if [ -f "$DESKTOP_FILE" ]; then
    echo "The program has already been added to startup"
else
    mkdir -p "$AUTOSTART_DIR"
    echo "[Desktop Entry]
Type=Application
Exec=$EXE_PATH
Name=$APP_NAME
Comment=argnullo@gmail.com
Icon=$ICON_PATH
Terminal=false" > "$DESKTOP_FILE"
    echo "The program has been added to startup."
fi
