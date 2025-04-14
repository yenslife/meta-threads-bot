from agents import Agent, function_tool, RunContextWrapper
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

from dotenv import load_dotenv
from meta_threads_bot.Context.basic import PostContent

load_dotenv()


@function_tool(description_override="Copywriting, you can use this tool to copywriting")
def copywriting(
    context: RunContextWrapper[PostContent],
    caption: str,
) -> str:
    """Copywriting"""
    context.context.caption = caption
    return caption


agent = Agent[PostContent](
    name="Copywriting Agent",
    instructions=f"{RECOMMENDED_PROMPT_PREFIX}\n\n你將根據需求撰寫貼文，請提供貼文內容",
    model="gpt-4o-mini",
    handoff_description="負責撰寫貼文的 Agent",
    tools=[copywriting],
)
