from loguru import logger
from langchain_core.messages import ToolMessage
from agent.context.context import AgentContext
from agent.context.prompt import PromptBuilder
from agent.llm import Llm
from agent.tools.func_call.call import FunctionCallEngine


class BuffetAgent:
    def __init__(self) -> None:
        self._ctx = AgentContext()
        self.__init_ctx_first_time()

        self._llm = Llm()
        self._fc_engine: FunctionCallEngine = FunctionCallEngine()
        self._fc_engine.initialize()

    def __init_ctx_first_time(self):
        from agent.tools.interest_stocks import interested_stock_list

        # update 关注股票列表
        self._ctx.stockActCtx.interested_stock_list = interested_stock_list()

    @property
    def ctx(self):
        return self._ctx

    @property
    def llm(self) -> Llm:
        return self._llm

    @property
    def fc_engine(self) -> FunctionCallEngine:
        return self._fc_engine

    def run_agent(self):
        while True:
            next_prompt_msgs = PromptBuilder.next_prompt_msgs(ctx=self.ctx)
            logger.info("当前持股状态 = {}", self.ctx.stockActCtx.stock_holding)
            llm_resp = self._llm.invoke_with_tools(
                messages=next_prompt_msgs,
                tools=self.fc_engine.tools_definitions().dict(),
            )

            self.update_ctx(llm_resp=llm_resp)

    def update_ctx(self, llm_resp):
        if llm_resp.tool_calls:  # FIXME 这里默认就一个 tool 被调用
            self.__update_ctx_with_funccall(llm_resp)
        elif llm_resp.content:
            self.__update_ctx_with_thinking(llm_resp)
        else:
            logger.warning("gpt dont response anything")

    def __update_ctx_with_funccall(self, llm_resp):
        self.ctx.llm_logs.append(llm_resp)
        for tool_call in llm_resp.tool_calls:
            mname = tool_call["name"]
            args = tool_call["args"]
            # update args
            kwargs = {"ctx": self.ctx}
            kwargs.update(args)

            ret = self.fc_engine.call_method_with_args(mname=mname, args=kwargs)
            logger.info("method={},result={}", mname, ret)
            self.ctx.llm_logs.append(
                ToolMessage(content=str(ret), tool_call_id=tool_call["id"])
            )

    def __update_ctx_with_thinking(self, llm_resp):
        logger.info(llm_resp.content)
        self.ctx.llm_logs.append(llm_resp)
