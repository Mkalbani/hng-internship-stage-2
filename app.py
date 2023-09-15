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

# Create a user resource
@app.route('/api', methods=['POST'])
def create_user():
    # Extract JSON data from the request
    data = request.json

    # Check if the "name" field exists in the request data
    if "name" not in data:
        return jsonify({"message": "Name is required"}), 400

    # Assign the name from the request data
    name = data["name"]

    # Create a new user object with an incremental _id and predefined ID
    user_id = users_collection.insert_one({"name": name, "_id": 1}).inserted_id
    new_user = {"_id": user_id, "name": name}

    # Return a success response with a 201 status code
    return jsonify({"message": "User created successfully", "user": new_user}), 201

# Get all users
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

# Update a user by user_id
@app.route('/api/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    # Extract JSON data from the request
    data = request.json

    # Update the user in the MongoDB collection by user_id
    result = users_collection.update_one({"_id": user_id}, {"$set": data})

    # If no user was updated, return a 404 error response
    if result.modified_count == 0:
        return jsonify({"message": "User not found"}), 404

    # Return a success response
    return jsonify({"message": "User updated successfully"})

# Delete a user by user_id
@app.route('/api/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Delete a user from the MongoDB collection by user_id
    result = users_collection.delete_one({"_id": user_id})

    # If no user was deleted, return a 404 error response
    if result.deleted_count == 0:
        return jsonify({"message": "User not found"}), 404

    # Return a success response with a 204 status code (No Content)
    return jsonify({"message": "User deleted successfully"}), 204

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
