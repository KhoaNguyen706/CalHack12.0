from uagents import Agent, Bureau, Context, Model
from typing import List, Optional
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

user_input = "I want to make spicy Japanese food under 20 minutes"

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Action 
class Input(Model):
    text: str
    


class Summarize(Model):
    favour: str
    time: str
    cuisine: str

action_agent = Agent(
    name="action_agent",
    seed="action agent seed",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)

@action_agent.on_message(model=Input)
async def handle_action(ctx: Context, sender: str, msg: Input):
    ctx.logger.info(f"Received input from {sender}: {msg.text}")
    
    summarize_prompt = f"""
    Given a text input, summarize it into JSON format.
    ONLY RETURN VALID JSON, nothing else.
    
    Example input: "I want to make sweet thailand food around 1 hour"
    Example output:
    {{
        "favour": "sweet",
        "time": "around_1_hour",
        "cuisine": "thailand"
    }}
    
    Now process this input: "{msg.text}"
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
    ctx.logger.info(f"LLM Response: {result}")
    
    try:
        # Parse JSON response
        parsed = json.loads(result)
        summarized = Summarize(
            favour=parsed.get("favour", ""),
            time=parsed.get("time", ""),
            cuisine=parsed.get("cuisine", "")
        )
        await ctx.send(sender, summarized)
    except Exception as e:
        ctx.logger.error(f"Failed to parse response: {e}")


@action_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Action Agent started with address: {action_agent.address}")
    ctx.logger.info(f"Agent running on port 8001")
    
    # Auto-test: Send a message to itself after 3 seconds
    import asyncio
    await asyncio.sleep(3)
    
    # Test the agent with sample input
    test_input = Input(text="I want to make spicy Japanese food under 20 minutes")
    ctx.logger.info("🧪 Testing agent with sample input...")
    await ctx.send(action_agent.address, test_input)


@action_agent.on_message(model=Summarize)
async def receive_summary(ctx: Context, sender: str, msg: Summarize):
    """Receive the summarized response"""
    print("\n" + "="*60)
    print("✅ TEST RESULT - SUMMARIZATION COMPLETE!")
    print("="*60)
    print(f"📝 Favour:  {msg.favour}")
    print(f"⏰ Time:    {msg.time}")
    print(f"🍱 Cuisine: {msg.cuisine}")
    print("="*60 + "\n")
    ctx.logger.info(f"Test completed successfully!")


if __name__ == "__main__":
    action_agent.run()

