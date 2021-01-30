# Bank Application

API de saque e transferência

## Install Dependencies

```bash
pip install -r requirements.txt
```

For more information on pip requirements files check the [documentation](https://pip.pypa.io/en/stable/reference/pip_install/#requirements-file-format)

## Setup DB

```bash
flask db init
flask db migrate
flask db upgrade
```

## Run app

```bash
# Create virtual environment
python3 -m venv venv

# Install Dependencies
pip install -r requirements.txt

# Run Flask
flask run
```

## Documentation

* [Flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
* [SQLAlchemy Migrate](https://opendev.org/x/sqlalchemy-migrate)
