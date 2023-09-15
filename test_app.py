import unittest
from flask import Flask, jsonify
from app import app  # Import your Flask app instance

class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()  # Create a test client for the Flask app
        self.app.testing = True  # Set the app to testing mode

    def test_get_all_users(self):
        response = self.app.get('/users')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, list))  # Check if the response is a list

    def test_get_user(self):
        response = self.app.get('/users/0')  # Assuming you have a user with _id 0
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, dict))  # Check if the response is a dictionary

    def test_get_nonexistent_user(self):
        response = self.app.get('/users/nonexistent')  # Assuming no user with this ID
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], "User not found")

    def test_create_user(self):
        new_user = {"new_user": "John"}
        response = self.app.post('/users', json=new_user)
        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['message'], "User created successfully")
        self.assertTrue(isinstance(data['user'], dict))

    def test_create_user_missing_name(self):
        new_user = {"invalid_key": "John"}  # Missing "new_user" key
        response = self.app.post('/users', json=new_user)
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], "Name is required")

    def test_update_user(self):
        user_data = {"name": "Updated Name"}
        response = self.app.put('/users/0', json=user_data)  # Assuming you have a user with _id 0
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], "User updated successfully")

    def test_update_nonexistent_user(self):
        user_data = {"name": "Updated Name"}
        response = self.app.put('/users/nonexistent', json=user_data)  # Assuming no user with this ID
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], "User not found")

    def test_delete_user(self):
        response = self.app.delete('/users/0')  # Assuming you have a user with _id 0
        self.assertEqual(response.status_code, 204)

    def test_delete_nonexistent_user(self):
        response = self.app.delete('/users/nonexistent')  # Assuming no user with this ID
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], "User not found")

if __name__ == '__main__':
    unittest.main()
