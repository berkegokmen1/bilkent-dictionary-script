# Setup

There are several packages that you need to install. 
```bash
pip install beautifulsoup4
pip install requests
pip install termcolor
pip install colorama
pip install lxml
```



## Desktop shortcut for Mac users

0. (Shortcut for windows are on the way)
1. open dict.command using a text editor.
2. type in the folder path to the specified area.
```zsh
echo running dictionary...
clear
cd -PATH TO THE FOLDER CONTAINING PY FILES-
python3 dictionary.py
cd /Applications
```
3. save the files and exit.

#### If you see an error saying “File could not be executed because you do not have appropriate access privileges” then try running the command below

```zsh
chmod u+x /Users/-YOUR USERNAME-/Desktop/stars.command
chmod u+x /Users/-YOUR USERNAME-/Desktop/zoom.command
```
You can then use the .command files to run the script


This command will allow you to run the script directly from terminal by simply typing "dict" anytime you want. This will also ensure that the .csv file will be created inside the same folder with the python file.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
