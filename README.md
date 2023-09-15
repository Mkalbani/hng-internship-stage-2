# Flask CRUD App

This is a simple Flask web application that demonstrates CRUD (Create, Read, Update, Delete) operations using a MongoDB database. The app allows you to manage user records, including their names.

## Prerequisites

Before running the app, make sure you have the following dependencies installed:

- Python 3.x
- Flask
- Flask-PyMongo
- pymongo

You can install these dependencies using pip:

```bash
pip install flask flask-pymongo pymongo
git clone https://github.com/mkothm/hng-internship-stage-2.git
cd hng-internship-stage-2
app.config["MONGO_URI"] = "mongodb://yourusername:yourpassword@yourmongodbhost/yourdatabasename"
python app.py
```
# Create a User
curl -X POST http://localhost:5000/api -H "Content-Type: application/json" -d '{"name": "John"}'

{
    "message": "User created successfully",
    "user": {
        "_id": "user_id",
        "name": "musa"
    }
}
# Read Users
[
    {
        "_id": "user_id1",
        "name": "John"
    },
    {
        "_id": "user_id2",
        "name": "Alice"
    },
    ...
]

# Update User
curl -X PUT http://localhost:5000/api/user_id1 -H "Content-Type: application/json" -d '{"name": "Updated Name"}'
## Response 
{
    "message": "User updated successfully"
}
# Delete User
{
    "message": "User deleted successfully"
}

