from uagents import Agent, Bureau, Context, Model
from typing import List, Optional
from groq import Groq
from dotenv import load_dotenv
import os,asyncio
import json
import httpx
from agentFunction import Summarize,Cook,Caculate_rating,Generate_llm_feedback,CookAgain,clean_json_response,search_dish_image
load_dotenv()


recipe_results = {}
RESULTS_DIR = "recipe_results"  


if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

# Action Agent
class InputForAction(Model):
    text: str
    ingredients:List[str]
    session: Optional[str] = None

#
test_agent = Agent(
    name="test_agent",
    seed="test agent seed phrase",
    port=8010,
    #endpoint=["http://127.0.0.1:8010/submit"],
)

@test_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"🧪 Test Agent Address: {test_agent.address}")
    ctx.logger.info("Waiting 5 seconds before sending test message...")
    await asyncio.sleep(5)
    
    
    ACTION_AGENT_ADDRESS = "agent1qfa5mjk0f7rl24f5v9fa3fampa4kc724cl6wxa6s52x62q07v7emsqhxc4p"  # Replace with your action agent address
    
    test_message = InputForAction(
        text="I'm tire today, i just want to make under 10 minutes",
        ingredients=["beef", "rice", "green onion"]
    )
    
    ctx.logger.info(f"📤 Sending test message to Action Agent...")
    ctx.logger.info(f"   Text: {test_message.text}")
    ctx.logger.info(f"   Ingredients: {test_message.ingredients}")
    
    await ctx.send(ACTION_AGENT_ADDRESS, test_message)
    ctx.logger.info("✅ Test message sent!")
#

class SummarizeByAction(Model):
    favour: Optional[str] =None
    time: Optional[str] =None
    cuisine: Optional[str] =None
    ingredients:List[str]
    session: Optional[str] = None

action_agent = Agent(
    name="action_agent",
    seed="action agent seed",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],  # Re-enabled for REST access
)

class RecipeStartResponse(Model):
    success: bool
    session: Optional[str] = None
    message: str
    detected: Optional[dict] = None
    error: Optional[str] = None

@action_agent.on_rest_post("/api/recipe/start", InputForAction, RecipeStartResponse)
async def rest_start_recipe(ctx: Context, req: InputForAction) -> RecipeStartResponse:
    """
    REST endpoint to start recipe generation
    POST to: http://localhost:8001/api/recipe/start
    Body: {"text": "...", "ingredients": [...], "session": "..."}
    """
    ctx.logger.info(f" REST POST received: {req.text}")
    ctx.logger.info(f" Ingredients: {req.ingredients}")
    
    # Store initial status
    if req.session:
        recipe_results[req.session] = {
            "status": "processing",
            "stage": "summarizing"
        }
    
    try:
       
        result = await Summarize(req.text, req.ingredients)
        cleaned = clean_json_response(result)
        parsed = json.loads(cleaned)
        
        ctx.logger.info(f" Summarized: {parsed}")
        
        
        summarized = SummarizeByAction(
            favour=parsed.get("favour", ""),
            time=parsed.get("time", ""),
            cuisine=parsed.get("cuisine", ""),
            ingredients=req.ingredients,
            session=req.session
        )
        
        cooker_address = "agent1qwke9pml8wcysqqj4js4405wt29xqcrmw0xqw8gw7z84n8mwafdykdlyvjq"
        await ctx.send(cooker_address, summarized)
        
        if req.session:
            recipe_results[req.session]["stage"] = "cooking"
        
        return RecipeStartResponse(
            success=True,
            session=req.session,
            message="Recipe generation started",
            detected=parsed
        )
        
    except Exception as e:
        ctx.logger.error(f" Error: {e}")
        return RecipeStartResponse(
            success=False,
            error=str(e),
            message="Failed to start recipe generation"
        )


@action_agent.on_message(model=InputForAction)
async def handle_action(ctx: Context, sender: str, msg: InputForAction):
    ctx.logger.info(f"Received input from {sender}: {msg.text} and{msg.ingredients}")
    result = await Summarize(msg.text,msg.ingredients)
    ctx.logger.info(f"LLM Response: {result}")
    try:
        cleaned = clean_json_response(result)
        parsed = json.loads(cleaned)
        summarized = SummarizeByAction(
            favour=parsed.get("favour", ""),
            time=parsed.get("time", ""),
            cuisine=parsed.get("cuisine", ""),
            ingredients=msg.ingredients
        )
        cooker_address ="agent1qwke9pml8wcysqqj4js4405wt29xqcrmw0xqw8gw7z84n8mwafdykdlyvjq"
        await ctx.send(cooker_address, summarized)
    except Exception as e:
        ctx.logger.error(f"Failed to parse response: {e}")


# Cooker Agent


class OutputByCooker(Model):
    name:str
    ingredients_used: List[str]
    steps : List[str]
    calories: int
    health:str
    difficulty:str
    original_request: dict
    session: Optional[str] = None

class InputforAdvisor(Model):
    rating: float
    approved: bool
    feedback: str
    recipe: dict

class OutputforAdvisor(Model):
    original_request: dict
    feedback: str
    attempt: int
    session: Optional[str] = None

cooker_agent = Agent(
    name="cooker_agent",
    seed="cooker agent seed",
    port=8002,
    endpoint=["http://127.0.0.1:8002/submit"],  # Re-enabled for REST access
)
@cooker_agent.on_message(model=SummarizeByAction)
async def handle_cook(ctx:Context,sender:str,msg:SummarizeByAction):
        action_address = "agent1qfa5mjk0f7rl24f5v9fa3fampa4kc724cl6wxa6s52x62q07v7emsqhxc4p"
        ctx.logger.info(f"Received input from {action_address}: {msg} ")
        result = await Cook(msg)
        ctx.logger.info(f"LLM Response: {result}")
        try:
            cleaned = clean_json_response(result)
            parsed = json.loads(cleaned)
            output = OutputByCooker(
                name=parsed.get("name", ""),
                ingredients_used=parsed.get("ingredients_used", []),
                steps=parsed.get("steps", ""),
                calories=parsed.get("calories", 0),
                health=parsed.get("health", ""),
                difficulty=parsed.get("difficulty", ""),
                original_request={
                "ingredients": msg.ingredients,
                "favour": msg.favour,
                "time": msg.time,
                "cuisine": msg.cuisine
            },
                session=msg.session  # Pass session through
            )
            advisor_address = "agent1qv0zgfy639er7tdvpv6yep3my3hse4wvh7cge7g4rdrg4uj3h0qdqw9zt7e"
            await ctx.send(advisor_address, output)
        except Exception as e:
            ctx.logger.error(f"Failed to parse response: {e}")
@cooker_agent.on_message(model=OutputforAdvisor)
async def handle_retry(ctx: Context, sender: str, msg: OutputforAdvisor):
    ctx.logger.info(f" Retry attempt #{msg.attempt}")
    ctx.logger.info(f" Feedback: {msg.feedback}")
    retry = await CookAgain(msg)
    ctx.logger.info(f"LLM Response: {retry}")
    try:
        cleaned = clean_json_response(retry)
        parsed = json.loads(cleaned)
        steps = parsed.get("steps", [])
        if isinstance(steps, str):
            steps = [steps]
        output = OutputByCooker(
        name=parsed.get("name", ""),
        ingredients_used=parsed.get("ingredients_used", []),
        steps=parsed.get("steps", ""),
        calories=parsed.get("calories", 0),
        health=parsed.get("health", ""),
        difficulty=parsed.get("difficulty", ""),
        original_request={
                "ingredients": msg.original_request.get("ingredients", []),  
                "favour": msg.original_request.get("favour", ""),
                "time": msg.original_request.get("time", ""),
                "cuisine": msg.original_request.get("cuisine", ""),
                "attempt": msg.attempt  
        },
        session=msg.session  # Pass session through retry
        )
        advisor_address = "agent1qv0zgfy639er7tdvpv6yep3my3hse4wvh7cge7g4rdrg4uj3h0qdqw9zt7e"
        await ctx.send(advisor_address, output)
    except Exception as e:
            ctx.logger.error(f"Failed to parse response: {e}")

advisor_agent = Agent(
    name="advisor_agent",
    seed="food advisor agent seed",
    port=8003,
    endpoint=["http://127.0.0.1:8003/submit"],  # Re-enabled for REST access
)

class RecipeResultResponse(Model):
    status: str
    session: Optional[str] = None
    data: Optional[dict] = None
    stage: Optional[str] = None

@advisor_agent.on_rest_get("/api/recipe/result/{session_id}", RecipeResultResponse)
async def get_recipe_result(ctx: Context, session_id: str) -> RecipeResultResponse:
    """
    REST endpoint to check recipe result
    GET: http://localhost:8003/api/recipe/result/{session_id}
    """
    ctx.logger.info(f" REST GET for session: {session_id}")
    ctx.logger.info(f" Available sessions in memory: {list(recipe_results.keys())}")
    
    # Try to get from memory first
    if session_id in recipe_results:
        result = recipe_results[session_id]
        ctx.logger.info(f" Found result in memory for session: {session_id}")
        return RecipeResultResponse(
            status=result.get("status", "unknown"),
            session=session_id,
            data=result.get("data"),
            stage=result.get("stage")
        )
    
    # Try to read from file as backup
    file_path = os.path.join(RESULTS_DIR, f"{session_id}.json")
    ctx.logger.info(f" Checking file: {file_path}")
    ctx.logger.info(f" File exists: {os.path.exists(file_path)}")
    
    # List all files in directory
    if os.path.exists(RESULTS_DIR):
        files = os.listdir(RESULTS_DIR)
        ctx.logger.info(f" Files in {RESULTS_DIR}: {files}")
    
    if os.path.exists(file_path):
        ctx.logger.info(f" Found result in file: {file_path}")
        with open(file_path, 'r') as f:
            result = json.load(f)
        return RecipeResultResponse(
            status=result.get("status", "unknown"),
            session=session_id,
            data=result.get("data"),
            stage=result.get("stage")
        )
    
    # Not found anywhere
    ctx.logger.info(f"Session not found: {session_id}")
    return RecipeResultResponse(
        status="not_found",
        session=session_id
    )
@advisor_agent.on_message(model=OutputByCooker)
async def evaluate_recipe(ctx:Context,sender: str, msg: OutputByCooker):
    ctx.logger.info(f" Advisor received recipe: {msg.name}")
    rating = Caculate_rating(msg)
    total_score = rating["total"]
    ctx.logger.info(f" Score: {total_score}/100")
    ctx.logger.info(f" Breakdown: {rating['breakdown']}")
    
    
    current_attempt = msg.original_request.get('attempt', 0)
    MAX_RETRIES = 30
    
    if total_score >= 84:
        ctx.logger.info(f" Recipe APPROVED!")
        
        # Search for dish image
        ctx.logger.info(f" Searching for image of '{msg.name}'...")
        image_url = await search_dish_image(msg.name)
        
        if msg.session:
            result_data = {
                "status": "completed",
                "data": {
                    "name": msg.name,
                    "image_link": image_url,
                    "step_by_step": msg.steps,
                    "rating": total_score,
                    "calories": msg.calories,
                    "health": msg.health,
                    "difficulty": msg.difficulty,
                    "ingredients_used": msg.ingredients_used
                }
            }
            
            
            
            
            
            file_path = os.path.join(RESULTS_DIR, f"{msg.session}.json")
            with open(file_path, 'w') as f:
                json.dump(result_data, f, indent=2)
            
            
            ctx.logger.info(f" Saved to file: {file_path}")
        
    elif current_attempt >= MAX_RETRIES:
        
        ctx.logger.info(f"Max retries ({MAX_RETRIES}) reached. Returning current recipe (Score: {total_score}/100)")
        
        
        ctx.logger.info(f" Searching for image of '{msg.name}'...")
        image_url = await search_dish_image(msg.name)
        
        if msg.session:
            result_data = {
                "status": "completed",
                "data": {
                    "name": msg.name,
                    "image_link": image_url,
                    "step_by_step": msg.steps,
                    "rating": total_score,
                    "calories": msg.calories,
                    "health": msg.health,
                    "difficulty": msg.difficulty,
                    "ingredients_used": msg.ingredients_used
                }
            }
            
          
            
           
            file_path = os.path.join(RESULTS_DIR, f"{msg.session}.json")
            with open(file_path, 'w') as f:
                json.dump(result_data, f, indent=2)
            
            ctx.logger.info(f"Stored result for session: {msg.session}")
            ctx.logger.info(f"Saved to file: {file_path}")
    
    else:
        ctx.logger.info(f"Recipe needs improvement (Score: {total_score}/100) - Attempt {current_attempt + 1}/{MAX_RETRIES}")
        feedback = Generate_llm_feedback(rating, msg.original_request)
        retry = OutputforAdvisor(
            original_request=msg.original_request,
            feedback=feedback,
            attempt=current_attempt + 1,
            session=msg.session  # Pass session through retry
        )
        
        cooker_address = "agent1qwke9pml8wcysqqj4js4405wt29xqcrmw0xqw8gw7z84n8mwafdykdlyvjq"
        await ctx.send(cooker_address, retry)
        ctx.logger.info(" Sent feedback to Cooker for retry")


@action_agent.on_event("startup")
async def action_startup(ctx: Context):
    ctx.logger.info(f"Action Agent Address: {action_agent.address}")
    
@cooker_agent.on_event("startup")
async def cooker_startup(ctx: Context):
    ctx.logger.info(f"Cooker Agent Address: {cooker_agent.address}")

@advisor_agent.on_event("startup")
async def advisor_startup(ctx: Context):
    ctx.logger.info(f"Advisor Agent Address: {advisor_agent.address}")

family = Bureau(port=8000,endpoint="http://127.0.0.1:8000/submit")
family.add(action_agent)
family.add(cooker_agent)
family.add(advisor_agent)
# family.add(test_agent)


if __name__ == "__main__":
    family.run()
