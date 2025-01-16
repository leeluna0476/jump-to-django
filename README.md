# How to run a server
1. Install python and Django.
```zsh
# Mac
$ brew install python3
$ pip install django
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
4. Clone this repository at the root directory of the project.
```zsh
# Mac
$ git clone git@github.com:leeluna0476/jump-to-django.git [project-name]
```
5. Run the server.
```zsh
# Mac
$ cd [project-name]
$ python3 manage.py runserver
```
