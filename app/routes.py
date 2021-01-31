from app import app, db
from flask import abort, make_response, jsonify, request
from app.models import Transaction, Customer


@app.route('/balance/<customer_id>', methods=['GET'])
def balance(customer_id):
    customer = Customer.query.get(customer_id)

    if customer is None:
        abort(make_response(jsonify(message="Invalid customer"), 400))

    return make_response(jsonify(account=customer.account, balance=account_balance(customer_id)), 200)


def account_balance(customer_id):
    balance = 0

    for transaction in Transaction.query.filter_by(from_customer_id=customer_id).all():
        balance -= transaction.amount

    for transaction in Transaction.query.filter_by(to_customer_id=customer_id).all():
        balance += transaction.amount

    return balance


@app.route('/withdraw', methods=['POST'])
def withdraw():
    if not request.json:
        abort(make_response(jsonify(message="Invalid payload"), 400))

    errors = []
    if 'from_customer_id' not in request.json:
        errors.append("Missing from customer")
    if Customer.query.get(request.json['from_customer_id']) is None:
        errors.append("Invalid from customer")
    if 'amount' not in request.json:
        errors.append("Missing to amount")

    if account_balance(request.json['from_customer_id']) - float(request.json['amount']) < 0:
        errors.append("Insufficient funds")

    if errors:
        abort(make_response(jsonify(message="".join(errors)), 400))

    transaction = Transaction(
        type="Withdraw",
        from_customer_id=request.json['from_customer_id'],
        amount=request.json['amount'],
    )

    db.session.add(transaction)
    db.session.commit()

    return make_response(jsonify(transaction_id=transaction.id), 200)


@app.route('/transfer', methods=['POST'])
def transfer():
    if not request.json:
        abort(make_response(jsonify(message="Invalid payload"), 400))

    errors = []
    if 'from_customer_id' not in request.json:
        errors.append("Missing from customer")
    if Customer.query.get(request.json['from_customer_id']) is None:
        errors.append("Invalid from customer")
    if 'to_customer_id' not in request.json:
        errors.append("Missing to customer")
    if Customer.query.get(request.json['to_customer_id']) is None:
        errors.append("Invalid to customer")
    if 'amount' not in request.json:
        errors.append("Missing to amount")

    if account_balance(request.json['from_customer_id']) - float(request.json['amount']) < 0:
        errors.append("Insufficient funds")

    if errors:
        abort(make_response(jsonify(message="".join(errors)), 400))

    transaction = Transaction(
        type="Transfer",
        from_customer_id=request.json['from_customer_id'],
        to_customer_id=request.json['to_customer_id'],
        amount=request.json['amount'],
    )

    db.session.add(transaction)
    db.session.commit()

    return make_response(jsonify(transaction_id=transaction.id), 200)
