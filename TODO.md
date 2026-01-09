# Late Show API Project - TODO List

## Project Setup
- [x] Create requirements.txt with dependencies
- [x] Create config.py for Flask configuration
- [x] Create models.py with Episode, Guest, Appearance models
- [x] Create app.py with Flask routes
- [x] Create seed.py for database seeding
- [x] Create README.md with project documentation

## Database Setup
- [x] Create migrations folder and configuration
- [x] Run initial migration
- [x] Seed database with sample data

## Route Implementation
- [x] Implement GET /episodes
- [x] Implement GET /episodes/:id
- [x] Implement GET /guests
- [x] Implement POST /appearances

## Validation & Testing
- [x] Add Appearance validation (rating 1-5)
- [x] Test all endpoints using Postman
- [x] Verify error handling

## Documentation
- [x] Write comprehensive README
- [x] Add docstrings to all functions
- [x] Verify markdown renders correctly

## Test Results
All endpoints tested successfully:
- GET /episodes: 200 OK ✓
- GET /episodes/1: 200 OK ✓
- GET /episodes/9999: 404 Not Found ✓
- GET /guests: 200 OK ✓
- POST /appearances: 201 Created ✓
- POST /appearances (invalid rating): 400 Bad Request ✓
- POST /appearances (missing fields): 400 Bad Request ✓
