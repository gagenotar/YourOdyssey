#!/bin/bash

# Activate virtual environment and run the Flask app for development
source "$(dirname "$(dirname "$0")")/.venv/bin/activate"
python flask_app.py
