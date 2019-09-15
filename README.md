# kankei-backend

> A python backend for kankei made with Sanic

## Project setup
on a linux terminal execute : 
```
$ ./setup.sh
$ source venv/bin/activate #or venv/scripts/activate on windows
```
this will make a virtual environment to start the python server

then install the python requirements.txt:

```
pip install -r requirements.txt
```

### Start the server 

```
export KANKEI_WEB_SETTINGS=`pwd`/src/settings/dev.py  #or use a custom setting
python `pwd`/src/server.py
```

