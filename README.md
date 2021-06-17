# Run django app

1. Install Python 3.8+
2. Install virtualenv package.
```
$ python3 -m pip install virtualenv
```
3. Create virtual environment.
```
$ python3 -m virtualenv my_env
```
4. Activate environment
```
$ source ../my_env/bin/activate
```
5. Clone/Download the repository

6. Install requirements
```
(my_env) $ pip install -r ../requirements.txt
```
7. Create super user
```
(my_env) $ python3 manage.py createsuperuser
```
8. Make migrations
```
(my_env) $ python3 manage.py makemigrations
```
9. Migrate
```
(my_env) $ python3 manage.py migrate
```
10. Run server
```
(my_env) $ python3 manage.py runserver
```