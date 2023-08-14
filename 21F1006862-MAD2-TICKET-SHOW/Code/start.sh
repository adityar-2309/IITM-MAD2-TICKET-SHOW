#!/bin/bash

# Start the Flask server
cd backend
start cmd /k py app.py

# Start the Redis server inside WSL
wsl redis-server &

# Start Celery worker
cd backend
start cmd /k celery -A app:celery_app worker -l info -P eventlet

# Start Celery beat
cd backend
start cmd /k celery -A app:celery_app beat -l info

# Start the Vue.js server
cd ../frontend
start cmd /k npm run serve

# Open localhost:8080 in default browser
sleep 10
start http://localhost:8080
