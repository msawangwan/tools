#JIRA ISSUE CREATOR

###Easily post issues using a prefedined template to a JIRA DB

**Dependencies**

- python 2.7
- JIRA python module

**Installation**

- Install python 2.7 (https://www.python.org/download/releases/2.7/)
	- To confirm python is installed, open a command prompt and type ...

			python -V

	- You should see ...

			Python 2.7.11

	- If not, you may have messed up or need additional configuring. Seek help.

- Use the python package manager to install the JIRA python module
	- To do this, run the command line and type ...

			pip install jira

	- If no errors appear, you're good.

- Unzip the *jira-tasker* directory somewhere, like your desktop or docs or whatever. You're done with the install.

**Setup**

- From the *jira-tasker* directory, open the *jira-tasker-create-issue.bat* file in a text-editor.
	- On the first line, type in the path to the file *JiraTaskerGUI.py*
- Create a shortcut to this *.bat* file on your desktop or taskbar.

**Config**

- Open the *userconfig.ini* file in a text-editor, and read the instructions.
	- For the most part, this file is already set-up, but you need to go through and replace any text enclosed in angled brackets.
- That's it, you're done. Run the *.bat* file to use the app.
