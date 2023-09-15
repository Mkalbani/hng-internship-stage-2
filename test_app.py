import unittest
import json
from flask import Flask
from app import app


class TestAppRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True


    def test_create_user(self):
        data = {"name": "John"}
        response = self.client.post('/api', json=data)
        assert response.status_code == 201

    def test_create_user(self):
        # Create a user data to be sent in the request
        user_data = {"name": "John"}

        # Perform a POST request to create a user
        response = self.app.post('/api', json=user_data)

        # Check if the response status code is 201 (Created)
        self.assertEqual(response.status_code, 201)

        # Optionally, you can check the response content for correctness
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data["message"], "User created successfully")
        self.assertIn("user", data)  # Ensure "user" key is present in the response

    def test_create_user(self):
        data = {"name": "musa"}
        response = self.app.post('/api', json=data)

        # Check if the status code is 201 (Created)
        self.assertEqual(response.status_code, 201)

        # Parse the response data as JSON
        response_data = json.loads(response.data.decode('utf-8'))

        # Check if the response message is as expected
        self.assertEqual(response_data['message'], "User created successfully")

        # Check if the response data contains the user information
        self.assertTrue('user' in response_data)
        user = response_data['user']
        self.assertTrue('_id' in user)
        self.assertEqual(user['name'], "musa")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["message"], "User created successfully")
        self.assertTrue("user" in data)

    def test_create_user_missing_name(self):
        data = {}  # Missing "name" field
        response = self.app.post('/api', json=data)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Name is required")

    def test_get_all_users(self):
        response = self.app.get('/api')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, list))

    def test_get_user(self):
        # Create a user for testing
        user_id = users_collection.insert_one({"name": "John"}).inserted_id

        # Perform a GET request with the created user's ID
        response = self.app.get(f'/api/{user_id}')
        
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the response JSON contains the expected ID and name
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data["_id"], str(user_id))
        self.assertEqual(data["name"], "John")

    def test_get_user_not_found(self):
        user_id = 'non_existent_user_id'
        response = self.app.get(f'/api/{user_id}')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "User not found")

    # Add similar test methods for update_user and delete_user routes

if __name__ == '__main__':
    unittest.main()
