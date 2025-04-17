# Leaderboard API

This project is a Model-View-Controller (MVC) API for managing a leaderboard. It is built using FastAPI and SQLModel, providing endpoints to create, update, and retrieve leaderboard scores.

## Features

- **Create Score**: Add a new score entry to the leaderboard.
- **Update Score**: Update the points for an existing score entry.
- **Retrieve Top Scores**: Fetch the top scores from the leaderboard with pagination support.

## Project Structure

- `score.py`: Defines the data models for the leaderboard, including `Score`, `ScoreBase`, `ScoreCreate`, and `ScorePublic`.
- `database.py`: Manages the database connection and session, and initializes the database schema.
- `main.py`: Implements the FastAPI application and defines the API endpoints.

## Endpoints

### 1. Create Score
- **URL**: `/score`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "name": "string",
    "points": 0
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "name": "string",
    "points": 0
  }
  ```

### 2. Update Score
- **URL**: `/scores`
- **Method**: `PUT`
- **Query Parameters**:
  - `user_id`: ID of the user whose score is to be updated.
  - `points`: Points to add to the user's score.
- **Response**:
  ```json
  {
    "id": 1,
    "name": "string",
    "points": 10
  }
  ```

### 3. Get Top Scores
- **URL**: `/scores`
- **Method**: `GET`
- **Query Parameters**:
  - `offset`: Number of records to skip (default: 0).
  - `limit`: Maximum number of records to return (default: 10, max: 10).
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "string",
      "points": 10
    }
  ]
  ```

## Setup

### Prerequisites
- Python 3.12 or higher

### Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

### Accessing the API
The API will be available at `http://127.0.0.1:8000`. You can explore the API documentation at `http://127.0.0.1:8000/docs`.

## License
This project is licensed under the MIT License.