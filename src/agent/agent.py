from dotenv import load_dotenv
from .llm import LlmClient

BUFFET_SYSTEM_PROMPT = """
You are a stock trader,you make profit through buy and sell stocks on the stock market.
Some contrains as following
- You have an stock account with initiate money, you can only use this money to buy stock
- You can't sell the stock just after you buy it on same day
- You have a interested stock list which refered from your friend Mark , you only buy the stock in this list
- If you think you have nothing to do today , just call the go_tomorrow function
"""


class BuffetAgent:
    def __init__(self) -> None:
        self._llm = LlmClient()

    def run_agent(self):
        while True:
            break


load_dotenv()
