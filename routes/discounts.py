
from flask import jsonify, request
from datetime import datetime
from flask_app import app
from routes.products import products

discounts = []


def is_discounted(product_id):  # check if product is already discounted
    for product in products:
        if product['id'] == product_id:
            return not product['discounted_price'] == -1
    return None


def change_discounted_price(product_id, discounted_price, discounted_price_date):
    for product in products:
        if product['id'] == product_id:
            product['discounted_price'] = float(discounted_price)
            product['discounted_price_date'] = discounted_price_date
            return True
    return False
# POST endpoint to create a new discount


@app.route('/discounts', methods=['POST'])
def create_discount():

    data = request.get_json()
    if not data or 'discounted_price_date' not in data or 'discounted_items' not in data:
        return jsonify({'message': 'No discounted_price_date or discounts provided'}), 400

    discounted_price_date = datetime.strptime(
        data['discounted_price_date'], '%Y-%m-%d').date()
    items = data['discounted_items']

    for item in items:  # precheckig all products
        if 'product_id' not in item or 'discounted_price' not in item:
            return jsonify({'message': 'No product_id or discounted price provided'}), 400

        try:
            product_id = int(item['product_id'])
            discounted_price = float(item['discounted_price'])
        except ValueError:
            return jsonify({'message': 'Invalid product_id or discounted_price'}), 400

        if product_id <= 0:
            return jsonify({'message': 'No product_id '}), 400

        if discounted_price <= 0:
            return jsonify({'message': 'Discounted price must be greater than 0'}), 400

        discounted = is_discounted(product_id)
        print(discounted)
        if discounted or discounted is None:
            return jsonify({'message': 'Product already discounted'}), 400

    for item in items:
        change_discounted_price(
            int(item['product_id']), float(item["discounted_price"]), discounted_price_date)

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

            data = request.get_json()
            if not data or 'discounted_price_date' not in data or 'discounted_items' not in data:
                return jsonify({'message': 'No discounted_price_date or discounts provided'}), 400

            discounted_price_date = datetime.strptime(
                data['discounted_price_date'], '%Y-%m-%d').date()
            items = data['discounted_items']

            for item in items:  # precheckig all products
                if 'product_id' not in item or 'discounted_price' not in item:
                    return jsonify({'message': 'No product_id or discounted price provided'}), 400

                try:
                    product_id = int(item['product_id'])
                    discounted_price = float(item['discounted_price'])
                except ValueError:
                    return jsonify({'message': 'Invalid product_id or discounted_price'}), 400

                if product_id <= 0:
                    return jsonify({'message': 'Product not found'}), 404

                if discounted_price <= 0:
                    return jsonify({'message': 'Discounted price must be greater than 0'}), 400

                discounted = is_discounted(product_id)
                is_in_old_discount = int(
                    item['product_id']) in [product['product_id'] for product in discount['discounted_items']]
                print("old", is_in_old_discount)
                if not is_in_old_discount:
                    if discounted:
                        return jsonify({'message': 'Product already discounted'}), 400
                    if discounted is None:
                        return jsonify({'message': 'Product not found'}), 404

            for item in items:
                change_discounted_price(
                    int(item['product_id']), float(item["discounted_price"]), discounted_price_date)

            for item in discount['discounted_items']:  # revert changes
                change_discounted_price(int(item['product_id']), -1, -1)

            for item in items:  # add new changes
                change_discounted_price(
                    int(item['product_id']), item['discounted_price'], discounted_price_date)

            # change info in discounts
            discount['discounted_price_date'] = discounted_price_date

            discount['discounted_items'] = items

            return jsonify(discount)
    return jsonify({'message': 'Discount not found'}), 404

# DELETE endpoint to delete a specific discount by ID


@ app.route('/discounts/<int:discount_id>', methods=['DELETE'])
def delete_discount(discount_id):
    for discount in discounts:
        if discount['id'] == discount_id:

            for item in discount['discounted_items']:  # revert changes
                change_discounted_price(int(item['product_id']), -1, -1)

            discounts.remove(discount)
            return jsonify({'message': 'Discount deleted'})
    return jsonify({'message': 'Discount not found'}), 404
