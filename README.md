# Late Show API

A Flask-based REST API for managing episodes, guests, and their appearances on a late-night talk show.

## Project Overview

This API allows you to manage a database of late show episodes, guests, and their appearances. It provides endpoints to retrieve episodes and guests, as well as create new appearance records linking guests to specific episodes.

## Features

- View all episodes and guests
- View detailed information about a specific episode including all guest appearances
- Create new guest appearances with ratings
- Delete episodes (with cascade delete for appearances)
- Data validation to ensure rating integrity
- Proper error handling with appropriate HTTP status codes

## Technology Stack

- **Python 3.8+**
- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM for database operations
- **Flask-Migrate** - Database migrations
- **SQLite** - Database (development)

## Data Model

The application uses three main models:

### Episode
- id: Primary key
- date: Episode air date
- number: Episode number

### Guest
- id: Primary key
- name: Guest name
- occupation: Guest occupation

### Appearance
- id: Primary key
- rating: Rating between 1-5 (inclusive)
- episode_id: Foreign key to Episode
- guest_id: Foreign key to Guest

### Relationships
- An Episode has many Guests through Appearances
- A Guest has many Episodes through Appearances
- An Appearance belongs to both an Episode and a Guest
- Cascade deletes are configured on Appearance model

## Installation

1. Clone the repository:
bash:
git clone: https://github.com/CODER-41/lateshow-ronny-mboya.git
cd lateshow-ronny-mboya


2. Navigate to the server directory:
bash:
cd server


3. Create a virtual environment:
bash:
pip install pipenv 


4. Install dependencies and create virtual environment:
bash:
pipenv install

5. Activate the virtual environment:
bash:
pipenv shell


6. Set up the database:
bash:
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python seed.py


7. Run the application:
bash:
python app.py


The API will be available at `http://localhost:5555`

## API Endpoints

### GET /episodes
Retrieves all episodes.

**Response (200 OK):**
json
[
  {
    "id": 1,
    "date": "1/11/99",
    "number": 1
  },
  {
    "id": 2,
    "date": "1/12/99",
    "number": 2
  }
]


### GET /episodes/:id
Retrieves a specific episode with all appearances and guest details.

**Response (200 OK):**
json
{
  "id": 1,
  "date": "1/11/99",
  "number": 1,
  "appearances": [
    {
      "id": 1,
      "rating": 4,
      "episode_id": 1,
      "guest_id": 1,
      "guest": {
        "id": 1,
        "name": "Michael J. Fox",
        "occupation": "actor"
      }
    }
  ]
}

**Response (404 Not Found):**
json
{
  "error": "Episode not found"
}


### DELETE /episodes/:id
Deletes a specific episode and all associated appearances.

**Response (204 No Content):**
Empty response body

**Response (404 Not Found):**
json
{
  "error": "Episode not found"
}

**Note:** Due to cascade delete, all appearances associated with this episode will also be deleted.

### GET /guests
Retrieves all guests.

**Response (200 OK):**
json
[
  {
    "id": 1,
    "name": "Michael J. Fox",
    "occupation": "actor"
  },
  {
    "id": 2,
    "name": "Sandra Bernhard",
    "occupation": "Comedian"
  }
]


### POST /appearances
Creates a new appearance linking a guest to an episode.

**Request Body:**
json
{
  "rating": 5,
  "episode_id": 100,
  "guest_id": 123
}


**Response (201 Created):**
json
{
  "id": 162,
  "rating": 5,
  "guest_id": 123,
  "episode_id": 100,
  "episode": {
    "id": 100,
    "date": "1/12/99",
    "number": 2
  },
  "guest": {
    "id": 123,
    "name": "Tracey Ullman",
    "occupation": "television actress"
  }
}

**Response (400 Bad Request):**
json
{
  "errors": ["validation errors"]
}


## Testing

This project includes a Postman collection for testing all endpoints.

### Using Postman:

1. Open Postman
2. Click **Import**
3. Select `challenge-4-lateshow.postman_collection.json` from the project root
4. Run the requests to verify all endpoints work correctly

### Available Test Requests:
-  GET /episodes - Retrieve all episodes
-  GET /episodes/:id - Retrieve specific episode
-  DELETE /episodes/:id - Delete episode
-  GET /guests - Retrieve all guests
-  POST /appearances - Create new appearance

### Manual Testing with curl:

bash:
# Get all episodes
curl http://localhost:5555/episodes

# Get specific episode
curl http://localhost:5555/episodes/1

# Get all guests
curl http://localhost:5555/guests

# Create appearance
curl -X POST http://localhost:5555/appearances \
  -H "Content-Type: application/json" \
  -d '{"rating": 5, "episode_id": 2, "guest_id": 3}'

# Delete episode
curl -X DELETE http://localhost:5555/episodes/1


## Validation Rules

- **Appearance rating**: Must be between 1 and 5 (inclusive)
- All validations return appropriate error messages and HTTP status codes

## Error Handling

The API uses standard HTTP status codes:
- 200 OK - Successful GET request
- 201 Created - Successful POST request
- 204 No Content - Successful DELETE request
- 400 Bad Request - Validation errors
- 404 Not Found - Resource not found

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is part of a coding challenge and is for educational purposes.

## Author

[Ronny Mboya]

## Acknowledgments

- Flask documentation
- SQLAlchemy documentation
- Challenge provided by [Moringa School]