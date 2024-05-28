#!/usr/bin/env bash

source .venv/bin/activate
uvicorn --factory reggui.main:run --reload --host 0.0.0.0 --port 8060