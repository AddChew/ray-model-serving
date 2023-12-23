#!/bin/bash

source activate model-serving
python manage.py makemigrations demo
python manage.py migrate
uvicorn app:app --port 8000
# ray start --head --dashboard-port 8001 --metrics-export-port 8002
# serve run app:model -p 8003