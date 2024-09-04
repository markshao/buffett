from enum import Enum
from typing import List
from pydantic import BaseModel,Field

SYSTEM_PROMPT = """
you are an experienced stock trader, you try to maximum the profit through buying and selling stocks

some constrains
- At the beginning , you have your personal accout with some money intialized
- The Stock Market support T+1 trade model
- You have an interested stock list, each time you can pick up one of them , to decide whether to buy / sell / analyze it 
- You can make many transactions per-day
- If you think you have nothing to do for today, just wait for the next trade date
"""

class TransType(Enum):
    THINK = "think"
    FUNCTION_CALL = "function call"

class Transaction(BaseModel):
    type: TransType
    log: str

class TransactinoCtx(BaseModel):
    transactions: List[Transaction]

    def clear(self):
        self.transactions.clear()

class StatusPrompt(BaseModel):
    interested_stock_list: List[str]
    stock_account: None
    transactions: TransactinoCtx

    