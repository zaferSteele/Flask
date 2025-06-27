# This script creates a RESTful API using Flask and SQLAlchemy to manage
# network devices and retrieve their OS version over SSH. It connects to a SQLite
# database, supports CRUD operations for devices, and uses an external module called pexpect from the module called ssh_show_version to fetch
# version information from devices based on role or ID.
# added asynchronous functionality to spawn background threads for long-running SSH tasks.
# Http authentication added

#Examples:
# http --auth zafer:secret POST http://192.168.255.3:5000/devices/ 'hostname'='R6' 'loopback'='192.168.0.12' 'mgmt_ip'='192.168.255.18' 'role'='spine' 'vendor'='Cisco' 'os'='15.8'
# http --auth zafer:secret GET http://192.168.255.3:5000/devices/1/version  --> this will run in the background
# http --auth zafer:secret GET http://192.168.255.3:5000/status/90e585321ac544989fc74ffa8eb88bba --> the long number in the end should be modified with your own location header value obtained after running http --auth zafer:secret GET http://192.168.255.3:5000/devices/1/version --> this will then retrive the device version information 

from flask import Flask, url_for, jsonify, request,\
    make_response, copy_current_request_context, g
from flask_sqlalchemy import SQLAlchemy
from ssh_show_version import show_version # External module for SSH command execution
from http.client import INTERNAL_SERVER_ERROR, NOT_FOUND
import uuid
import functools
from threading import Thread
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth

# Initialize the Flask web application
app = Flask(__name__)
# Configure the app to use SQLite as the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///network.db'
# Disable modification tracking to improve performance
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize SQLAlchemy ORM with the Flask app
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

# Dictionary to track asynchronous background tasks
background_tasks = {}
# Optionally auto-dele0te task results after completion
app.config['AUTO_DELETE_BG_TASKS'] = True

# Custom error type for invalid or incomplete data input
class ValidationError(ValueError):
    pass

# Define the database model for Users
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

# Define the database model for a network device
class Device(db.Model):
    __tablename__ = 'devices'
    
    # Define fields/columns in the table
    id = db.Column(db.Integer, primary_key=True)        # Unique device ID
    hostname = db.Column(db.String(64), unique=True)    # Hostname must be unique
    loopback = db.Column(db.String(120), unique=True)   # Loopback IP
    mgmt_ip = db.Column(db.String(120), unique=True)    # Management IP
    role = db.Column(db.String(64))                     # Device role (e.g. core, access)
    vendor = db.Column(db.String(64))                   # Vendor (e.g. Cisco, Juniper)
    os = db.Column(db.String(64))                       # Operating system name/version

    # Return the full API URL for a specific device
    def get_url(self):
        return url_for('get_device', id=self.id, _external=True)

    # Return device data as a dictionary
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
        
    # Populate this device object using JSON input
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

# Decorator to run route logic as an asynchronous background task
def background(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        @copy_current_request_context
        def task():
            global background_tasks
            try:
                # Save the final result of the background function
                background_tasks[id] = make_response(f(*args, **kwargs))
            except:
                # Catch errors and return 500
                background_tasks[id] = make_response(INTERNAL_SERVER_ERROR())

        global background_tasks
        id = uuid.uuid4().hex  # Unique task ID
        background_tasks[id] = Thread(target=task)
        background_tasks[id].start()

        # 202 Accepted with URL to check task status
        return jsonify({}), 202, {'Location': url_for('get_task_status', id=id)}
    return wrapped

# Auth verification logic with g to hold current user
@auth.verify_password
def verify_password(username, password):
    g.user = User.query.filter_by(username=username).first()
    if g.user is None:
        return False
    return g.user.verify_password(password)

# Protect all routes with login required
@app.before_request
@auth.login_required
def beofre_request():
    pass


# Return a custom JSON error for unauthorized requests
@auth.error_handler
def unauthorized():
    response = jsonify({'status':401, 'error': 'unauthorized', 'message': 'please authenticate'})
    response.status_code = 401
    return response

# Route to return a list of all device resource URLs
@app.route('/devices/', methods=['GET'])
def get_devices():
    return jsonify({'device': [device.get_url() 
                               for device in Device.query.all()]})

# Route to get detailed info for a specific device by ID
@app.route('/devices/<int:id>', methods=['GET'])
def get_device(id):
    return jsonify(Device.query.get_or_404(id).export_data())

# Route to get version information for a specific device by ID asynchronously 
@app.route('/devices/<int:id>/version', methods=['GET'])
@background
def get_device_version(id):
    device = Device.query.get_or_404(id)
    hostname = device.hostname
    ip = device.mgmt_ip
    prompt = hostname + "#"
    result = show_version(hostname, prompt, ip, 'admin', 'password')
    return jsonify({"version": str(result)})

# Route to get version info for all devices matching a specific role asynchronously
@app.route('/devices/<device_role>/version', methods=['GET'])
@background
def get_role_version(device_role):
    device_id_list = [device.id for device in Device.query.all() if device.role == device_role]
    result = {}
    for id in device_id_list:
        device = Device.query.get_or_404(id)    # Retrieve device or return 404
        hostname = device.hostname
        ip = device.mgmt_ip
        prompt = hostname + "#"
        device_result = show_version(hostname, prompt, ip, 'admin', 'password') # Call SSH function
        result[hostname] = str(device_result)
    return jsonify(result)

# Route to create a new device
@app.route('/devices/', methods=['POST'])
def new_device():
    device = Device()
    device.import_data(request.json)    # Load JSON data into the device
    db.session.add(device)
    db.session.commit()                 # Save device to the database
    return jsonify({}), 201, {'Location': device.get_url()}

# Route to update an existing device's data
@app.route('/devices/<int:id>', methods=['PUT'])
def edit_device(id):
    device = Device.query.get_or_404(id)
    device.import_data(request.json)    # Update with new data
    db.session.add(device)
    db.session.commit()
    return jsonify({})

# Check background task status
@app.route('/status/<id>', methods=['GET'])
def get_task_status(id):
    global background_tasks
    rv = background_tasks.get(id)
    if rv is None:
        return NOT_FOUND(None)

    if isinstance(rv, Thread):
        # Task is still running
        return jsonify({}), 202, {'Location': url_for('get_task_status', id=id)}

    # Task is finished; delete if auto-delete enabled
    if app.config['AUTO_DELETE_BG_TASKS']:
        del background_tasks[id]
    return rv

# Entry point: create the tables and start the Flask development server
if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', debug=True)
