from fetchai.ledger.api import LedgerApi
from fetchai.ledger.identity import Identity
import json
from uagents import Agent, Context, Model
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Define message types
class InputMessage(Model):
    text: str

class ResponseMessage(Model):
    reply: str

# Create agent
chat_agent = Agent(
    name="chat_agent",
    seed="chat agent seed",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

@chat_agent.on_message(model=InputMessage)
async def handle_message(ctx: Context, sender: str, msg: InputMessage):

# Handle responses
@chat_agent.on_message(model=ResponseMessage)
async def show_response(ctx: Context, sender: str, msg: ResponseMessage):
    print("\n💬 AI Agent Reply:", msg.reply, "\n")

if __name__ == "__main__":
    chat_agent.run()