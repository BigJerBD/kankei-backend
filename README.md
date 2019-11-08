# kankei-backend

Kankei is a project focus on creating a tool to help people learn about kanji. 
It currently contains about 200 000 japanese words and about 10 000 kanji

Kankei-Backend is only a single part of the whole project. It contains the async backend
created with Sanic

> A python backend for kankei made with Sanic
## Requirements

Only python 3.7.x is required to the the server
  
## Project setup
on a linux terminal execute : 
```
$ ./setup.sh
$ source venv/bin/activate #or venv/scripts/activate on windows
```
this will make a virtual environment to start the python server

then install the python requirements.txt:
```
$ source venv/bin/activate #or venv/scripts/activate on windows
pip install -r requirements.txt
```

### Start the server 

```
$ source venv/bin/activate #or venv/scripts/activate on windows
$ export KANKEI_WEB_SETTINGS=`pwd`/src/settings/dev.py  #or use a custom setting
$ python `pwd`/src/server.py
```

### Other Components

- to run the backend with the frontend, please go the `Kankei-Frontend` repository
  for more information about the setup

- to run also the database, please contact me directly. The data are not openly shared to everyone
  since they come from personal data wrangling processes


## Authors

- Jérémie Bigras-Dunberry - Initial work
