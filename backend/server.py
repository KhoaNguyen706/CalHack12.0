from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from DetectAgent import read_image_bytes, detect_ingredients


app = FastAPI(title="Image → Ingredients")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)


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


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"ok": True, "status": "running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="localhost", port=8000, reload=True)