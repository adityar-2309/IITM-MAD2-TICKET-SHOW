REM Start the Flask server
cd backend
start cmd /k py app.py

REM Start Celery worker
cd backend
start cmd /k celery -A app:celery_app worker -l info -P eventlet

REM Start Celery beat
cd backend
start cmd /k celery -A app:celery_app beat -l info

REM Start mailhog
start cmd /k  C:\Users\dashc\Downloads\Programs\MailHog_windows_amd64.exe

REM Start the Vue.js server
cd ../frontend
start cmd /k npm install

REM Start the Vue.js server
cd ../frontend
start cmd /k npm run serve

REM Open localhost:8080 in default browser
timeout /t 10
start http://localhost:8080

REM Start the Redis server inside WSL
wsl redis-cli

