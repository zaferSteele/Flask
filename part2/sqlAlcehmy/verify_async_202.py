# This script verifies that the Flask API returns HTTP 202 Accepted 
# while the asynchronous task (fetching OS version) is still processing.
# It sends a request to start the background task, then polls the status endpoint.
# The expected behavior is:
#   - Initial GET to /devices/1/version triggers the task.
#   - API responds with 202 and a 'Location' header.
#   - Follow-up requests to the task URL should return 202 until the task completes.
#   - Later (after some wait), a final request may return 303 See Other.


import requests
import time

# Base server URL
server = 'http://192.168.255.3:5000'
# Endpoint to trigger OS version retrieval for device with ID 1
endpoint = '/devices/1/version'

# 1. Initiate background task
r = requests.get(server + endpoint)
# Location header contains the URL to track background task status
resource = r.headers['location']
print("Status: {} Resource: {}".format(r.status_code, resource))

# 2. Immediately poll the task status
r = requests.get(server + "/" + resource)
print("Immediate Status Query to Resource: " + str(r.status_code))

# 3. Wait before checking again
print("Sleep for 2 seconds")
time.sleep(2)

# 4. Re-poll to check if the task has completed
r = requests.get(server + "/" + resource)
print("Status after 2 seconds: " + str(r.status_code))
