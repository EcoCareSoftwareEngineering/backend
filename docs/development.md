# Development 

## Running

To run the appliation, in the terminal type:
- `docker compose up`
- If the docker configuration has changed you will need to run `docker compose up --build` to force a rebuild

## Troubleshooting

### Database Issues

If there are any database issues, especially connected with migrations:
- Delete the migrations folder
- Either using docker or the docker extension
  - Delete the backend container under Containers
  - Delete the backend_db_data volume under Volumes
- Run `docker compose up`

If there are still issues message John. 