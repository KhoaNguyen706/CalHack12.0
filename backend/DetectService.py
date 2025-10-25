import os
import io
import json
from typing import List, Dict
from fastapi import UploadFile, HTTPException
from PIL import Image
from dotenv import load_dotenv
from rapidfuzz import process as rf_process, fuzz as rf_fuzz
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("Set GEMINI_API_KEY in .env")

genai.configure(api_key=api_key)
gem_model = genai.GenerativeModel("gemini-2.5-flash")


CANON = [
    "apple", "banana", "orange", "lemon", "lime", "grape", "strawberry", "blueberry", "mango",
    "avocado", "tomato", "cucumber", "carrot", "broccoli", "lettuce", "spinach", "onion", "garlic",
    "potato", "egg", "milk", "cheese", "yogurt", "butter", "rice", "pasta", "bread", "chicken", "beef", "tofu"
]


def best_match(token: str, choices: List[str], thr: int = 85):
    """Match a token to the best canonical ingredient name."""
    token = (token or "").strip().lower()
    if not token:
        return None
    match, score, _ = rf_process.extractOne(token, choices, scorer=rf_fuzz.WRatio)
    return match if score >= thr else None


def read_image_bytes(upload: UploadFile) -> bytes:
    """Read and normalize image to JPEG bytes for Gemini."""
    raw = upload.file.read()
    try:
        img = Image.open(io.BytesIO(raw)).convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=90)
        return buf.getvalue()
    except Exception:
        
        return raw


def detect_ingredients(image_bytes: bytes) -> Dict:
    """
    Detect ingredients from image using Gemini Vision API.
    
    Args:
        image_bytes: JPEG image bytes
        
    Returns:
        Dict with keys: ingredients (List[str]), confidence (float), raw_items (List[dict])
    """
    prompt = (
        "You are an ingredient detector for fridge photos or for table photos. "
        "List visible edible ingredients/foods (not brands/containers). "
        "Return ONLY JSON: {\"ingredients\":[{\"name\":\"apple\",\"confidence\":0.92}, ...]} "
        "Use lowercase common names and include 5–15 items max."
    )

    image_part = {"inline_data": {"mime_type": "image/jpeg", "data": image_bytes}}
    
    try:
        resp = gem_model.generate_content(
            [prompt, image_part],
            generation_config={"response_mime_type": "application/json"}
        )
        data = json.loads(resp.text)
        items = data.get("ingredients", [])
    except Exception as e:
        raise HTTPException(500, f"Vision model error: {e}")

    
    names, top_conf = [], 0.0
    for it in items:
        n = str(it.get("name", "")).lower().strip()
        c = float(it.get("confidence", 0.0))
        m = best_match(n, CANON, 80) or n  
        names.append(m)
        top_conf = max(top_conf, c)

    cleaned = sorted(set(names))
    
    return {
        "ingredients": cleaned,
        "confidence": float(top_conf),
        "raw_items": items
    }