from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException,Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from DetectService import read_image_bytes, detect_ingredients
import asyncio
import uuid
import httpx
import os
import json


app = FastAPI(title="Recipe Generator API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

pending_requests = {}

class RecipeRequest(BaseModel):
    text: str
    ingredients: List[str]

class RecipeResponse(BaseModel):
    status: str
    data: dict
class DetectResponse(BaseModel):
    ingredients: List[str]
    confidence: float  
    raw_items: List[dict]  

@app.get("/api/recipe/result/{request_id}")
async def get_recipe_status(request_id: str):
    """
    Get the current status of a recipe generation request
    Returns: processing, retrying, completed, or not_found
    """
    try:
        file_path = f"recipe_results/{request_id}.json"
        
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                recipe_data = json.load(f)
            
            
            if "status" in recipe_data:
                return recipe_data  
            else:
                
                return {
                    "status": "completed",
                    "data": recipe_data
                }
        else:
            return {
                "status": "not_found",
                "message": "Recipe not yet available"
            }
            
    except Exception as e:
        print(f"Error getting recipe status: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

@app.post("/detect", response_model=DetectResponse)
async def detect(image: UploadFile = File(...)):
    """Detect ingredients from an uploaded image."""
    if image.content_type not in {"image/jpeg", "image/jpg", "image/png", "image/webp", "image/heic", "image/heif"}:
        raise HTTPException(400, "Please upload a JPEG/PNG/WEBP/HEIC image")

    
    img_bytes = read_image_bytes(image)
    
    
    result = detect_ingredients(img_bytes)
    
    return DetectResponse(**result)

@app.post("/recipe/generate")
async def generate_recipe(
    image: UploadFile = File(...),
    text: str = Form(...)
):
    """
    Start recipe generation: detect ingredients, write initial status file,
    start Action Agent in background and return request_id immediately.
    The frontend should poll /api/recipe/result/{request_id}.
    """
    try:
        # Step 1: Detect ingredients from image
        img_bytes = await image.read()
        detection = detect_ingredients(img_bytes)
        ingredients = detection["ingredients"]
        if not ingredients:
            raise HTTPException(400, "No ingredients detected in image")

        request_id = str(uuid.uuid4())
        pending_requests[request_id] = {
            "status": "processing",
            "ingredients": ingredients,
            "text": text
        }

        # Ensure result dir
        RESULTS_DIR = "recipe_results"
        os.makedirs(RESULTS_DIR, exist_ok=True)

        # Write initial detect status so frontend can show "Detecting" immediately
        detect_status = {
            "status": "processing",
            "stage": "detect",
            "step": "detect",
            "message": "Ingredients detected. Starting summarization...",
            "data": {
                "ingredients": ingredients,
                "confidence": detection.get("confidence", 0),
                "raw_items": detection.get("raw_items", [])
            }
        }
        file_path = os.path.join(RESULTS_DIR, f"{request_id}.json")
        with open(file_path, "w") as f:
            json.dump(detect_status, f, indent=2)

        # Start Action Agent in background so this endpoint returns immediately
        async def start_action_agent():
            try:
                async with httpx.AsyncClient(timeout=180.0) as client:
                    # adjust URL/port to your Action Agent service
                    resp = await client.post(
                        "http://localhost:8000/api/recipe/start",
                        json={
                            "text": text,
                            "ingredients": ingredients,
                            "session": request_id
                        }
                    )
                    # log response for debugging; agent itself should update status file
                    print(f"[background] Action Agent start status: {resp.status_code}")
                    print(f"[background] Action Agent body: {resp.text}")
            except Exception as e:
                print(f"[background] Failed to call Action Agent: {e}")
                # write an error status to results so frontend sees failure
                error_status = {
                    "status": "error",
                    "stage": "detect",
                    "step": "detect",
                    "message": f"Failed to start action agent: {str(e)}"
                }
                with open(file_path, "w") as f:
                    json.dump(error_status, f, indent=2)

        asyncio.create_task(start_action_agent())

        # Return immediately with request_id - frontend will poll for step updates
        return {"status": "accepted", "request_id": request_id}

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Error: {str(e)}")
        
@app.post("/recipe/webhook/{request_id}")
async def recipe_webhook(request_id: str, data: dict):
    """
    Webhook for agents to send results back
    Called by Advisor Agent when recipe is approved/rejected
    """
    print(f" Webhook received for {request_id}")
    
    if request_id in pending_requests:
        pending_requests[request_id].update(data)
        print(f"Updated request {request_id}")
        return {"ok": True}
    
    return {"ok": False, "error": "Request not found"}

        
@app.get("/health")
def health():
    """Health check endpoint."""
    return {"ok": True, "status": "running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="localhost", port=8080, reload=True)