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


@app.post("/detect", response_model=DetectResponse)
async def detect(image: UploadFile = File(...)):
    """Detect ingredients from an uploaded image."""
    if image.content_type not in {"image/jpeg", "image/jpg", "image/png", "image/webp", "image/heic", "image/heif"}:
        raise HTTPException(400, "Please upload a JPEG/PNG/WEBP/HEIC image")

    
    img_bytes = read_image_bytes(image)
    
    
    result = detect_ingredients(img_bytes)
    
    return DetectResponse(**result)

@app.post("/recipe/generate", response_model=RecipeResponse)
async def generate_recipe(
    image: UploadFile = File(...),
    text: str = Form(...)
):
    """
    Generate recipe from image and text preferences.
    
    This endpoint:
    1. Detects ingredients from image
    2. Sends to Action Agent → Cooker Agent → Advisor Agent
    3. Waits for final approved recipe
    4. Returns complete recipe with rating
    
    Args:
        image: Uploaded image of ingredients
        text: User preferences (e.g., "I want spicy Thai food in 30 minutes")
        
    Returns:
        {
            "status": "successfully",
            "data": {
                "name": "Recipe Name",
                "image_link": "https://...",
                "step_by_step": ["Step 1", "Step 2", ...],
                "rating": 85,
                "calories": 550,
                "health": "healthy",
                "difficulty": "easy",
                "ingredients_used": ["chicken", "rice", ...]
            }
        }
    """
    try:
        # Step 1: Detect ingredients from image
        print(f"Reading image...")
        img_bytes = await image.read()  # Read file bytes
        print(f"Image size: {len(img_bytes)} bytes")
        
        print(f"Detecting ingredients...")
        detection = detect_ingredients(img_bytes)
        print(f"Detection result: {detection}")
        
        ingredients = detection["ingredients"]
        if not ingredients:
            raise HTTPException(400, "No ingredients detected in image")
        
        print(f"Found ingredients: {ingredients}")
        
        request_id = str(uuid.uuid4())
        pending_requests[request_id] = {
            "status": "processing",
            "ingredients": ingredients,
            "text": text
        }
        async with httpx.AsyncClient(timeout=180.0) as client:
            print("Sending to Action Agent...")
            print(f" Request data: text='{text}', ingredients={ingredients}, session={request_id}")
            
            # Send to Action Agent's individual REST endpoint
            start_response = await client.post(
                "http://localhost:8000/api/recipe/start",  # Action Agent on port 8001
                json={
                    "text": text,
                    "ingredients": ingredients,
                    "session": request_id
                }
            )
            
            print(f"Action Agent response status: {start_response.status_code}")
            print(f"Response body: {start_response.text}")
            
            if start_response.status_code != 200:
                error_text = start_response.text
                print(f"Error response: {error_text}")
                raise HTTPException(500, f"Action Agent returned {start_response.status_code}: {error_text}")
            
            start_result = start_response.json()
            print(f"Recipe started: {start_result}")
            
            
            print("Waiting for recipe to complete...")
            RESULTS_DIR = "recipe_results"
            for i in range(36): 
                await asyncio.sleep(5)
                
                
                file_path = os.path.join(RESULTS_DIR, f"{request_id}.json")
                
                if os.path.exists(file_path):
                    
                    print(f"📁 Found result file: {file_path}")
                    with open(file_path, 'r') as f:
                        result = json.load(f)
                    
                    status = result.get("status")
                    print(f"   [{(i+1)*5}s] Status: {status}, Data: {result.get('data') is not None}")
                else:
                
                    print(f"   [{(i+1)*5}s] Waiting for recipe...")
                    status = None
                    result = {}
                
              
                if status == "completed" and result.get("data"):
                    print(f"\n✅ Recipe completed successfully!\n")
                    
                    data = result.get("data", {})
                    
                    
                    response = RecipeResponse(
                        status="successfully",
                        data={
                            "name": data.get("name"),
                            "image_link": data.get("image_link", ""),
                            "step_by_step": data.get("step_by_step", []),
                            "rating": data.get("rating"),
                            "calories": data.get("calories"),
                            "health": data.get("health"),
                            "difficulty": data.get("difficulty"),
                            "ingredients_used": data.get("ingredients_used", []),
                            "detected_ingredients": ingredients,
                            "confidence": detection.get("confidence")
                        }
                    )
                    
                
                    try:
                        os.remove(file_path)
                        print(f"🗑️ Deleted result file: {file_path}")
                    except Exception as e:
                        print(f"⚠️ Warning: Could not delete file {file_path}: {e}")
                    
                    return response
                
                
                elif status == "completed" and not result.get("data"):
                    error = result.get("error", "Recipe generation failed")
                    print(f"\n❌ Recipe failed: {error}\n")
                    raise HTTPException(422, error)
                
                
                elif status == "not_found":
                    print(f"\n❌ Session not found!\n")
                    raise HTTPException(404, "Session not found in advisor agent")
            
            
            raise HTTPException(408, "Recipe generation timeout after 3 minutes")
        
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