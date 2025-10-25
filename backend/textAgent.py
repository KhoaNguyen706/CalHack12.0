from uagents import Agent, Context, Model
from typing import List
import asyncio

# Import your message models from agents.py
class InputForAction(Model):
    text: str
    ingredients: List[str]

# Create a test agent
test_agent = Agent(
    name="test_agent",
    seed="test agent seed phrase",
    port=8010,
    endpoint=["http://127.0.0.1:8010/submit"],
)

@test_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"🧪 Test Agent Address: {test_agent.address}")
    ctx.logger.info("Waiting 5 seconds before sending test message...")
    await asyncio.sleep(5)
    
    # Send test message to Action Agent
    ACTION_AGENT_ADDRESS = "agent1qfa5mjk0f7rl24f5v9fa3fampa4kc724cl6wxa6s52x62q07v7emsqhxc4p"  # Replace with your action agent address
    
    test_message = InputForAction(
        text="I want to make spicy Thai food in 30 minutes",
        ingredients=["chicken", "rice", "chili", "garlic", "onion", "coconut milk"]
    )
    
    ctx.logger.info(f"📤 Sending test message to Action Agent...")
    ctx.logger.info(f"   Text: {test_message.text}")
    ctx.logger.info(f"   Ingredients: {test_message.ingredients}")
    
    await ctx.send(ACTION_AGENT_ADDRESS, test_message)
    ctx.logger.info("✅ Test message sent!")

if __name__ == "__main__":
    test_agent.run()