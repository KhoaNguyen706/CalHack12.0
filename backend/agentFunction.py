from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

async def Summarize(text,ingredients):
    summarize_prompt = f"""
    Your role is Input Anlysis. 
    Given a text input and ingredients list like ["...","orange"], summarize it into JSON format.
    ONLY RETURN VALID JSON, nothing else.
    
    Example input: "I want to make sweet thailand food that takes an 1 hour"
    Example output:
    {{
        "ingredients":["tomato","egg","banana"]
        "favour": "sweet",
        "time": "around_1_hour",
        "cuisine": "thailand"
    }}
    
    Now process this input: "{text} and {ingredients}"
    """
    
    response = client.chat.completions.create(
        model="moonshotai/kimi-k2-instruct-0905",  # Updated model
        messages=[
            {"role": "system", "content": "You are a summarization assistant. Extract favour, time, and cuisine from user input."},
            {"role": "user", "content": summarize_prompt}
        ],
        max_tokens=100
    )
    
    result = response.choices[0].message.content.strip()
    return result


async def Cook(msg):
    cooking_prompt =f"""
    you are 3 star Michelein cheft or restaurant chef or 20+ experienced chef.
    your task is to give input ingredients, time, cuisine, favour
    with current ingredients, you are chef, that mean you must cook the best food
    if cuisine is None, you will invent the dishes like your job
    always make food by priority favour. 
    After cooking, you ONLY RETURN VALID JSON FORMAT nothing else
    Example:
    {{
        "name":"beef pho"
        "ingredients_used": ["beef","onion","noodle"]
        "steps" : ["slice onion","wash beef"]
        "calories": 400
        "health": "Good"
        "difficulty": "hard"
        "original_request": 
    }}
    Now process this message: "{msg}"

    In case: Our food advisor rate your food below 85 points you should try to find new different
    dishes make it you only have 3 attempts to perform. Lets do your best
"""
    response = client.chat.completions.create(
        model="moonshotai/kimi-k2-instruct-0905",  # Updated model
        messages=[
            {"role": "system", "content": "You are a extremly perfect chef. Cooking by your heart"},
            {"role": "user", "content": cooking_prompt}
        ],
        max_tokens=500
    )
    
    result = response.choices[0].message.content.strip()
    return result

async def CookAgain(msg):
    cooking_again_prompt =f"""
    you are 3 star Michelein cheft or restaurant chef or 20+ experienced chef.
    this case because you are fail to pass by Food Advisor
    you give original_request , feed back, attempt
    You have 2 options to improve your reciept: 
    1. Change the dishes
    2. Change the ingredients you used to fit with feed back
    Return ONLY JSON FORMAT nothing else
    {{
        "name":"new dishes",
        "ingredients_used": ["beef","onion","rice","tomato"],
        "steps" : ["slice onion","wash beef"],
        "calories": 400,
        "health": "Good",
        "difficulty": "hard",
    }}
"""
    response = client.chat.completions.create(
        model="moonshotai/kimi-k2-instruct-0905",  # Updated model
        messages=[
            {"role": "system", "content": "You are a extremly perfect chef. Cooking by your heart"},
            {"role": "user", "content": cooking_again_prompt}
        ],
        max_tokens=500
    )
    
    result = response.choices[0].message.content.strip()
    return result
    
def Caculate_rating(msg) -> dict:
    scores ={
        "calories":0,
        "health":0,
        "difficulty":0,
        "ingredients":0,
        "steps":0
    }
    reasons =[]

    #calories scores
    if 350 <=msg.calories <= 600:
        scores["calories"] = 25
    elif msg.calories <350:
        scores["calories"] = 15
        reasons.append(f"Calories too low {msg.calories}")
    else:
        reasons.append(f"Calories too high {msg.calories}")

    #health
    if msg.health.lower() in ["healthy", "very healthy"]:
        scores["health"] = 20
    elif msg.health.lower() == "moderate":
        scores["health"] = 15
        reasons.append("Health score is moderate")
    else:
        scores["health"] = 10
        reasons.append("Unhealthy")

    # dfficulty 
    if msg.difficulty.lower() == "easy":
        scores["difficulty"] = 25
    elif msg.difficulty.lower() == "medium":
        scores["difficulty"] = 15
        reasons.append("Could be easier")
    else:
        scores["difficulty"] = 10
        reasons.append("Too difficult")

    num_ingredients = len(msg.ingredients_used)
    if num_ingredients >= 4:
        scores["ingredients"] = 20
    elif num_ingredients >= 2:
        scores["ingredients"] = 15
        reasons.append("Using fewer ingredients")
    else:
        scores["ingredients"] = 10
        reasons.append("lack of nutrients")

    if len(msg.steps) > 100:
        scores["steps"] = 5
        reasons.append("Steps too long")
    elif len(msg.steps) > 50:
        scores["steps"] = 10
        reasons.append("Steps could be more reduced")
    else:
        scores["steps"] = 15

    total = sum(scores.values())
    return {
        "total": total,
        "breakdown": scores,
        "reasons": reasons,
        "recipe_data": {
            "name": msg.name,
            "calories": msg.calories,
            "health": msg.health,
            "difficulty": msg.difficulty,
            "ingredients_count": num_ingredients
        }
    }

def Generate_llm_feedback(rating_data: dict, original_request: dict) -> str:
    """Use LLM to generate actionable feedback"""
    
    prompt = f"""
You are a recipe quality advisor. A recipe has been evaluated and needs improvement.

RECIPE EVALUATION:
- Recipe Name: {rating_data['recipe_data']['name']}
- Total Score: {rating_data['total']}/100
- Score Breakdown:
  * Calories: {rating_data['breakdown']['calories']}/20
  * Health: {rating_data['breakdown']['health']}/25
  * Difficulty: {rating_data['breakdown']['difficulty']}/20
  * Ingredients: {rating_data['breakdown']['ingredients']}/20
  * Steps: {rating_data['breakdown']['steps']}/15

ISSUES FOUND:
{chr(10).join('- ' + reason for reason in rating_data['reasons'])}

ORIGINAL REQUEST:
- Favour: {original_request.get('favour')}
- Cuisine: {original_request.get('cuisine')}
- Time: {original_request.get('time')}
- Available Ingredients: {', '.join(original_request.get('ingredients', []))}

TASK: Provide specific, actionable feedback on how to improve this recipe to score above 85 points.
Focus on:
1. What to change (be specific)
2. Why it will improve the score
3. How to maintain the user's preferences

Keep feedback concise and actionable (3-5 bullet points).
"""

    response = client.chat.completions.create(
        model="moonshotai/kimi-k2-instruct-0905",
        messages=[
            {"role": "system", "content": "You are an expert recipe advisor. Provide specific, actionable feedback."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    result = response.choices[0].message.content.strip()
    return result

def clean_json_response(response: str) -> str:
    """Remove markdown code blocks and extra whitespace from LLM response"""
    response = response.strip()
    if response.startswith("```json"):
        response = response[7:]  
    elif response.startswith("```"):
        response = response[3:]  
    if response.endswith("```"):
        response = response[:-3]  
    return response.strip()

async def search_dish_image(dish_name: str) -> str:
    """
    Search for a dish image using multiple methods:
    1. Unsplash API (free, high quality)
    2. Bright Data (if configured)
    3. Placeholder image as fallback
    """
    import httpx
    import urllib.parse
    
    try:
        # Try Unsplash first (free, no API key needed for basic usage)
        search_query = urllib.parse.quote(f"{dish_name} food")
        unsplash_url = f"https://source.unsplash.com/800x600/?{search_query}"
        
        print(f" Generated image URL for '{dish_name}': {unsplash_url}")
        return unsplash_url
        
    except Exception as e:
        print(f" Error generating image URL: {e}")
        # Fallback to a placeholder
        search_query = urllib.parse.quote(dish_name)
        return f"https://via.placeholder.com/800x600.png?text={search_query}"
        