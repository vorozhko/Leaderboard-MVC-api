# Leaderboard - solving Top K Problem with Python

This project is a solution to the Leaderboard task from System Design Interview book. It is built using **FastAPI, SQLModel and Valkey**.

## Features

- **Create Score**: Add a new score entry to the leaderboard.
- **Update Score**: Update the points for an existing score entry.
- **Retrieve Top Scores**: Fetch the top scores from the leaderboard with pagination support.
- **Row Number Calculation**: Each score entry includes a dynamically calculated rank based on points.

## Project Structure

- `score_model.py`: Defines Pydantic data models for the leaderboard, including `Score` as a table, `ScoreBase` as a base SQLModel, `ScoreCreate` as a model to create new record, and `ScorePublic` as a return model for all queries.
- `score_repository.py`: Encapsulates all database-related logic for interacting with the `Score` model and Valkey database.
- `score_service.py`: Implements the business logic for managing scores, using the repository layer.
- `database.py`: Manages the database connection and session, and initializes the database schema.
- `main.py`: Implements the FastAPI application and defines the API endpoints.

## Storage Options

This project supports multiple storage backends:

- **SQLite**: The default relational database used for persistent storage. It is lightweight and easy to set up.
- **Redis (via Valkey)**: A high-performance in-memory data store used for scenarios requiring fast access and ranking operations. The `Valkey` library is used to interact with Redis for leaderboard functionality.

## Endpoints

### 1. Create Score
- **URL**: `/scores`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "name": "AwesomeGamer"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "name": "AwesomeGamer",
    "points": 0,
    "rank": 99
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
    "name": "AwesomeGamer",
    "points": 10,
    "rank": 50
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
      "name": "AwesomeGamer",
      "points": 120,
      "rank": 1
    },
    {
      "id": 4,
      "name": "GGALL",
      "points": 90,
      "rank": 2
    }
  ]
  ```

### 4. Get Score for a User with Current Rank
- **URL**: `/scores/{user_id}`
- **Method**: `GET`
- **Path Parameter**:
  - `user_id`: ID of the user whose score is to be retrieved.
- **Response**:
  ```json
  {
    "id": 7,
    "name": "TopPlayer",
    "points": 10,
    "rank": 55
  }
  ```

## Setup

### Prerequisites
- Python 3.12 or higher
- Running Valkey database on localhost with port 6379

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