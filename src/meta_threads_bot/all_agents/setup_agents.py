from meta_threads_bot.all_agents.master_agent import agent as master_agent
from meta_threads_bot.all_agents.posting_agent import agent as posting_agent
from meta_threads_bot.all_agents.copywriting_agent import agent as copywriting_agent

from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel
from dotenv import load_dotenv

import os

load_dotenv()

# 設定 handoffs
master_agent.handoffs = [posting_agent, copywriting_agent]
posting_agent.handoffs = [master_agent, copywriting_agent]
copywriting_agent.handoffs = [master_agent, posting_agent]

# 設定 gemini
client = AsyncOpenAI(
    base_url=os.getenv("GEMINI_BASE_URL"),
    api_key=os.getenv("GEMINI_API_KEY"),
)

# 設定 gemini
master_agent.model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-001", openai_client=client
)
posting_agent.model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-001", openai_client=client
)
copywriting_agent.model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-001", openai_client=client
)

__all__ = ["master_agent", "posting_agent", "copywriting_agent"]
