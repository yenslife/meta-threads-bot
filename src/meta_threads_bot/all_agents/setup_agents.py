from meta_threads_bot.all_agents.master_agent import agent as master_agent
from meta_threads_bot.all_agents.posting_agent import agent as posting_agent
from meta_threads_bot.all_agents.copywriting_agent import agent as copywriting_agent

# 設定 handoffs
master_agent.handoffs = [posting_agent, copywriting_agent]
posting_agent.handoffs = [master_agent, copywriting_agent]
copywriting_agent.handoffs = [master_agent, posting_agent]

__all__ = ["master_agent", "posting_agent", "copywriting_agent"]
