# This script implements a RESTful API using Flask and SQLAlchemy
# to manage a network device inventory. It provides endpoints to
# list, retrieve, create, and update network devices stored in a
# SQLite database.

from flask import Flask, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///network.db'

# Create the SQLAlchemy object, bound to the Flask app
db = SQLAlchemy(app)

# Custom exception for validation errors
class ValidationError(ValueError):
    pass

# Define the Device model, representing the 'devices' table in the database
class Device(db.Model):
    __tablename__ = 'devices'

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    hostname = db.Column(db.String(64), unique=True)  # Unique hostname
    loopback = db.Column(db.String(120), unique=True)  # Unique loopback IP
    mgmt_ip = db.Column(db.String(120), unique=True)  # Unique management IP
    role = db.Column(db.String(64))  # Device role
    vendor = db.Column(db.String(64))  # Vendor name
    os = db.Column(db.String(64))  # Operating system

    # URL to access this device's resource
    def get_url(self):
        return url_for('get_device', id=self.id, _external=True)

    # Serialize the device data as a dictionary
    def export_data(self):
        return {
            'self_url': self.get_url(),
            'hostname': self.hostname,
            'loopback': self.loopback,
            'mgmt_ip': self.mgmt_ip,
            'role': self.role,
            'vendor': self.vendor,
            'os': self.os
        }

    # Import data from a dictionary into this device object
    def import_data(self, data):
        try:
            self.hostname = data['hostname']
            self.loopback = data['loopback']
            self.mgmt_ip = data['mgmt_ip']
            self.role = data['role']
            self.vendor = data['vendor']
            self.os = data['os']
        except KeyError as e:
            raise ValidationError('Invalid device: missing ' + e.args[0])
        return self

# Route to get a list of all devices (only their URLs)
@app.route('/devices/', methods=['GET'])
def get_devices():
    return jsonify({'device': [device.get_url() 
                               for device in Device.query.all()]})

# Route to get the details of a specific device by ID
@app.route('/devices/<int:id>', methods=['GET'])
def get_device(id):
    return jsonify(Device.query.get_or_404(id).export_data())

# Route to create a new device record from JSON request body
@app.route('/devices/', methods=['POST'])
def new_device():
    device = Device()
    device.import_data(request.json)
    db.session.add(device)
    db.session.commit()
    return jsonify({}), 201, {'Location': device.get_url()}

# Route to update an existing device by ID using JSON data
@app.route('/devices/<int:id>', methods=['PUT'])
def edit_device(id):
    device = Device.query.get_or_404(id)
    device.import_data(request.json)
    db.session.add(device)
    db.session.commit()
    return jsonify({})

# Run the application and create tables if necessary
if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(host='0.0.0.0', debug=True)  # Start the development server
