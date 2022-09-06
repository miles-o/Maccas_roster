# Read me
This takes your roster from myjob, converts it to a csv, then takes you to google calender to import with only a few clicks 

If there are any problems add an issue to the issue section or if you know me just tell me and I'll sort it out :)

## Setup
1. Install python at [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Install Visual studio code at [https://code.visualstudio.com/download](https://code.visualstudio.com/download)
3. In vs code go to extensions and install the python extension by microsoft
4. Open the command prompt/terminal and check the python installation with: python3 --version, it should say something like "Python 3.10.5"
5. Make sure pip is up to date in the terminal using: python3 -m pip install pip --upgrade pip
6. Install selenium in the terminal using: pip install selenium
7. Add your google login details to the login_details.txt file
8. Download all files and put them in a folder
10. Delete the placeholder.txt file in the data folder
11. You should be good to go!

## How to use
1. Open vscode and clock on open folder, navigate to folder containing all files for this program
2. Click run in the top right corner
3. Let the code run until in the google calendar setting page
4. Click upload files on google calendar and select the roster.csv located in the code folder
5. Select calendar to import into and import the shifts
6. To access estimated pay and weekly hours open data folder and select file for that week
