# Import the Flask class from the flask module
from flask import Flask

# Create a Flask web application instance
app = Flask(__name__)

# Define a route for the root URL ('/')
@app.route('/')
def index():
    # This function runs when someone visits the root URL
    return 'You are at index()'  # This message is shown in the browser

# Define a second route at '/routers/'
@app.route('/routers/')
def routers():
    # This function runs when someone visits '/routers/'
    return 'You are at routers()'  # This message is shown in the browser

# Run the app only if this script is executed directly
if __name__ == '__main__':
    # Start the Flask development server
    # host='0.0.0.0' makes it accessible from any network interface
    # debug=True enables auto-reload and detailed error pages
    app.run(host='0.0.0.0', debug=True)