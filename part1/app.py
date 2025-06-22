# Import the Flask class from the flask module
from flask import Flask

# Create an instance of the Flask application
# __name__ is a special variable in Python. It gets the name of the current module.
app = Flask(__name__)

# Define a route for the root URL ('/') of the web app
@app.route('/')
def hello_networkers():
    # This function runs when someone visits the root URL
    return 'Hello Networkers!'  # This is the text shown in the browser

# This checks if this script is run directly (not imported)
if __name__ == '__main__':
    # Run the Flask web app
    # host='0.0.0.0' makes the app accessible from any network interface
    # debug=True gives helpful error messages and auto-reloads the app when code changes
    app.run(host='0.0.0.0', debug=True)