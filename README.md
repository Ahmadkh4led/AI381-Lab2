
# AI381 Lab 2 – Bring Your Own Model

![AI381 Lab 2 CI](https://github.com/Ahmadkh4led/AI381-Lab2/actions/workflows/main.yml/badge.svg)

## Project Description

This project serves a machine learning model through a FastAPI REST API. The application is containerized with Docker and tested automatically using GitHub Actions.

## Features

- FastAPI REST API
- Machine learning prediction endpoint
- Input validation
- Automated tests using pytest
- Multi-stage Docker build
- Non-root runtime user
- Docker health check
- GitHub Actions CI pipeline
- Trivy vulnerability scanning
- Docker image publishing to GitHub Container Registry (GHCR)

## Requirements

- Docker installed on your machine

## Run the Service

Build the Docker image and start the API with this single command:

```bash
docker build -t ai381-lab2 . && docker run --rm -p 8000:8000 ai381-lab2
```

## API Endpoints

### Health Check

**GET** `/health`

Example:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

### Make a Prediction

**POST** `/predict`

Example:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"tenure_months":72,"monthly_fee":45.0,"contract":"two-year","internet_service":"dsl","support_calls":1}'
```

Example response:

```json
{"churn_probability":0.008}
```

## Testing

Run the tests locally:

```bash
PYTHONPATH=. python -m pytest -v
```

Run linting:

```bash
ruff check src tests
```

## Continuous Integration

GitHub Actions runs linting and tests on pull requests and pushes to the `main` branch.

On pushes to `main`, the workflow also builds the Docker image, scans it with Trivy, and publishes it to GHCR using the commit SHA as the image tag.

## Container Registry

GitHub Container Registry: `ghcr.io/ahmadkh4led/ai381-lab2`

## Repository

https://github.com/Ahmadkh4led/AI381-Lab2
