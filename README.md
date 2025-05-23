<picture>
    <source media="(prefers-color-scheme: dark)" srcset="./GooD_Autobackuper.svg">
    <source media="(prefers-color-scheme: light)" srcset="./GooD_Autobackuper.svg">
    <img alt="GooD_Autobackuper" src="./GooD_Autobackuper.svg">
</picture>

# GooD Autobackuper

## About program

An Automated Backup System for Google Drive — GooD Autobackuper.

Version 1.5.0.

## Author 

Github: [durysvit](https://github.com/durysvit).

Email: argnullo@gmail.com.

## Program requirements

Functional requirements include the following capabilities:
* The user can launch the application with a graphical user interface;
* The user must authorize with Google to use the application;
* The application should support automatic reauthorization with Google;
* The user must register a project in the Google Cloud Console;
* The application requires two files to operate: token.json for user authorization and credentials.json for developer access;
* The main window of the application "GooD Autobackuper" must include:
    - A table displaying user-defined rules from the modal form window.
    - An Add button to add a new rule.
    - A Delete button to remove a selected rule.
    - A File menu with an option to delete the token file (Delete token file).
* The user can create backup rules through a dedicated modal window called Creation Rule, which includes:
    - A read-only field displaying the full path to the source directory to be backed up;
    - A button (with a folder icon) to open the directory chooser;
    - A field to enter the Google Drive folder ID where files will be copied;
    - A field to enter the Google account name (label);
    - A time picker widget;
    - A list of unique time entries when the backup should occur;
    - A button to add a time to the list;
    - A dropdown list with days of the week;
    - A dropdown list with days of the month;
    - A Confirm button to create the rule;
* Rule creation requires specifying:
    - A source directory to copy files from;
    - A destination Google Drive folder ID;
    - An exact time for the backup;
    - Optionally, a specific day of the week or day of the month.
* The application must display appropriate error messages in the following cases:
    - Empty source directory path;
    - Empty Google Drive folder ID;
    - Empty account label field;
    - Empty list of scheduled times;
    - Files failed to copy to the cloud storage;
    - credentials.json file is missing;
    - token.json file is missing, expired, or revoked;
    - No rule selected in the table when trying to delete;
    - Application is unable to upload files to Google Drive;
    - The specified Google Drive folder ID does not exist;
    - And other similar critical failures.
* The user can delete an existing rule;
* When the main window is closed, the application should minimize to the system tray and continue running in the background;
* The application must terminate when the Exit button in the tray menu is clicked (via right-click on the tray icon);
* The application must have an icon/emblem.

Non-functional requirements include:
* The application stores authorization data and developer credentials in token.json and credentials.json, respectively;
* The application starts automatically and runs in the background;
* Authorization data is stored in a file to support automatic login;
* The user can authorize only one Google account;
* Backup times must be specified in the "HH:MM" format;
* The application saves the following data in a CSV file:
    - Source directory path;
    - Destination Google Drive folder ID;
    - Exact backup time;
    - Optionally, day of the week or day of the month;
* The Google Drive folder is identified by an ID — a hash value at the end of the URL after https://drive.google.com/drive/folders/;
* The source directory must be provided as an absolute path in the file system;
* The application is guaranteed to work on Windows 11 and Manjaro Linux 6.11;
* The application icon must be in SVG vector format.

### Out of scopes

The program does not take into account that your Google Drive has little or no memory; it also does not take into account an unstable or poor connection.

## User manual

### Before starting the program

Create Google Cloud project:
1. Create a project on [Google Cloud](https://console.cloud.google.com/projectcreate) — enter project name and ID.
1. Enable the Google Cloud API­— see [Drive Python API](https://developers.google.com/drive/api/quickstart/python).
1. Configure the OAuth consent screen and add yourself as a test user: in [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent?) enable User Type — External; press "Create".
1. Add scopes: "auth/drive" and "auth/docs".
1. You also need to authorize credentials for the desktop application using an OAuth 2.0 client ID. The client ID is used to identify a single application to Google OAuth servers. Press:
    1. "API and servises";
    1. "Credentials";
    1. "Create credentials";
    1. "OAuth client ID";
    1. "Application app";
    1. "Desktop app" and enter the name of your OAuth 2.0 client.
1. Create "credentials.json" — copy the file to the root of the program project.

### After starting the program

After starting the program, you must log in to Google. 

After authorization, give access rights to your account to the GooD Autobackuper program.

### Add the program to autoload

To add a program to startup:
* for Windows users:
    - create a shortcut to the file GooD_Autobackuper.exe;
    - press the key combination "Win + R" and enter `shell:startup`;
    - move the shortcut to this folder. 
* for Linux users — run the autostartLinux.sh script.

### Remove from startup

* for Windows users:
    - press the key combination "Win + R" and enter "shell:startup";
    - remove the shortcut from this folder. 
* for Linux users — remove GooD_Autobackuper.desktop file from `~/.config/autostart`.

### Usage  

For the program to work, you need to create a rule. 

The rule consists of:
* the full path to your directory on your computer that needs to be copied;
* the Google Drive folder ID, which is located at the end of the folder link after https://drive.google.com/drive/folders/;
* the account name; 
* the time when you need to make a copy;
* and optional: the weekday or the number of the month.

In the main window, click the "Add" button. You will see a window to add a rule. 

Add data to the appropriate fields: 
* select folder; 
* copy the ID of your folder in Google Drive and paste; 
* enter your account name;
* add time to the list; if the time is entered incorrectly, select it and click "Delete";
* and optional: select the weekday or the day of the month.

If you need to delete this rule from the table, then select it in the table and click the "Delete" button.

When closing the program, it will be minimized to the tray. If you need to end the program, you need to right-click on the program icon in the tray and click "Exit".

### Problem solving

Exceptions:
* ...LineEditIsEmptyException — Path from, Folder ID, Account — raises if one of the fields in the rule creation window is empty — fill in all fields;
* TokenFileDoesNotExistException — raises if the token file does not exist — log in to Google;
* CredentialsFileDoesNotExistException — raises if credentials file doesn't exist  — register as a developer in Google Console — see subsection "Before starting the program";
* FileNotUploadedException — raises if in the file has not been uploaded to Google Drive — check if the Google Drive folder ID is entered correctly; try again later; check your internet connection; re-authorize by deleting the "token.json" file;
* EmptyTimeListException — raises if in the Creation rule window, the time list is empty — complete the list with time;
* NoRowSelectedInTable — raises if no row was selected to delete from table — select the row;
* NotExistFolderIDException — raises if the Google Drive folder ID does not exist — check the ID of folder.
* TokenFileIsExpiredOrRevokedException — raises if token file is expired or revoked — try delete token file and authorise again;
* etc.

**If the app does not start, try deleting the token.json file from the program directory and restart the app (from tray).**

### Recommendations

Do not abuse the number of rules, do not abuse the size of the copied files — **your account may be blocked** for suspicious actions, for automation, for spam.

It is better to set the time in the rules with a difference of at least 2 minutes.

## System requirements

System Requirements:
* OS:
    - Manjaro Linux 6.11;
    - Windows 11.

## Build the project

Install the latest version of [Python and Pip](https://www.python.org/).

Create a [virtual environment](https://docs.python.org/uk/3.10/library/venv.html):

```
python -m venv venv
```

Activate the virtual env. for Linux (Manjaro) run:

```
. ./venv/bin/activate
```

and for Windows run:

```
.\venv\Scripts\activate.bat
```

Run:

```
pip install -r requirements.txt
```

Assemble the project:

```
pyinstaller --onefile --windowed --icon=GooD_Autobackuper.svg --name GooD_Autobackuper main.py
```

## License

The code is distributed under the GNU GPLv3. See [LICENSE](./LICENSE).
