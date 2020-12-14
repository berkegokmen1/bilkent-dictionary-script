# Setup

There are several packages that you need to install. 
```bash
pip install beautifulsoup4
pip install requests
pip install termcolor
pip install colorama
```



## Recommended commands (For zsh users)
1. open ~/.zshrc file with a code editor. (nano)
2. type in following command.
```zsh
nano ~/.zshrc

dict() {
	echo running dictionary...
	clear
	cd -PATH TO THE FOLDER CONTAINING PY FILE-
	python3 dictionary.py
}

```
3. save the file and exit.

This command will allow you to run the script directly from terminal by simply typing "dict" anytime you want. This will also ensure that the .csv file will be created inside the same folder with the python file.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.