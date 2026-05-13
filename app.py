from phi.agent import Agent
from phi.tools.sql import SQLTools
from phi.model.groq import Groq
import chainlit as cl
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('GROQ_API_KEY')
db_url = os.getenv("DB_URL")  # ✅ Load once

def create_agent(db_url: str):
    sql_agent = Agent(
        tools=[SQLTools(db_url=db_url)],  
        model=Groq(id="openai/gpt-oss-120b", api_key=api_key),
        add_chat_history_to_messages=True,
        num_history_responses=3,
        description="You are a helpful AI agent that answers questions about the SQL database.",
        instructions=[
            "Answer SQL-related questions only.",
            "Include SQL query in response.",
            "Explain clearly.",
            "Give 3 practice questions (Easy, Medium, Hard)."
        ]
    )
    return sql_agent


@cl.on_chat_start
async def on_chat_start():
    sql_agent = create_agent(db_url)  # ✅ no need to ask user
    cl.user_session.set("agent", sql_agent)

    await cl.Message(
        content="✅ Connected to database! Ask your SQL questions."
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    try:
        agent = cl.user_session.get("agent")

        msg = cl.Message(content="")
        for chunk in await cl.make_async(agent.run)(message.content, stream=True):
            await msg.stream_token(chunk.get_content_as_string())

        await msg.send()

    except Exception as e:
        await cl.Message(content=f"❌ Error: {e}").send()
