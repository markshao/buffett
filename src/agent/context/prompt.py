import os
from agent.context.context import AgentContext
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate

prompt_fpath = os.path.join(os.path.dirname(__file__),"prompts","buffett_agent_prompt_template.txt")
prompt = PromptTemplate.from_file(template_file=prompt_fpath)

    

class PromptBuilder:
    SYSTEM_PROMPT = """
you are an experienced stock trader in the virtual world, you try to maximum the profit through buying and selling stocks

some constrains
- At the beginning , you have your personal accout with some money intialized
- The Stock Market support T+1 trade model
- You have an interested stock list, each time you can pick up one of them , decide whether to buy / sell / analyze it
- You can make many transactions per-day
- If you think you have nothing to do for today or the price of the stock dont change , dont forget call the function let the time pass to next trade date
- You can think before you make any action, but dont forget use the tool I provided to make the real transaction
"""

    @classmethod
    def next_prompt_msgs_v1(cls, ctx: AgentContext):
        messages = []
        messages.append(SystemMessage(content=cls.SYSTEM_PROMPT))
        messages.append(HumanMessage(content=ctx.model_dump_json(by_alias=True)))
        # append history llm messages
        messages.extend(ctx.llm_logs)
        messages.append(HumanMessage(content="what's your next thinking or action?"))
        return messages
    
    @classmethod
    def next_prompt_msgs_v2(cls, ctx: AgentContext):
        messages = []
        prompt_content = prompt.format(
            total_available_money = ctx.stockActCtx.total_available_money,
            stock_holding= ctx.stockActCtx.stock_holding,
            interested_stock_list = ctx.stockActCtx.interested_stock_list
        )
        messages.append(SystemMessage(content=prompt_content))
        # append history llm messages
        messages.extend(ctx.llm_logs)
        messages.append(HumanMessage(content="what's your next thinking or action?"))
        return messages
