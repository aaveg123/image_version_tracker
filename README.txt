
===============================
 Image Version Tracker (Flask)
===============================

Track and log Docker image metadata (such as image ID, tag, and commit hash) using Flask, Docker SDK, and PostgreSQL.

-----------------------
📦 Project Description
-----------------------

This tool helps developers and DevOps teams log and view Docker image versions used in deployments. It pulls metadata from Docker Hub or private registries and stores it in a PostgreSQL database via a Flask-based REST API.

-----------------------
🛠️ Technologies Used
-----------------------

- Python 3
- Flask (API framework)
- Docker SDK for Python
- PostgreSQL (data storage)
- psycopg2 (PostgreSQL adapter)

## 🚀 Features

- Pulls Docker image metadata automatically
- Stores metadata in PostgreSQL
- REST API endpoints to log and retrieve image versions
- Simple and extensible Python implementation

-----------------------
📁 Project Structure
-----------------------

image_version_tracker/
├── image_version_tracker.py   # Main application
├── requirements.txt           # Python dependencies
└── README.txt                 # Project instructions (this file)

-----------------------
🚀 Setup Instructions
-----------------------

1. Clone or download this repository.

2. Set up a Python virtual environment:
   $ python3 -m venv venv
   $ source venv/bin/activate

3. Install dependencies:
   $ pip install -r requirements.txt

4. Ensure Docker is installed and running.

5. Set up PostgreSQL:
   - Create the database and user:
     $ psql -U postgres
     postgres=# CREATE DATABASE image_tracker;
     postgres=# CREATE USER image_user WITH ENCRYPTED PASSWORD 'password';
     postgres=# GRANT ALL PRIVILEGES ON DATABASE image_tracker TO image_user;
     postgres=# \q

6. Run the Flask app:
   $ python3 image_version_tracker.py

7. Test logging an image:
   $ curl -X POST http://127.0.0.1:5000/log-image \
        -H "Content-Type: application/json" \
        -d '{"image_name": "ubuntu:latest", "storage": "postgresql"}'

8. View logged images:
   $ curl http://127.0.0.1:5000/get-images

-----------------------
📋 API Endpoints
-----------------------

POST /log-image
  - Description: Pulls a Docker image and logs metadata.
  - Body:
    {
      "image_name": "ubuntu:latest",
      "storage": "postgresql"
    }

GET /get-images
  - Description: Returns all logged image metadata.

-----------------------
🧪 Example Response
-----------------------

POST /log-image

Response:
{
  "message": "Image version data logged successfully.",
  "version": "sha256:abc123...",
  "tag": "latest"
}

GET /get-images

Response:
[
  {
    "image_name": "ubuntu",
    "tag": "latest",
    "version": "sha256:abc123...",
    "commit_hash": "unknown",
    "timestamp": "2025-04-11T14:00:23.123456"
  }
]

-----------------------
📌 Notes
-----------------------

- This is a development server. Do not use it in production without a proper WSGI server (e.g., Gunicorn).
- Timestamp handling is in UTC.
- Only PostgreSQL is supported for now (JSON storage disabled).

-----------------------
🧑‍💻 Author
-----------------------

Developed by: [Aaveg Kumar]
GitHub: @aaveg123
