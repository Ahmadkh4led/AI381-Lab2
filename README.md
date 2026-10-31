# AI381 Lab 2 – Bring Your Own Model

![AI381 Lab 2 CI](https://github.com/Ahmadkh4led/AI381-Lab2/actions/workflows/main.yml/badge.svg)

## Project Description

This project serves a machine learning model through a FastAPI REST API. The application is containerized with Docker and tested automatically using GitHub Actions.

## Features

- FastAPI REST API
- Machine learning prediction endpoint
- Input validation using Pydantic
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

The API will be available at:

`http://localhost:8000`

## API Endpoints

### Health Check

**GET** `/health`

Check whether the API is running:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

### Make a Prediction

**POST** `/predict`

Send customer information to get the churn probability:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"tenure_months":72,"monthly_fee":45.0,"contract":"two-year","internet_service":"dsl","support_calls":1}'
```

Example response:

```json
{
  "churn_probability": 0.008
}
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

On pushes to `main`, the workflow also:

- Builds the Docker image.
- Scans the image with Trivy.
- Publishes the image to GitHub Container Registry (GHCR).
- Tags the image using the commit SHA.

## Container Registry

GitHub Container Registry:

`ghcr.io/ahmadkh4led/ai381-lab2`

Pull the published image using:

```bash
docker pull ghcr.io/ahmadkh4led/ai381-lab2:3478ee82e7687c833216e8b4ac62f4f39484e607
```

Image Digest:

```text
sha256:fcfd919fe585baebcd54e115ee79c34dd43c4b2d846e8dd47c5bce77d8e40c2d
```

## Repository

[AI381-Lab2 – GitHub](https://github.com/Ahmadkh4led/AI381-Lab2)
