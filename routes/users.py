
from flask import jsonify, request
from flask_app import app
# GET endpoint to retrieve all users


users = []


def check_user_exists(user_id):
    for user in users:
        if user['id'] == user_id:
            return True
    return False


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

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
