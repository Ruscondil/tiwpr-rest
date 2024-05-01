
from flask import jsonify, request
from datetime import datetime
from flask_app import app
# GET endpoint to retrieve all products


products = []
#
#        'id': int,
#        'name': string,
#        'quantity': int,
#        'price': float(,
#        'discounted_price': float,
#        'discounted_price_date': datetime


def check_product_exists(product_id):
    for product in products:
        if product['id'] == product_id:
            return True
    return False


def get_quantity(product_id):
    for product in products:
        if product['id'] == product_id:
            return product['quantity']
    return None


def change_product_quantity(product_id, quantity_change):
    for product in products:
        if product['id'] == product_id:
            if quantity_change > 0 or (quantity_change < 0 and product['quantity'] >= quantity_change):
                product['quantity'] = product['quantity'] + quantity_change
                return True
    return False


def is_item_discounted(product_id):
    for product in products:
        if product['id'] == product_id:
            return product['discounted_price'] < product['price']
    return False


@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

# POST endpoint to create a new products


@app.route('/products', methods=['POST'])
def create_product():
    name = request.json.get('name')
    quantity = request.json.get('quantity')
    price = request.json.get('price')
    discounted_price = request.json.get('discounted_price')
    discounted_price_date = request.json.get('discounted_price_date')

    if not name or not quantity or not price or not discounted_price_date:
        return jsonify({'message': 'Missing required fields'}), 400

    try:
        quantity = int(quantity)
        price = float(price)
        discounted_price = float(discounted_price)
        discounted_price_date = datetime.strptime(
            discounted_price_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'message': 'Invalid data types'}), 400

    if quantity <= 0 or price <= 0 or discounted_price <= 0:
        return jsonify({'message': 'Quantity, price, and discounted price must be greater than 0'}), 400

    new_product = {
        'id': len(products) + 1,
        'name': name,
        'quantity': quantity,
        'price': price,
        'discounted_price': discounted_price,
        'discounted_price_date': discounted_price_date
    }
    products.append(new_product)
    return jsonify(new_product), 201


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
            name = request.json.get('name')
            quantity = request.json.get('quantity')
            price = request.json.get('price')
            discounted_price = request.json.get('discounted_price')
            discounted_price_date = request.json.get('discounted_price_date')

            if not name or not quantity or not price or not discounted_price_date:
                return jsonify({'message': 'Missing required fields'}), 400

            try:
                quantity = int(quantity)
                price = float(price)
                discounted_price = float(discounted_price)
                discounted_price_date = datetime.strptime(
                    discounted_price_date, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'message': 'Invalid data types'}), 400

            if quantity <= 0 or price <= 0 or discounted_price <= 0:
                return jsonify({'message': 'Quantity, price, and discounted price must be greater than 0'}), 400

            product['name'] = name
            product['quantity'] = int(quantity)
            product['price'] = float(price)
            product['discounted_price'] = float(discounted_price)
            product['discounted_price_date'] = discounted_price_date
            return jsonify(product)
    return jsonify({'message': 'Product not found'}), 404


# Patch endpoint to update a specific product by ID


@app.route('/products/<int:product_id>', methods=['PATCH'])
def patch_product(product_id):
    for product in products:
        if product['id'] == product_id:
            if 'name' in request.json:
                product['name'] = request.json.get('name')
            if 'quantity' in request.json:
                quantity = request.json.get('quantity')
                try:
                    quantity = int(quantity)
                    if quantity <= 0:
                        return jsonify({'message': 'Quantity must be greater than 0'}), 400
                    product['quantity'] = quantity
                except ValueError:
                    return jsonify({'message': 'Invalid data type for quantity'}), 400
            if 'price' in request.json:
                price = request.json.get('price')
                try:
                    price = float(price)
                    if price <= 0:
                        return jsonify({'message': 'Price must be greater than 0'}), 400
                    product['price'] = price
                except ValueError:
                    return jsonify({'message': 'Invalid data type for price'}), 400
            if 'discounted_price' in request.json:
                discounted_price = request.json.get('discounted_price')
                try:
                    discounted_price = float(discounted_price)
                    if discounted_price <= 0:
                        return jsonify({'message': 'Discounted price must be greater than 0'}), 400
                    product['discounted_price'] = discounted_price
                except ValueError:
                    return jsonify({'message': 'Invalid data type for discounted_price'}), 400

            if 'discounted_price_date' in request.json:
                discounted_price_date = request.json.get(
                    'discounted_price_date')
                try:
                    discounted_price_date = datetime.strptime(
                        discounted_price_date, '%Y-%m-%d').date()
                except ValueError:
                    return jsonify({'message': 'Invalid data type for discounted_price_date'}), 400
                product['discounted_price_date'] = discounted_price_date
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
