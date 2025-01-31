# Development 

## Running the Application

> Suggestion is to use git bash for all terminal commands

To run the application
- `docker compose up`

To run the application (if there has been a change in the build process of docker)
- `docker compose up --build`

## Connecting to a container

To connect to a container (backend-web-1 | backend-db-1)
- `docker -it exec (container-name) bash`

## Log into MariaDB

To login to MariaDB (after connecting to the container, database is `local_device_database`)
- `mariadb -h 0.0.0.0 -u root -prootpassword`

## Sending HTTP Traffic

Use `cURL` to send HTTP messages
- `curl -X [GET | DELETE] http://127.0.0.1:5000/.../`
- `curl -X [POST | PUT] http://127.0.0.1:5000/.../ -H "Content-Type: application/json" -d '{"key": value}'`

Syntax is
- `curl -X (verb) (url) (-H "headerKey: headerValue") (-d 'data')`

## Reset the database

There is an endpoint under `/dev` that deletes and re-inserts all data from the database, resetting it to a consistent initial state.

## Pytest

To run pytest (make sure the app is running with no errors)
- `pytest`

To see any print statements make sure to use
- `pytest -s`

## Printing from Flask

To use print statements in Flask make sure to use
- `print(..., flush=True)`

## Troubleshooting

### Database Issues

If there are any database issues, especially connected with migrations:
- Delete the migrations folder
- Either using docker or the docker extension
  - Delete the backend container under Containers
  - Delete the backend_db_data volume under Volumes
- Run `docker compose up`