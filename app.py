# Import config from decouple
import os
import json
import pymongo
from flask import Flask, jsonify, request, make_response, abort, url_for  # noqa; F401
from pymongo import MongoClient
from bson import json_util
from pymongo.errors import OperationFailure
from pymongo.results import InsertOneResult
from bson.objectid import ObjectId
import sys


songs_list = [{}]

# Create a Flask app instance
app = Flask(__name__)

# Configure Flask-PyMongo with the MongoDB URI
app.config["MONGO_URI"] = "mongodb+srv://user:test234@cluster0.5amxkrp.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(app.config["MONGO_URI"])

# Set up MongoDB
db = client.songs
db.songs.drop()
db.songs.insert_many(songs_list)

db = client.songs
db.songs.drop()
db.songs.insert_many(songs_list)

@app.route("/song")
def songs():
    listofsongs = db.songs.find({})
    return jsonify({"songs":parse_json(listofsongs)}), 200

# RETURN SONG BY ID

@app.route("/song/<int:id>")
def get_song_by_id(id):
    song = db.songs.find_one({"id":id})
    if song:
        return jsonify({"songs":parse_json(song)}), 200
    return ({"message":"song with id not found"}), 404

# CREATE A SONG

@app.route("/song", methods=["POST"])
def create_song():
    new_song = request.json
    print(new_song["id"])
    test=db.songs.find_one({"id":new_song["id"]})
    if test:
      return {"Message": "song with id " + str(new_song['id']) + " already present"}, 302
    insert_id = db.songs.insert_one(new_song)
    return jsonify({"inserted id":parse_json(insert_id,inserted_id)}), 201

# UPDATE A SONG

@app.route("/song/<int:id>", methods=["PUT"])
def update_song(id):
    change_song = request.json
    test=db.songs.find_one({"id":id})
    if test == None:
        return {"Message":"song not found"}, 404
    new_data = {"$set":change_song}
    result=db.songs.update_one({"id":id}, new_data)
    if result.modified_count == 0:
        return {"message": "song found, but nothing updated"}, 200
    else:
        return jsonify(parse_json(db.songs.find_one({"id":id}))),201

# DELETE A SONG

@app.route("/song/<int:id>", methods=["DELETE"])
def delete_song(id):
    result=db.songs.delete_one({"id":id})
    if result.deleted_count == 0:
        return {"Message":"song not found"}, 404
    else:
        return "", 204

# # Import config from decouple
# from platformdirs import user_data_dir
# from pymongo.errors import ServerSelectionTimeoutError
# from flask import Flask, request, jsonify
# from pymongo import MongoClient

# # Create a Flask capp instance
# app = Flask(__name__)

# # Configure Flask-PyMongo with the MongoDB URI
# app.config["MONGO_URI"] = "mongodb+srv://user:test234@cluster0.5amxkrp.mongodb.net/?retryWrites=true&w=majority"
# client = MongoClient(app.config["MONGO_URI"])

# # Set up MongoDB
# db = client.get_database('users')
# users_collection = db.users

# # Get all users
# @app.route('/api', methods=['GET'])
# def get_all_users():
#     # Retrieve all users from the MongoDB collection
#     users = list(users_collection.find())

#     # Check if there are no users in the collection
#     if not users:
#         return jsonify({"message": "No users found"}), 404

#     # Convert ObjectId values to strings
#     for user in users:
#         user["_id"] = str(user["_id"])

#     # Return the list of users as a JSON response
#     return jsonify(users)

# # Get a user by user_id
# @app.route('/api/<int:user_id>', methods=['GET'])
# def get_user(user_id):
#     # Find a user in the MongoDB collection by user_id
#     user = users_collection.find_one({"_id": user_id})

#     # If the user is not found, return a 404 error response
#     if not user:
#         return jsonify({"message": "User not found"}), 404

#     # Return the user data as a JSON response
#     return jsonify(user)

# # Create a user resource
# @app.route('/api', methods=['POST'])
# def create_user():
#     try:
#         # Get the user name from the request JSON data
#         user_data = request.get_json()
        
#         # Check if the required "name" field is present in the request data
#         if 'name' in user_data:
#             name = user_data['name']
            
#             # Generate a unique ID for the user
#             user_id = users_collection.count_documents({}) + 1
#             # user_id = str(ObjectId())

#             # Insert the user data into the MongoDB collection
#             user = {"_id": user_id, "name": name}
#             users_collection.insert_one(user)

#             return jsonify({'message': 'User added successfully', 'user_id': user_id}), 201
#         else:
#             return jsonify({'error': 'Name is required in the request data'}), 400
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # Update a user by user_id
# @app.route('/api/<string:user_id>', methods=['PUT'])
# def update_user(user_id):
#     # Extract JSON data from the request
    
#     data = request.get_json()

#     # Update the existing user
#     updated_data = {"$set": data}
#     result = users_collection.update_one({"_id": user_id}, updated_data)
#     if result.modified_count == 0:
#         return {"message": "User found, but nothing updated"}, 200
#     else:
#         return {"message": "User updated"}, 200

# # @app.route('/api/<string:user_id>', methods=['PUT'])
# # def update_user(user_id):
# #     # Extract JSON data from the request
# #     data = request.json

# #     # Update the user in the MongoDB collection by user_id
# #     result = users_collection.update_one({"_id": user_id}, {"$set": data})

# #     # If no user was updated, return a 404 error response
# #     if result.modified_count == 0:
# #         return jsonify({"message": "User not found"}), 404

# #     # Return a success response
# #     return jsonify({"message": "User updated successfully"})
# # Delete a user by name
# @app.route('/api/<string:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     result = users_collection.delete_one({"_id": user_id})

#     if result.deleted_count == 0:
#         return {"message": "User not found"}, 404
#     return jsonify({"message": "User deleted successfully"}), 204


# # Delete a user by user_id
# # @app.route('/api/<string:user_id>', methods=['DELETE'])
# # def delete_user(user_id):
# #     # Delete a user from the MongoDB collection by user_id
# #     result = users_collection.delete_one({"_id": user_id})

# #     # If no user was deleted, return a 404 error response
# #     if result.deleted_count == 0:
# #         return jsonify({"message": "User not found"}), 404

# #     # Return a success response with a 204 status code (No Content)
# #     return jsonify({"message": "User deleted successfully"}), 204

# # Run the Flask app
# if __name__ == '__main__':
#     app.run(debug=True)
