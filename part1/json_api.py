# Import Flask and the jsonify function from the flask module
from flask import Flask, jsonify

# Create a new Flask application instance
app = Flask(__name__)

# Define a dynamic route that takes two values from the URL:
# - hostname (string), e.g., 'R1'
# - interface_number (integer), e.g., 2
# Example: /routers/R1/interface/2
@app.route('/routers/<hostname>/interface/<int:interface_number>')
def interface(hostname, interface_number):
    # Return a JSON response with the hostname and interface number
    # jsonify converts the Python dictionary to a valid JSON response
    return jsonify(name=hostname, interface=interface_number)

# Run the app only when the script is executed directly
if __name__ == '__main__':
    # Start the development server
    # host='0.0.0.0' allows access from other machines on the network
    # debug=True enables auto-reloading and useful error messages
    app.run(host='0.0.0.0', debug=True)