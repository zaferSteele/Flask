# This script initializes a Flask application with SQLAlchemy,
# defines a Device model for network devices, creates a SQLite database,
# and seeds it with a few sample device records.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///network.db'
# Disable tracking modifications to save system resources
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy object, bound to the Flask app
db = SQLAlchemy(app)

# Define the Device model, representing the 'devices' table in the database
class Device(db.Model):
    __tablename__ = 'devices'  # Table name explicitly defined

    # Table columns
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    hostname = db.Column(db.String(120), index=True)  # Hostname with index for fast lookup
    vendor = db.Column(db.String(40))  # Vendor name column

    # Constructor to initialize a Device object
    def __init__(self, hostname, vendor):
        self.hostname = hostname
        self.vendor = vendor

    # String representation for debugging/logging
    def __repr__(self):
        return '<Device %r>' % self.hostname

# Run this block only when the script is executed directly
if __name__ == '__main__':
    # Create the database tables based on model definitions
    db.create_all()

    # Create device entries
    r1 = Device('lax-dc1-core1', 'Juniper')
    r2 = Device('sfo-dc1-core1', 'Cisco')
    r3 = Device('lax-dc1-core2', 'Juniper')

    # Add devices to the session (staging area before commit)
    db.session.add(r1)
    db.session.add(r2)
    db.session.add(r3)

    # Commit the session to write data to the database
    db.session.commit()

    # Query and fetch the first device matching a specific hostname
    Device.query.filter_by(hostname='lax-dc1-core2').first()
