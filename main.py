from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
purchases = []
products = []
# GET endpoint to retrieve all purchases


@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

# POST endpoint to create a new purchase


@app.route('/products', methods=['POST'])
def create_product():

    new_product = {
        'id': len(products) + 1,
        'item': request.args.get('item'),
        'quantity': int(request.args.get('quantity')),
        'price': float(request.args.get('price'))
    }
    products.append(new_product)
    return jsonify(new_product), 201


@app.route('/purchases', methods=['GET'])
def get_purchases():
    return jsonify(products)

# POST endpoint to create a new purchase


@app.route('/purchases', methods=['POST'])
def create_purchase():
    new_purchase = {
        'id': len(purchases) + 1,
        'item': request.args.get('item'),
        'quantity': int(request.args.get('quantity')),
        'price': float(request.args.get('price'))
    }
    purchases.append(new_purchase)
    return jsonify(new_purchase), 201


if __name__ == '__main__':
    app.run()
