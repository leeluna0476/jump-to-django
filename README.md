# How to make a django project in a python virtual environment
1. Install python.
```zsh
# Mac
$ brew install python3
```
2. Make a new python virtual environment.
```zsh
# Mac
$ python3 -m venv [venv-name]
```
3. Activate python virtual environment.
```zsh
# Mac
$ source [venv-name]/bin/activate
# Deactivate
$ deactivate
```
4. Install django in python virtual environment.
```zsh
# Mac
$ pip install django
```
5. Make a new django project.
```zsh
# Mac
$ mkdir [project-dir]
$ django-admin startproject config [project-dir]
```
6. Run the server.
```zsh
# Mac
$ cd [project-dir]
$ python3 ./manage.py runserver
```
