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


# GET endpoint to retrieve a specific product by ID


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    for product in products:
        if product['id'] == product_id:
            return jsonify(product)
    return jsonify({'message': 'Product not found'}), 404

# PUT endpoint to update a specific product by ID


@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    for product in products:
        if product['id'] == product_id:
            product['item'] = request.args.get('item')
            product['quantity'] = int(request.args.get('quantity'))
            product['price'] = float(request.args.get('price'))
            return jsonify(product)
    return jsonify({'message': 'Product not found'}), 404


# Patch endpoint to update a specific product by ID


@app.route('/products/<int:product_id>', methods=['PATCH'])
def patch_product(product_id):
    for product in products:
        if product['id'] == product_id:
            if 'item' in request.args:
                product['item'] = request.args.get('item')
            if 'quantity' in request.args:
                product['quantity'] = int(request.args.get('quantity'))
            if 'price' in request.args:
                product['price'] = float(request.args.get('price'))
            return jsonify(product)
    return jsonify({'message': 'Product not found'}), 404

# Delete endpoint to delete a specific product by ID


@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    for product in products:
        if product['id'] == product_id:
            products.remove(product)
            return jsonify({'message': 'Product deleted'})
    return jsonify({'message': 'Product not found'}), 404


if __name__ == '__main__':
    app.run()
