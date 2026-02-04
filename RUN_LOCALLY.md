# How to Run Locally

You can run the AI Code Reviewer application locally without Docker.

## Prerequisites

- **Python 3.11+** (for Backend)
- **Node.js 18+** (for Frontend)

## Quick Start (Windows)

### One-Click Start (Recommended)

1.  Double-click `run_app.bat` in the root directory.
    - This will open two new windows: one for the backend and one for the frontend.
    - The application will be accessible at [http://localhost:3000](http://localhost:3000).

### Manual Start

If you prefer to run them separately:

### 1. Backend

1.  Navigate to the `backend` directory.
2.  Double-click `run_local.bat`.
    - This will automatically create a virtual environment, install dependencies, and start the server.
    - The server will run at [http://localhost:8000](http://localhost:8000).

### 2. Frontend

1.  Navigate to the `frontend` directory.
2.  Double-click `run_local.bat`.
    - This will install Node dependencies and start the development server.
    - The application will run at [http://localhost:3000](http://localhost:3000).

## Manual Setup

### Backend

1.  Navigate to `backend`:
    ```bash
    cd backend
    ```
2.  Create and activate virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the server:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```
5.  Access API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

### Frontend

1.  Navigate to `frontend`:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start development server:
    ```bash
    npm run dev
    ```

## Environment Variables

Make sure the `.env` file in the root or `backend` directory is properly configured with your AWS credentials.

For details on configuring AWS SSO, see [AWS_SETUP.md](AWS_SETUP.md).
