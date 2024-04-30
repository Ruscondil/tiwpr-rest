from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Sample data
purchases = []
products = []
#
#        'id': int,
#        'name': string,
#        'quantity': int,
#        'price': float(,
#        'discounted_price': float,
#        'discounted_price_date': datetime
users = []
discounts = []
# GET endpoint to retrieve all products


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


def change_discounted_price(product_id, discounted_price, discounted_price_date):
    for product in products:
        if product['id'] == product_id:
            product['discounted_price'] = float(discounted_price)
            product['discounted_price_date'] = discounted_price_date
            return True
    return False


@app.route('/purchases', methods=['GET'])
def get_purchases():
    return jsonify(purchases)


# POST endpoint to create a new purchase
@app.route('/purchases', methods=['POST'])
def create_purchase():
    data = request.get_json()
    # TODO sprawdzanie czy user istnieje
    # TODO sprawdzanie poprawnośći formatów
    if not data or 'user_id' not in data or 'purchases' not in data:
        return jsonify({'message': 'No user_id or purchases provided'}), 400

    user_id = data['user_id']
    items = data['purchases']
    purchased_items = []

    for item in items:  # checking if has enough quantity of all the product
        if get_quantity(int(item['product_id'])) < int(item['quantity']):
            return jsonify({'message': 'Too little quantity of one of the products'}), 400

    for item in items:
        change_product_quantity(
            int(item['product_id']), -1 * int(item['quantity']))
        purchased_items.append(item)

    new_purchase = {
        'id': len(purchases) + 1,
        'user_id': user_id,
        'purchase': purchased_items,
    }
    purchases.append(new_purchase)

    return jsonify({'message': 'Purchases created'}), 201

# GET endpoint to retrieve a specific purchase by ID


@app.route('/purchases/<int:purchase_id>', methods=['GET'])
def get_purchase(purchase_id):
    for purchase in purchases:
        if purchase['id'] == purchase_id:
            return jsonify(purchase)
    return jsonify({'message': 'Purchase not found'}), 404


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

            if not name or not quantity or not price:
                return jsonify({'message': 'Missing required fields'}), 400

            try:
                quantity = int(quantity)
                price = float(price)
            except ValueError:
                return jsonify({'message': 'Invalid data types'}), 400

            product['name'] = name
            product['quantity'] = int(quantity)
            product['price'] = float(price)
            return jsonify(product)
    return jsonify({'message': 'Product not found'}), 404


# Patch endpoint to update a specific product by ID


@app.route('/products/<int:product_id>', methods=['PATCH'])
def patch_product(product_id):
    # TODO sprawdzanie poprawnośći formatów
    for product in products:
        if product['id'] == product_id:
            if 'name' in request.json:
                product['name'] = request.json.get('name')
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


def check_user_exists(user_id):
    for user in users:
        if user['id'] == user_id:
            return True
    return False


# POST endpoint to create a new user


@app.route('/users', methods=['POST'])
def create_user():
    name = request.json.get('name')
    email = request.json.get('email')

    if not name or not email:
        return jsonify({'message': 'Name and email are required'}), 400

    if '@' not in email or '.' not in email:
        return jsonify({'message': 'Invalid email format'}), 400

    new_user = {
        'id': len(users) + 1,
        'name': name,
        'email': email
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
    # TODO sprawdzanie poprawnośći formatów
    for user in users:
        if user['id'] == user_id:
            name = request.json.get('name')
            email = request.json.get('email')

            if not name or not email:
                return jsonify({'message': 'Name and email are required'}), 400

            if '@' not in email or '.' not in email:
                return jsonify({'message': 'Invalid email format'}), 400

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
                email = request.json.get('email')
                if '@' not in email or '.' not in email:
                    return jsonify({'message': 'Invalid email format'}), 400
                user['email'] = email
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


# POST endpoint to create a new discount


@app.route('/discounts', methods=['POST'])
def create_discount():
    # TODO sprawdzanie poprawnośći formatów
    # TODO sprawdzanie czy zosało już coś przecenione

    data = request.get_json()
    if not data or 'discounted_price_date' not in data or 'discounted_items' not in data:
        return jsonify({'message': 'No discounted_price_date or discounts provided'}), 400

    discounted_price_date = datetime.strptime(
        data['discounted_price_date'], '%Y-%m-%d').date()
    items = data['discounted_items']

    for item in items:
        change_discounted_price(
            int(item['item_id']), float(item["discounted_price"]), discounted_price_date)

    new_discount = {
        'id': len(discounts) + 1,
        'discounted_price_date': discounted_price_date,
        'discounted_items': items,
    }
    discounts.append(new_discount)

    return jsonify(new_discount), 201


# GET endpoint to retrieve all discounts
@app.route('/discounts', methods=['GET'])
def get_discounts():
    return jsonify(discounts)


# GET endpoint to retrieve a specific discount by ID
@app.route('/discounts/<int:discount_id>', methods=['GET'])
def get_discount(discount_id):
    for discount in discounts:
        if discount['id'] == discount_id:
            return jsonify(discount)
    return jsonify({'message': 'Discount not found'}), 404

# PUT endpoint to update a specific discount by ID


@app.route('/discounts/<int:discount_id>', methods=['PUT'])
def update_discount(discount_id):
    # TODO sprawdzanie poprawnośći formatów
    for discount in discounts:
        if discount['id'] == discount_id:

            discounted_price_date = request.json.get('discounted_price_date')
            discounted_items = request.json.get('discounted_items')

            if discounted_price_date is None or discounted_items is None:
                return jsonify({'message': 'Missing parameters'}), 400

            for item in discount['discounted_items']:  # revert changes
                change_discounted_price(int(item['item_id']), -1, -1)

            for item in discounted_items:  # add new changes
                change_discounted_price(
                    int(item['item_id']), item['discounted_price'], discounted_price_date)

            # change info in discounts
            discount['discounted_price_date'] = datetime.strptime(
                discounted_price_date, '%Y-%m-%d').date()

            discount['discounted_items'] = discounted_items

            return jsonify(discount)
    return jsonify({'message': 'Discount not found'}), 404

# DELETE endpoint to delete a specific discount by ID


@app.route('/discounts/<int:discount_id>', methods=['DELETE'])
def delete_discount(discount_id):
    for discount in discounts:
        if discount['id'] == discount_id:

            for item in discount['discounted_items']:  # revert changes
                change_discounted_price(int(item['item_id']), -1, -1)

            discounts.remove(discount)
            return jsonify({'message': 'Discount deleted'})
    return jsonify({'message': 'Discount not found'}), 404


if __name__ == '__main__':
    app.run()
