from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api import routes as scenes_router
import os

# create a FastAPI instance to define routes, middleware and events, etc ..
app = FastAPI(title="Volumetric Streaming API", version="1.0.0")

# bridge that allows front-end applications running on a different domain, port, or protocol (e.g., a React app on http://localhost:3000) to safely communicate with the FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure my api to serve static files (.ply scenes) - note it doesn't send the files rather waits for client to request a file path then sends only that requested file
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Send a JSON response with available scenes ready to be streamed to the client
# Include the REST API routes
app.include_router(scenes_router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Peripheral Labs Volumetric Streamer",
        "endpoints": {
            "gallery": "/api/v1/scenes",
            "scene_detail": "/api/v1/scenes/{scene_id}"
        }
    }