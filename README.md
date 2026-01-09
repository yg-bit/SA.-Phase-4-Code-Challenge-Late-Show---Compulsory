# Late Show API

A Flask REST API for managing late show episodes, guests, and appearances.

## Overview

This API provides endpoints to manage a late show television program, tracking episodes, guest appearances, and ratings. It's built with Flask and SQLAlchemy, featuring proper model relationships, validations, and JSON API responses.

## Features

- **Episode Management**: Track episodes with dates and episode numbers
- **Guest Management**: Maintain guest information (name, occupation)
- **Appearance Tracking**: Record guest appearances on episodes with ratings
- **Data Validation**: Ensure data integrity with rating constraints (1-5)
- **Cascade Deletes**: Automatic cleanup of related appearances

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd lateshow-firstname-lastname
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database and seed with sample data:
```bash
python seed.py
```

5. Run the application:
```bash
python app.py
```

The server will start at `http://localhost:5000`

## API Endpoints

### GET /episodes

Returns a list of all episodes.

**Response:**
```json
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
```

### GET /episodes/:id

Returns a single episode with its appearances.

**Response (Success):**
```json
{
  "id": 1,
  "date": "1/11/99",
  "number": 1,
  "appearances": [
    {
      "episode_id": 1,
      "guest": {
        "id": 1,
        "name": "Michael J. Fox",
        "occupation": "actor"
      },
      "guest_id": 1,
      "id": 1,
      "rating": 4
    }
  ]
}
```

**Response (Not Found):**
```json
{
  "error": "Episode not found"
}
```
**Status Code:** 404

### GET /guests

Returns a list of all guests.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Michael J. Fox",
    "occupation": "actor"
  },
  {
    "id": 2,
    "name": "Sandra Bernhard",
    "occupation": "comedian"
  }
]
```

### POST /appearances

Creates a new appearance record.

**Request Body:**
```json
{
  "rating": 5,
  "episode_id": 100,
  "guest_id": 123
}
```

**Response (Success):**
```json
{
  "id": 162,
  "rating": 5,
  "guest_id": 3,
  "episode_id": 2,
  "episode": {
    "date": "1/12/99",
    "id": 2,
    "number": 2
  },
  "guest": {
    "id": 3,
    "name": "Tracey Ullman",
    "occupation": "television actress"
  }
}
```
**Status Code:** 201

**Response (Validation Error):**
```json
{
  "errors": ["validation errors"]
}
```
**Status Code:** 400

## Data Models

### Episode
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| date | String | Episode air date |
| number | Integer | Episode number |

### Guest
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String | Guest's name |
| occupation | String | Guest's occupation |

### Appearance
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| rating | Integer | Rating (1-5) |
| episode_id | Integer | Foreign key to Episode |
| guest_id | Integer | Foreign key to Guest |

## Validations

- **Appearance.rating**: Must be between 1 and 5 (inclusive)
- All foreign key relationships are validated on creation

## Relationships

- An **Episode** has many **Appearances**
- A **Guest** has many **Appearances**
- An **Appearance** belongs to an **Episode** and a **Guest**
- Cascade deletes are configured: deleting an episode or guest removes associated appearances

## Testing with Postman

1. Import the Postman collection (`challenge-4-lateshow.postman_collection.json`)
2. Use the collection to test all endpoints
3. Verify responses match the expected format

## Project Structure

```
lateshow/
├── app.py           # Flask application and routes
├── config.py        # Flask configuration
├── models.py        # SQLAlchemy models
├── seed.py          # Database seeding script
├── requirements.txt # Python dependencies
├── README.md        # This file
├── episodes.csv     # Sample episode data
├── guests.csv       # Sample guest data
└── appearances.csv  # Sample appearance data
```

## Technologies Used

- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **Flask-SQLAlchemy**: Flask integration for SQLAlchemy
- **Flask-Migrate**: Database migrations
- **SQLite**: Database (configurable to PostgreSQL)

## License

This project is part of Phase 4 Code Challenge requirements.

