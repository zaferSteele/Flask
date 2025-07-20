<h1 align="center"> Zafer Steele's Flask for Network Automation </h1>

<p align="center">
<img src="assets/flask-network-icon.png" alt="Network Security Toolkit" width="100">
</p>

**Flask for Network Automation** is a collection of simple Flask-based web tools created by and for network engineers. The goal is to streamline and automate networking tasks using REST APIs and web interfaces. *(Project still in progress.)*

---

## Features

### Part 1: Basic Flask Routing

* `app.py`: Minimal Flask server returning "Hello Networkers!" on root URL.
* `dynamic_routes.py`, `routes_demo.py`, `json_api.py`, `generate_routes.py`: Demonstrations of various routing and response techniques using Flask.

### Part 2: REST API with SQLAlchemy

* Implements a network device inventory system.
* Endpoints to create, read, update, and list devices.
* Uses SQLite for backend storage and SQLAlchemy ORM for database interactions.

## Installation

```bash
# Clone the repository
$ git clone https://github.com/zaferSteele/Flask.git
$ cd Flask

# Create a virtual environment (optional but recommended)
$ python3 -m venv venv
$ source venv/bin/activate

# Install dependencies
$ pip install -r requirements.txt
```

## Requirements

See `requirements.txt`. Key dependencies:

* Flask
* Flask-SQLAlchemy
* requests
* httpie (for command-line HTTP testing)

---

## 👤 Author

**Zafer Steele**
GitHub: [@zaferSteele](https://github.com/zaferSteele)

---

## 📝 License

This repository is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---
