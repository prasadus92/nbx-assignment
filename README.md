# NBX Backend Recruitment Assignment

Welcome to the NBX developer assignment! The goal of this project to get an idea of your coding style. Enjoy!

## Requirements

This is a User Service API. It's purpose is to manage user resources. It should provide JSON endpoints to do this.

### Endpoints

- health: `GET /` - this is just an endpoint that returns the service name. You can hit this once you bring up the service to make sure it's working.
- list users: `GET /users` - return the list of users
  - Response Body:

    ```json
    [{
        "id": "uuid",
        "name": "string",
        "email": "string"
    }]
    ```

- create user: `POST /users` - create a user with the given request payload
  - Request Body:

    ```json
    {
        "name": "string",
        "email": "string"
    }
    ```

  - Response Body:

    ```json
    {
        "id": "uuid",
        "name": "string",
        "email": "string"
    }
    ```

- get user by id: `GET /users/{user_id}` - return the user with the ID from the url, or 404 if not found
  - Response Body:

    ```json
    {
        "id": "uuid",
        "name": "string",
        "email": "string"
    }
    ```

- update a user: `PUT /users/{user_id}` - update the user with the provided ID with the request payload, or 404 if not found
  - Request Body:

    ```json
    {
        "id": "uuid",
        "name": "string",
        "email": "string"
    }
    ```

  - Response Body:

    ```json
    {
        "id": "uuid",
        "name": "string",
        "email": "string"
    }
    ```

- delete a user: `DELETE /users/{user_id}` - delete the user with the given ID
  - Response: 204 No Content

## Possible Extras

- input validation
- unit tests (if you do this, add a section to this README with details on how to run them)
- functional tests (if you do this, add a section to this README with details on how to run them)
- use a database to store user resources
- restructure files to be more maintainable
- UI
- Error handling

## Prerequisites

- Docker: https://docs.docker.com/install/

## How to run the project

### Build

From within the project, run `docker-compose build app`

### Run

From within the project, run `docker-compose up -d`

This will also run the PostgreSQL as the application database.

**NOTE**: 

1. Application configuration is supplied via `userservice.yaml` file located under `config`. This is currently organized into environment specific files like `userservice-docker.yaml` (for Docker).
2. If you are running the application from an IDE, run the DB initialization script `init-db.py` before starting the application (also, you could use `run-application.sh`).

### Verify the service is up and running

Running `curl http://localhost:8080` should return `{"name": "user-service"}`

### Apply Changes

After you've made changes, run the above two commands again

### View logs

From within the project, run `docker-compose logs -f app`

### Access API Documentation

The API documentation is provided via Swagger and is accessible at - http://localhost:8080/api/doc
