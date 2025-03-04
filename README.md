<picture>
    <source media="(prefers-color-scheme: dark)" srcset="./GooD_Autobackuper.svg">
    <source media="(prefers-color-scheme: light)" srcset="./GooD_Autobackuper.svg">
    <img alt="GooD_Autobackuper" src="./GooD_Autobackuper.svg">
</picture>

# GooD Autobackuper

## About program

Automatic backup information system for Google Drive — GooD Autobackuper.

Version 1.1.0.

## Author 

Github [durysvit](https://github.com/durysvit).

Email argnullo@gmail.com.

## Requirements

Functional requirements include the following capabilities:
* the program has a graphical interface;
* the program starts automatically — works in the background;
* the ability to log in to Google;
* possibility to specify the directory from which files are copied;
* the ability to specify the Google Drive directory to which files are copied;
* the ability to set the exact time of copying files.

Non-functional requirements include:
* possibility to save authorization data;
* the ability to authorize one Google account.

## User manual

### Before starting the program

Create Google Cloud project:
1. Create a project on [Google Cloud](https://console.cloud.google.com/projectcreate) — enter project name and ID.
1. Google Cloud enable API Google­— see [Drive Python API](https://developers.google.com/drive/api/quickstart/python).
1. Configure the OAuth consent screen and add yourself as a test user: in [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent?) enable User Type — External; press "Create".
1. Add scopes: ".../auth/drive" and ".../auth/docs".
1. You also need to authorize credentials for the desktop application using an OAuth 2.0 client ID. The client ID is used to identify a single application to Google OAuth servers. Press "API and servises" — "Credentials" — "Create credentials" — "OAuth client ID" — "Application app" — "Desktop app" and enter the name of your OAuth 2.0 client.
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
* and the time when you need to make a copy.

In the main window, click the "Add" button. You will see a window to add a rule. 

Add data to the appropriate fields: 
* copy the full path to the folder and paste; 
* copy the ID of your folder in Google Drive and paste; 
* enter your account name;
* add time to the list; if the time is entered incorrectly, select it and click "Delete".

If you need to delete this rule from the table, then select it in the table and click the "Delete" button.

When closing the program, it will be minimized to the tray. If you need to end the program, you need to right-click on the program icon in the tray and click "Exit".

### Problem solving

EmptyLineEditException is thrown if one of the fields in the rule creation window is empty — fill in all fields.  

FileExistsError thrown if:
* token file doesn't exsist — log in to Google;
* credentials file doesn't exsist — register as a developer in Google Console — see subsection "Before starting the program";
* rules.csv file doesn't exsist — the file will be created automatically after;
* the path to the folder you want to copy does not exist — select an existing folder.

FileNotUploadedException thrown if in the file has not been uploaded to Google Drive — check if the Google Drive folder ID is entered correctly; try again later; check your internet connection; re-authorize by deleting the "token.pickle" file.

EmptyTimeListException thrown if in the Creation rule window, the time list is empty — complete the list with time.

NoRowSelectedInTable thrown if no row was selected to delete from table — select the row.

NotExistFolderIDException thrown if Google Drive folder ID does not exsist — check the ID of folder.

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

Install pyinstaller:

```
pip install pyinstaller
```

Assemble the project:

```
pyinstaller --onefile --windowed --icon=GooD_Autobackuper.svg --name GooD_Autobackuper main.py
```

## License

The code is distributed under the GNU GPLv3. See [LICENSE](./LICENSE).