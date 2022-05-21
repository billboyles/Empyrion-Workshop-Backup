# Empyrion Workshop Backup
Empyrion Workshop Backup (EWB) backs up all public blueprints from a given Steam ID's online library.

## Prerequisites

### Windows
EWB currently only runs on Windows and has only been tested on Windows 10 but should work on any version fulfilling the Python requirements below. EWB versions working on Mac and Linux are planned.  

### Python
EWB currently requires the following to be installed on the system: Python 3.6 or higher, the Python Requests module, the Beautiful Soup 4 module. 

### Steam ID
You need to get have the numeric Steam ID of the account you want to backup. There are two ways to obtain this.

1. Look in the URL of the workshop: \https://steamcommunity.com/profiles/<Numeric Steam ID>/myworkshopfiles\.

2. To obtain your own Steam ID, it is listed in the Account Details section of your account. Online, the link for Account Details is: (https://store.steampowered.com/account/). In the App, click the dropdown with your account name at the top right and select "Account Details".

### Workshop
Currently, you must be subscribed to every build on the target workshop. This will be changed in a future version.  


## Running EWB from the command line

1. Open a command line terminal (cmd or Powershell) and navigate to the EWB folder. 
2. Run EWB with the command `python ewb.py`
3. EWB will prompt you to select the folder to which you want the backup to be made. It is strongly advised you create a new empty folder, as the tool will create a new folder inside the backup folder for each build it backs up. 
4. EWB will prompt you to enter your numeric Steam ID.

That's it! EWB will download the title, description, and screenshots from the Steam website and unify them with the .epb file and main screenshot from your Steam workshop folder.

### Troubleshooting

Ensure you have Python 3.6 or higher installed and have installed the required Pytyhon modules. Verify you are selecting a folder to which you have write permissions in which to backup the files. Check that your Steam ID is correct.

Please feel free to create an Issue or make a Pull Request. I'll respond as soon as possible.