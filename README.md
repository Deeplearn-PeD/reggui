# Reg D. Bot GUI app
Flet-based GUI for Reggie

## Installation

### Local Installation
```bash
sudo apt install libmpv1
poetry install
```

## Running the App

### Desktop Mode
To run the app in desktop mode:
```bash
poetry run python -m reggui
```

### Web Mode with Docker
To run the app as a web application using Docker Compose:

1. Build and start the containers:
```bash
docker compose up --build
```

2. Access the web interface at: http://localhost:8502

To stop the containers:
```bash
docker compose down
```
