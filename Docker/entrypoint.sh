#!/usr/bin/env bash

source .venv/bin/activate
hypercorn  reggui.main:app  --bind 0.0.0.0:8060