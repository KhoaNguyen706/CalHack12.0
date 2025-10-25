from uagents import Agent, Bureau, Context, Model
from typing import List, Optional
from groq import Groq
from dotenv import load_dotenv
import os
import json
from agentFunction import Summarize,Cook,Caculate_rating,Generate_llm_feedback,CookAgain
load_dotenv()

# Action Agent
class InputForAction(Model):
    text: str
    ingredients:List[str]

class SummarizeByAction(Model):
    favour: str
    time: str
    cuisine: str
    ingredients:List[str]

action_agent = Agent(
    name="action_agent",
    seed="action agent seed",
    port=8001,
    #endpoint=["http://127.0.0.1:8001/submit"],
)
@action_agent.on_message(model=InputForAction)
async def handle_action(ctx: Context, sender: str, msg: InputForAction):
    ctx.logger.info(f"Received input from {sender}: {msg.text} and{msg.ingredients}")
    result = await Summarize(msg.text,msg.ingredients)
    ctx.logger.info(f"LLM Response: {result}")
    try:
        parsed = json.loads(result)
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
class InputForCooker(Model):
    ingredients:List[str]
    favour:str
    time:str
    cuisine:str

class OutputByCooker(Model):
    name:str
    ingredients_used: List[str]
    steps : str
    calories: int
    health:str
    difficulty:str
    original_request: dict

class InputforAdvisor(Model):
    rating: float
    approved: bool
    feedback: str
    recipe: dict

class OutputforAdvisor(Model):
    original_request: dict
    feedback: str
    attempt: int

cooker_agent = Agent(
    name="cooker_agent",
    seed="cooker agent seed",
    port=8002,
    #endpoint=["http://127.0.0.1:8002/submit"],
)
@cooker_agent.on_message(model=SummarizeByAction)
async def handle_cook(ctx:Context,sender:str,msg:SummarizeByAction):
        action_address = "agent1qfa5mjk0f7rl24f5v9fa3fampa4kc724cl6wxa6s52x62q07v7emsqhxc4p"
        ctx.logger.info(f"Received input from {action_address}: {msg} ")
        result = await Cook(msg)
        ctx.logger.info(f"LLM Response: {result}")
        try:
            parsed = json.loads(result)
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
            }
            )
            advisor_address = "agent1qv0zgfy639er7tdvpv6yep3my3hse4wvh7cge7g4rdrg4uj3h0qdqw9zt7e"
            await ctx.send(advisor_address, output)
        except Exception as e:
            ctx.logger.error(f"Failed to parse response: {e}")
@cooker_agent.on_message(model=OutputforAdvisor)
async def handle_retry(ctx: Context, sender: str, msg: OutputforAdvisor):
    ctx.logger.info(f"🔄 Retry attempt #{msg.attempt}")
    ctx.logger.info(f"📝 Feedback: {msg.feedback}")
    retry = CookAgain(msg)



advisor_agent = Agent(
    name="advisor_agent",
    seed="food advisor agent seed",
    port=8003,
    #endpoint=["http://127.0.0.1:8003/submit"],
)
@advisor_agent.on_message(model=OutputByCooker)
async def evaluate_recipe(ctx:Context,sender: str, msg: OutputByCooker):
    ctx.logger.info(f" Advisor received recipe: {msg.name}")
    rating = Caculate_rating(msg)
    total_score = rating["total"]
    ctx.logger.info(f" Score: {total_score}/100")
    ctx.logger.info(f" Breakdown: {rating['breakdown']}")
    if total_score >= 85:
        ctx.logger.info(f"Recipe APPROVED!")
        # return back to frontend
    else:
        ctx.logger.info(f" Recipe needs improvement (Score: {total_score}/100)")
        feedback = Generate_llm_feedback(rating, msg.original_request)
        retry = OutputforAdvisor(
            original_request=msg.original_request,
            feedback=feedback,
            attempt=msg.original_request.get('attempt', 0) + 1
        )
        
        cooker_address = "agent1qwke9pml8wcysqqj4js4405wt29xqcrmw0xqw8gw7z84n8mwafdykdlyvjq"
        await ctx.send(cooker_address, retry)
        ctx.logger.info(" Sent feedback to Cooker for retry")


@action_agent.on_event("startup")
async def action_startup(ctx: Context):
    ctx.logger.info(f"🎯 Action Agent Address: {action_agent.address}")
    
@cooker_agent.on_event("startup")
async def cooker_startup(ctx: Context):
    ctx.logger.info(f"👨‍🍳 Cooker Agent Address: {cooker_agent.address}")

@advisor_agent.on_event("startup")
async def advisor_startup(ctx: Context):
    ctx.logger.info(f"🎯 Advisor Agent Address: {advisor_agent.address}")

family = Bureau(port=8000,endpoint="http://127.0.0.1:8000/submit")
family.add(action_agent)
family.add(cooker_agent)
family.add(advisor_agent)


if __name__ == "__main__":
    family.run()
