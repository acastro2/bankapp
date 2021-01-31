import os
import pytest
import tempfile

from config import basedir
from app import app, db
from app.models import Customer, Transaction

@pytest.fixture(scope="session")
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            setup_db()
        yield client

    db.session.remove()
    db.drop_all()
    os.remove(os.path.join(basedir, 'test.db'))

def setup_db():
    c1 = Customer(name="Alexandre", account="12345", cpf="12345678900")
    db.session.add(c1)
    db.session.commit()

    transaction = Transaction(
        type="Deposit",
        to_customer_id=c1.id,
        amount=100000,
    )

    db.session.add(transaction)
    db.session.commit()

    c2 = Customer(name="Tester", account="12344", cpf="12345678901")
    db.session.add(c2)
    db.session.commit()

def test_balance(client):
    rv = client.get('/balance/1')
    json_data = rv.get_json()

    assert json_data['account'] == '12345'
    assert json_data['balance'] == 100000.0

def test_withdraw(client):
    rv = client.post('/withdraw', json={
        'from_customer_id': '1',
        'amount': 10.0
    })

    json_data = rv.get_json()

    print(json_data)
    assert json_data['transaction_id'] == 2

def test_transfer(client):
    rv = client.post('/withdraw', json={
        'from_customer_id': '1',
        'to_customer_id': '2',
        'amount': 10.0
    })

    json_data = rv.get_json()

    print(json_data)
    assert json_data['transaction_id'] == 3