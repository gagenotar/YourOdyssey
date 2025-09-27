#!/bin/bash

# Activate virtual environment and run Django server
source "$(dirname "$(dirname "$0")")/.venv/bin/activate"
python manage.py runserver
