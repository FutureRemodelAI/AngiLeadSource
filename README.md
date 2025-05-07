# AngiLeadSource
# Flask Lead API

A Flask application to manage and process leads. The API integrates with Angi and stores lead data in a PostgreSQL database.

## Features
- Webhook to receive and store lead data
- Integrates with Angi for fetching lead information
- PostgreSQL as the database
- Dockerized for easy development and deployment

## Prerequisites

Ensure that the following software is installed:

- Docker & Docker Compose
- Python 3.11 or higher (if not using Docker)
- PostgreSQL (if not using Docker)

## Installation

### without Docker 

1. Clone the repository:
   ```bash
   git clone https://github.com/FutureRemodelAI/AngiLeadSource.git
   cd flask-lead-api

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
   
3. Set up your PostgreSQL database, and update the DATABASE_URI in config.py with your connection details.

4. Initialize the database (if not already set up):
    ```bash 
    flask db init
    flask db migrate
    flask db upgrade
    ```
5. Run the Flask app:
```bash
python app.py
```
6. run test cases
```bash
make test
```

6. The application will be available at http://127.0.0.1:5000.


### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/FutureRemodelAI/AngiLeadSource.git
   cd flask-lead-api

2. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```

This will:

Build the Flask application container (flask-lead-api)

Set up the PostgreSQL database container (postgres-db)

3. The application will be available at http://127.0.0.1:5000.

4. To stop the containers, press CTRL+C or run:
   ```bash
   docker-compose down 
   ```