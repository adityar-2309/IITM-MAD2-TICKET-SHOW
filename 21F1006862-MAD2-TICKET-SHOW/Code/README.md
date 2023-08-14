# Movie Ticket Booking App

Welcome to the Movie Ticket Booking App! This application is built using Flask for the backend and Vue.js for the frontend. It allows users to book movie tickets, receive daily reminders, generate monthly reports, and export data to CSV. The backend also utilizes Redis for caching and Celery for background jobs.

## Setup

### Backend (Flask, Celery, Redis)

1. Open a terminal and navigate to the `backend` folder:
   ```
   cd backend
   ```

2. Install the required packages using `pip`:
   ```
   pip install -r requirements.txt
   ```

3. Start the Celery worker and beat scheduler:
   ```
   celery -A app:celery_app worker -l info -P eventlet
   celery -A app:celery_app beat -l info
   ```

4. Run the Flask app:
   ```
   python app.py
   ```

### Frontend (Vue.js)

1. Open a new terminal window/tab and navigate to the `frontend` folder:
   ```
   cd frontend
   ```

2. Install the required dependencies using `npm`:
   ```
   npm install
   ```

3. Run the Vue.js development server:
   ```
   npm run serve
   ```

### Redis (WSL)

1. If you don't have WSL installed, follow the instructions [here](https://docs.microsoft.com/en-us/windows/wsl/install) to set it up.

2. Install Redis in your WSL:
   ```
   sudo apt update
   sudo apt install redis-server
   ```

3. Start the Redis server:
   ```
   redis-server
   ```

## Usage

1. Access the frontend by navigating to `http://localhost:8080` in your web browser.

2. Use the Movie Ticket Booking App to book tickets, view reports, and export data.

3. Background jobs such as daily reminders and monthly reports will be handled by Celery workers.
