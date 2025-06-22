# Import Flask class and url_for function from the flask module
from flask import Flask, url_for

# Create a Flask app instance
app = Flask(__name__)

# Define a dynamic route that accepts a hostname from the URL
# Example: visiting /r1/list_interfaces
@app.route('/<hostname>/list_interfaces')
def device(hostname):
    # Check if the provided hostname is in the list of known routers
    if hostname in routers:
        # Return a message confirming the hostname is valid
        return 'Listing interfaces for %s' % hostname
    else:
        # Return a message for invalid hostnames
        return 'Invalid hostname'

# Define a list of valid router hostnames
routers = ['r1', 'r2', 'r3']

# Loop through each router and generate a test URL for it
# app.test_request_context() sets up a fake request environment
for router in routers:
    with app.test_request_context():
        # url_for builds the URL for the 'device' route using the router name
        print(url_for('device', hostname=router))

# Run the Flask app only if this script is executed directly
if __name__ == '__main__':
    # Start the development server
    # host='0.0.0.0' allows access from any device on the network
    # debug=True enables auto-reload and better error messages
    app.run(host='0.0.0.0', debug=True)