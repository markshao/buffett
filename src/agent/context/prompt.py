from ast import alias
from agent.context.context import AgentContext
from langchain_core.messages import HumanMessage, SystemMessage


class PromptBuilder:
    SYSTEM_PROMPT = """
you are an experienced stock trader, you try to maximum the profit through buying and selling stocks

some constrains
- At the beginning , you have your personal accout with some money intialized
- The Stock Market support T+1 trade model
- You have an interested stock list, each time you can pick up one of them , to decide whether to buy / sell / analyze it 
- You can make many transactions per-day
- You are in a virtual world , if you think you have nothing to do for today or the price of the stock dont change , dont forget call the function let the time pass to next trade date
"""

    @classmethod
    def next_prompt_msgs(cls, ctx: AgentContext):
        messages = []
        messages.append(SystemMessage(content=cls.SYSTEM_PROMPT))
        messages.append(HumanMessage(content=ctx.model_dump_json(by_alias=True)))
        # append history llm messages
        messages.extend(ctx.llm_logs)
        messages.append(HumanMessage(content="what's your next thinking or action?"))
        return messages
