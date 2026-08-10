from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import tasks

app = FastAPI(
    title="Task Manager API",
    description="A simple CRUD API for managing tasks, built while learning FastAPI.",
    version="1.0.0",
)

# --- CORS CONFIGURATION ---
# By default, browsers block JavaScript running on one origin (e.g.
# http://localhost:5173, our Vite React app) from calling an API on a
# different origin (e.g. http://localhost:8000, our FastAPI server).
# This middleware tells the browser "these specific origins are allowed
# to talk to me" -- without it, our React app's fetch() calls would fail
# with a CORS error even though the API itself works fine (e.g. via curl
# or /docs, which aren't subject to browser CORS rules).

origins = [
    "http://localhost:5173",  # Vite's default dev server port
    "http://127.0.0.1:5173",
    "http://localhost:5174",   # add whatever port your terminal actually shows
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # which frontend origins can call us
    allow_credentials=True,     # allow cookies/auth headers if we add them later
    allow_methods=["*"],        # allow GET, POST, PATCH, DELETE, etc.
    allow_headers=["*"],        # allow any request headers (e.g. Content-Type)
)


# Schema creation is now handled entirely by Alembic migrations
# (`alembic upgrade head`), not by the app itself. This mirrors how
# real deployments work: migrations run as an explicit step (e.g. in
# a CI/CD pipeline or release script), separate from the app starting up.

# Mount our task routes onto the main app. Every route in tasks.py
# is now live under the /tasks prefix we defined in the router.
app.include_router(tasks.router)


@app.get("/")
def root():
    return {"message": "Task Manager API is running. Visit /docs for interactive API docs."}