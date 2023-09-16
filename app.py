# Import config from decouple
from pymongo.errors import ServerSelectionTimeoutError
from flask import Flask, request, jsonify
from pymongo import MongoClient

# Create a Flask app instance
app = Flask(__name__)

# Configure Flask-PyMongo with the MongoDB URI
app.config["MONGO_URI"] = "mongodb+srv://user:test234@cluster0.5amxkrp.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(app.config["MONGO_URI"])

# Set up MongoDB
db = client.get_database('users')
users_collection = db.users

# Get all users
@app.route('/api', methods=['GET'])
def get_all_users():
    # Retrieve all users from the MongoDB collection
    users = list(users_collection.find())

    # Check if there are no users in the collection
    if not users:
        return jsonify({"message": "No users found"}), 404

    # Convert ObjectId values to strings
    for user in users:
        user["_id"] = str(user["_id"])

    # Return the list of users as a JSON response
    return jsonify(users)

# Get a user by user_id
@app.route('/api/<string:user_id>', methods=['GET'])
def get_user(user_id):
    # Find a user in the MongoDB collection by user_id
    user = users_collection.find_one({"_id": user_id})

    # If the user is not found, return a 404 error response
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Return the user data as a JSON response
    return jsonify(user)

# Create a user resource
@app.route('/api', methods=['POST'])
def create_user():
    try:
        # Get the user name from the request JSON data
        user_data = request.get_json()
        
        # Check if the required "name" field is present in the request data
        if 'name' in user_data:
            name = user_data['name']
            
            # Generate a unique ID for the user
            user_id = users_collection.count_documents({}) + 1
            # user_id = str(ObjectId())

            # Insert the user data into the MongoDB collection
            user = {"_id": user_id, "name": name}
            users_collection.insert_one(user)

            return jsonify({'message': 'User added successfully', '_id': user_id}), 201
        else:
            return jsonify({'error': 'Name is required in the request data'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update a user by name
@app.route('/api/{user_name}>', methods=['PUT'])
def update_user_by_name(user_name):
    # Extract JSON data from the request
    data = request.get_json()
    new = users_collection.find_one({"name": user_name})
    if new == None:
        return {"message": "User not found"}, 404
    updated_data = {"$set": data}
    result = users_collection.update_one({"name": user_name}, updated_data)
    if result.modified_count == 0:
        return {"message": "User found, but nothing updated"}, 200
    else:
        return parse_json(users_collection.find_one({"name": user_name})), 201

    # # Update the user in the MongoDB collection by name
    # result = users_collection.update_one({"name": user_name}, {"$set": data})

    # # If no user was updated, return a 404 error response
    # if result.modified_count == 0:
    #     return jsonify({"message": "User not found"}), 404

    # # Return a success response
    # return jsonify({"message": "User updated successfully"})

# Delete a user by name
@app.route('/api/{user_name}', methods=['DELETE'])
def delete_user_by_name(user_name):
    result = users_collection.delete_one({"name": user_name})
    if result.deleted_count == 0:
        return {"message": "User not found"}, 404
    else:
        return jsonify({"message": "User deleted successfully"}), 204


    # Find a user in the MongoDB collection by name
    user = users_collection.find_one({"name": user_name})

    # If the user is not found, return a 404 error response
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Delete the user from the MongoDB collection
    result = users_collection.delete_one({"name": user_name})

    # Check if the user was successfully deleted
    if result.deleted_count == 0:
        return jsonify({"message": "User deletion failed"}), 500

    # Return a success response with a 204 status code (No Content)
    return jsonify({"message": "User deleted successfully"}), 204

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
