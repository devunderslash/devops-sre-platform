# Sample Backend REST API (Team Attendance Tracker)

This is a sample backend REST API for a team attendance tracker. It is built using Flask. This is to display the Dev elements of a DevOps project. It incorporates up to date practices with the use of SOLID principles, DRY code, and a clean codebase. It also includes tests for the main functionality of the API and instructions as to how to both run the application and the tests simply and easily.

Here is a syetem diagram of the project:

TODO - Add system diagram

## Pre-Requisites
- Python 3.6 or higher

## Installation

1. Clone the repository
2. Create a virtual environment in the backend directory:
```bash
cd backend
python -m venv venv
```
3. Activate the virtual environment:
```bash
source venv/bin/activate
```
4. Install the dependencies:
```bash
pip install -r requirements.txt
```
5. Create DB tables:
```bash
flask db init
flask db migrate
flask db upgrade
```

6. Run the application:
```bash
flask run
```
7. The application should be running on http://127.0.0.1:5000/
8. Stop the application by pressing `Ctrl+C` and deactivate the virtual environment by running:
```bash
deactivate
```

## Running Tests

To run the tests, run the following command:
```bash
coverage run -m pytest -v
```

To see the test coverage, run:
```bash
coverage report
```

To see the test coverage in HTML, run:
```bash
coverage html
```
Then open the `htmlcov/index.html` file in a browser.


## API Endpoints

### GET /api/players

Get all players
Sample curl request:
```bash
curl -X GET http://127.0.0.1:5000/api/players
```

### POST /api/players

Create a new player
Sample curl request:
```bash
curl -X POST http://127.0.0.1:5000/api/players \
-H "Content-Type: application/json" \
-d '{
  "id": 1,
  "name": "John Doe",
  "dob": "2010-05-15",
  "age": 0, 
  "joined_group_date": "2023-01-01",
}'
# Age is calculated automatically based on the date of birth
```

### GET /api/players/<int:player_id>

Get a player by ID
Sample curl request:
```bash
curl -X GET http://127.0.0.1:5000/api/players/1
```

### PUT /api/players/<int:player_id>