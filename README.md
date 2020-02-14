# viral-growth

## starting server
```
install python3.6 and pipenv (pip install pipenv)
git clone https://github.com/valeriykundas/viral-growth
cd viral-growth
pipenv install
pipenv shell
python manage.py migrate
python manage.py runscript initdb
python manage.py runserver
go to localhost:8000
```

## running tests
```
pipenv install --dev
pipenv run pytest
```
