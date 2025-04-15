from agents import Agent
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents import function_tool

from dotenv import load_dotenv

load_dotenv()


@function_tool(description_override="撰寫一篇文章，請提供貼文內容")
def copywriting(caption: str) -> str:
    return caption


# TODO: 網路搜尋 or 資料檢索


agent = Agent(
    name="Copywriting Agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    你是 Copywriting Agent，負責撰寫貼文的 Agent
    你將根據需求撰寫貼文，請提供貼文內容
    - 不要用 Markdown 語法
    - 可以用少量的表情符號來修飾
    - 請使用繁體中文 (台灣正體) 撰寫文案
    - 請使用激烈的口吻撰寫
    - 越吸引眼球越好
    - 不要有換行 (有換行可能導致貼文失敗)
    - 每次都要和使用者確認內容
    - 不要出現 tag""",
    model="gpt-4.1-mini",
    handoff_description="負責撰寫貼文的 Agent",
    tools=[copywriting],
)
