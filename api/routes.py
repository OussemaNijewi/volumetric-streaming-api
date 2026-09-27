import json
from pathlib import Path
from fastapi import APIRouter, HTTPException

#group related API endpoints together into this separate, modular component
router = APIRouter(prefix="/api/v1", tags=["Scenes"])
ASSETS_DIR = Path("assets")

@router.get("/scenes")
def get_scenes():
    """Returns a list of available scenes for the dashboard gallery."""
    if not ASSETS_DIR.exists():
        return []

    scenes = []
    for folder in ASSETS_DIR.iterdir():
        if folder.is_dir():
            metadata_path = folder / "metadata.json"
            if metadata_path.is_file():
                try:
                    with open(metadata_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        scenes.append({
                            "scene_id": data.get("scene_id", folder.name),
                            "scene_name": data.get("scene_name", folder.name),
                            "thumbnail_url": data.get("thumbnail_url", f"/assets/{folder.name}/thumbnail.png"),
                            "hotspot_count": len(data.get("hotspots", []))
                        })
                except json.JSONDecodeError:
                    continue

    return scenes


@router.get("/scenes/{scene_id}")
def get_scene_metadata(scene_id: str):
    """Returns full metadata JSON for a specific scene viewer."""
    metadata_path = ASSETS_DIR / scene_id / "metadata.json"

    if not metadata_path.is_file():
        raise HTTPException(status_code=404, detail=f"Scene '{scene_id}' not found.")

    with open(metadata_path, "r", encoding="utf-8") as f:
        return json.load(f)