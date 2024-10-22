import pytest
from flask import json
from database import app, create_db_table, insert_user, get_users, get_user_by_id, update_user, delete_user  # Adjust import for your functions

# Setup the test client
@pytest.fixture(scope='module', autouse=True)
def test_client():
    app.config['TESTING'] = True
    client = app.test_client()

    # Create the database and table before any tests run
    create_db_table()
    
    yield client  # this will run the tests

    # Optionally: Cleanup code could go here (e.g., dropping the database)


# Test that the database is created with the specified users
def test_initial_users(test_client):
    # Insert some initial users (adjust based on your requirements)
    initial_users = [
        {"name": "John Doe", "email": "john@example.com", "phone": "1234567890", "address": "123 Main St", "country": "USA"},
        {"name": "Jane Smith", "email": "jane@example.com", "phone": "0987654321", "address": "456 Elm St", "country": "USA"},
    ]

    for user in initial_users:
        insert_user(user)

    # Get users and check if they were added
    response = test_client.get('/api/users')
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert len(data) == len(initial_users)


# Test insert_user()
def test_insert_user(test_client):
    new_user = {"name": "Alice Brown", "email": "alice@example.com", "phone": "5555555555", "address": "789 Pine St", "country": "USA"}
    
    response = test_client.post('/api/users/add', data=json.dumps(new_user), content_type='application/json')
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['user_id'] is not None  # Check that a user ID was returned
    assert data['name'] == new_user['name']


# Test get_users()
def test_get_users(test_client):
    response = test_client.get('/api/users')
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert isinstance(data, list)  # Ensure it's a list
    assert len(data) > 0  # Ensure there are users


# Test get_user_by_id()
def test_get_user_by_id(test_client):
    user_id = 1  # Adjust based on your test data
    response = test_client.get(f'/api/users/{user_id}')
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['user_id'] == user_id  # Check for correct user ID


# Test update_user()
def test_update_user(test_client):
    updated_user = {"user_id": 1, "name": "John Updated", "email": "john.updated@example.com", "phone": "1234567890", "address": "123 Main St", "country": "USA"}
    
    response = test_client.put('/api/users/update', data=json.dumps(updated_user), content_type='application/json')
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['name'] == updated_user['name']  # Verify the name was updated


# Test delete_user()
def test_delete_user(test_client):
    user_id = 3  # Use an existing user ID
    response = test_client.delete(f'/api/users/delete/{user_id}')
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['status'] == "User deleted successfully"  # Check for success message

    # Verify that the user was deleted
    response_check = test_client.get(f'/api/users/{user_id}')
    assert response_check.status_code == 404  # Expecting 404 for not found


# Test api_get_user()
def test_api_get_user(test_client):
    user_id = 1  # Adjust based on your test data
    response = test_client.get(f'/api/users/{user_id}')
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['user_id'] == user_id


# Test api_add_user()
def test_api_add_user(test_client):
    user = {"name": "Bob Green", "email": "bob@example.com", "phone": "4444444444", "address": "1010 Maple St", "country": "USA"}

    response = test_client.post('/api/users/add', data=json.dumps(user), content_type='application/json')
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['name'] == user['name']


# Test api_update_user()
def test_api_update_user(test_client):
    user = {"user_id": 1, "name": "John Updated Again", "email": "john.updated.again@example.com", "phone": "1231231234", "address": "123 Main St", "country": "USA"}

    response = test_client.put('/api/users/update', data=json.dumps(user), content_type='application/json')
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['name'] == user['name']


# Test api_delete_user()
def test_api_delete_user(test_client):
    user_id = 1  # Adjust based on your test data
    response = test_client.delete(f'/api/users/delete/{user_id}')
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['status'] == "User deleted successfully"

