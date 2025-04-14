from dotenv import load_dotenv
from agents import (
    Agent,
    set_tracing_disabled,
)
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

from meta_threads_bot.Context.basic import PostContent

load_dotenv()

set_tracing_disabled(disabled=True)

agent = Agent[PostContent](
    name="Master Agent",
    instructions=f"{RECOMMENDED_PROMPT_PREFIX}\n\n負責 Threads 網軍行動的總召。你總是用台灣人習慣的繁體中文回答。可以讓 Copywriting Agent 撰寫文案，準備好了就可以給 Posting Agent 發文",
    model="gpt-4o-mini",
    handoff_description="負責與使用者確認需求的 Agent",
)
