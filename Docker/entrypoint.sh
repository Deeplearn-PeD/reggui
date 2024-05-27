#!/usr/bin/env bash

source .venv/bin/activate
uvicorn  reggui.main:run --host 0.0.0.0 --port 8060