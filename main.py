from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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

# Configure my api to serve static files (.ply scenes)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Send a JSON response with available scenes ready to be streamed to the client
@app.get("/")
def read_root():
    # Dynamically discover scene directories in assets/
    assets_dir = "assets"
    active_scenes = (
        [d for d in os.listdir(assets_dir) if os.path.isdir(os.path.join(assets_dir, d))]
        if os.path.exists(assets_dir)
        else []
    )

    return {
        "status": "online",
        "service": "Volumetric Streamer",
        "active_scenes": active_scenes,
        "endpoints": {
            "assets": "/assets/{scene_name}/scene.spz"
        }
    }