from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
purchases = []
products = []
users = []
# GET endpoint to retrieve all products


@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

# POST endpoint to create a new products


@app.route('/products', methods=['POST'])
def create_product():

    new_product = {
        'id': len(products) + 1,
        'item': request.json.get('item'),
        'quantity': int(request.json.get('quantity')),
        'price': float(request.json.get('price'))
    }
    products.append(new_product)
    return jsonify(new_product), 201


def check_product_exists(product_id):
    for product in products:
        if product['id'] == product_id:
            return True
    return False


def get_quantity(item_id):
    for product in products:
        if product['id'] == item_id:
            return product['quantity']
    return None


def subtract_product_quantity(product_id, subract_quantity):
    for product in products:
        if product['id'] == product_id:
            if product['quantity'] > subract_quantity:
                product['quantity'] = product['quantity'] - subract_quantity
                return True
    return False


@app.route('/purchases', methods=['GET'])
def get_purchases():
    return jsonify(products)


# POST endpoint to create a new purchase


@app.route('/purchases', methods=['POST'])
def create_purchase():
    items = request.get_json()
    if not items:
        return jsonify({'message': 'No items provided'}), 400

    for item in items:
        new_purchase = {
            'id': len(purchases) + 1,
            'item': item['item'],
            'quantity': int(item['quantity'])
        }
        purchases.append(new_purchase)

    return jsonify({'message': 'Purchases created'}), 201


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
            item = request.json.get('item')
            quantity = request.json.get('quantity')
            price = request.json.get('price')

            if item is None or quantity is None or price is None:
                return jsonify({'message': 'Missing parameters'}), 400

            product['item'] = item
            product['quantity'] = int(quantity)
            product['price'] = float(price)
            return jsonify(product)
    return jsonify({'message': 'Product not found'}), 404


# Patch endpoint to update a specific product by ID


@app.route('/products/<int:product_id>', methods=['PATCH'])
def patch_product(product_id):
    for product in products:
        if product['id'] == product_id:
            if 'item' in request.json:
                product['item'] = request.json.get('item')
            if 'quantity' in request.json:
                product['quantity'] = int(request.json.get('quantity'))
            if 'price' in request.json:
                product['price'] = float(request.json.get('price'))
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

# GET endpoint to retrieve all users


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# POST endpoint to create a new user


@app.route('/users', methods=['POST'])
def create_user():
    new_user = {
        'id': len(users) + 1,
        'name': request.json.get('name'),
        'email': request.json.get('email')
    }
    users.append(new_user)
    return jsonify(new_user), 201
# GET endpoint to retrieve a specific user by ID


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    for user in users:
        if user['id'] == user_id:
            return jsonify(user)
    return jsonify({'message': 'User not found'}), 404

# PUT endpoint to update a specific user by ID


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    for user in users:
        if user['id'] == user_id:
            name = request.json.get('name')
            email = request.json.get('email')

            if name is None or email is None:
                return jsonify({'message': 'Missing parameters'}), 400

            user['name'] = name
            user['email'] = email
            return jsonify(user)
    return jsonify({'message': 'User not found'}), 404

# PATCH endpoint to update a specific user by ID


@app.route('/users/<int:user_id>', methods=['PATCH'])
def patch_user(user_id):
    for user in users:
        if user['id'] == user_id:
            if 'name' in request.json:
                user['name'] = request.json.get('name')
            if 'email' in request.json:
                user['email'] = request.json.get('email')
            return jsonify(user)
    return jsonify({'message': 'User not found'}), 404

# DELETE endpoint to delete a specific user by ID


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    for user in users:
        if user['id'] == user_id:
            users.remove(user)
            return jsonify({'message': 'User deleted'})
    return jsonify({'message': 'User not found'}), 404


if __name__ == '__main__':
    app.run()
