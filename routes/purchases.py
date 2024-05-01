
from flask import jsonify, request
from flask_app import app
from routes.products import change_product_quantity, get_quantity

purchases = []


@app.route('/purchases', methods=['GET'])
def get_purchases():
    return jsonify(purchases)

# POST endpoint to create a new purchase


@app.route('/purchases', methods=['POST'])
def create_purchase():

    purchased_items = []
    data = request.get_json()

    if not data or 'user_id' not in data or 'purchases' not in data:
        return jsonify({'message': 'No user_id or purchases provided'}), 400

    user_id = data['user_id']
    items = data['purchases']

    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({'message': 'Invalid user_id'}), 400

    for item in items:  # checking if has enough quantity of all the product
        if 'product_id' not in item or 'quantity' not in item:
            return jsonify({'message': 'No product_id or quantity provided'}), 400

        try:
            product_id = int(item['product_id'])
            quantity = int(item['quantity'])
        except ValueError:
            return jsonify({'message': 'Invalid product_id or quantity'}), 400

        if product_id <= 0:
            return jsonify({'message': 'No product_id '}), 400

        if quantity <= 0:
            return jsonify({'message': 'Quantity must be greater than 0'}), 400

        product_quantity = get_quantity(product_id)

        if product_quantity is None:
            return jsonify({'message': 'Product not found'}), 404

        if product_quantity < quantity:
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
