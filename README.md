# COMP3122 Project Group 2
Restaurant booking service: Eat Everywhere

## Prerequisites

- Python v3.5
- Docker Compose v1.25 (or Kubernetes v1.17)

## Start

- `docker-compose up`

## View

- Go to `http://localhost:5000/` to watch events and browse state.

## Test

- `python3 -m unittest tests/unit.py`

## View

- Go to `http://localhost:8001/` to see what's in Redis (use `redis:6379`)

## Stop

- `docker-compose down`
