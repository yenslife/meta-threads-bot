from agents import Agent
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

from dotenv import load_dotenv
from meta_threads_bot.Context.basic import PostContent

load_dotenv()


# TODO: 網路搜尋 or 資料檢索


agent = Agent[PostContent](
    name="Copywriting Agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    你是 Copywriting Agent，負責撰寫貼文的 Agent
    你將根據需求撰寫貼文，請提供貼文內容
    - 不要用 Markdown 語法
    - 可以用少量的表情符號來修飾
    - 請使用繁體中文 (台灣政體) 撰寫文案
    - 請使用激烈的口吻撰寫
    - 越吸引眼球越好""",
    model="gpt-4o-mini",
    handoff_description="負責撰寫貼文的 Agent",
)
