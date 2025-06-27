# Import the database instance and User model from async_device_api_with_auth.py
from async_device_api_with_auth import db, User

# Create the necessary database tables if they don't exist yet
db.create_all()

# Create a new user object with the username 'zafer'
u = User(username='zafer')

# Set the user's password using a secure hashing function
# This ensures the password is not stored in plain text
u.set_password('secret')

# Add the new user to the current database session (staging it for commit)
db.session.add(u)

# Commit the session to save the new user permanently in the database
db.session.commit()
