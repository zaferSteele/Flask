# Import the Flask class from the flask module
from flask import Flask

# Create a new instance of the Flask application
app = Flask(__name__)

# Define a dynamic route that captures a hostname from the URL
# Example: visiting /routers/R1 will pass "R1" to the function
@app.route('/routers/<hostname>')
def router(hostname):
    # This function displays the hostname in the response
    return 'You are at %s' % hostname

# Define another dynamic route with two parameters:
# - hostname: a string
# - interface_number: an integer
# Example: visiting /routers/R1/interface/2 passes "R1" and 2
@app.route('/routers/<hostname>/interface/<int:interface_number>')
def interface(hostname, interface_number):
    # This function shows both the hostname and interface number
    return 'You are at %s interface %d' % (hostname, interface_number)

# Run the app only if this script is executed directly
if __name__ == '__main__':
    # Start the Flask server
    # host='0.0.0.0' allows external access
    # debug=True enables auto-reload and useful error messages
    app.run(host='0.0.0.0', debug=True)