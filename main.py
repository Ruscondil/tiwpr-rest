from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
purchases = []

# GET endpoint to retrieve all purchases


@app.route('/purchases', methods=['GET'])
def get_purchases():
    return jsonify(purchases)

# POST endpoint to create a new purchase


@app.route('/purchases', methods=['POST'])
def create_purchase():
    new_purchase = {
        'item': request.args.get('item'),
        'quantity': int(request.args.get('quantity')),
        'price': float(request.args.get('price'))
    }
    purchases.append(new_purchase)
    return jsonify(new_purchase), 201


if __name__ == '__main__':
    app.run()
