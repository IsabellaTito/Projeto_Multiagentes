import logging
from typing import Any, Dict

from langchain_core.callbacks import BaseCallbackHandler


logger = logging.getLogger("agent_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(
    "historico_agente.log",
    encoding="utf-8"
)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)



class AgentLogger(BaseCallbackHandler):

    # =====================================================
    # AGENTE
    # =====================================================

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> None:
        logger.info(f"[CHAIN START] Inputs: {inputs}")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        logger.info(f"[CHAIN END] Outputs: {outputs}")

    def on_chain_error(self, error: BaseException, **kwargs: Any) -> None:
        logger.error(f"[CHAIN ERROR] {error}")

    # =====================================================
    # TOOL
    # =====================================================

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any) -> None:
        tool_name = serialized.get("name", "unknown_tool")

        logger.info(
            f"[TOOL START] "
            f"Tool={tool_name} "
            f"Input={input_str}"
        )

    def on_tool_end(self, output: Any, **kwargs: Any) -> None:
        logger.info(f"[TOOL END] Output={output}")

    # =====================================================
    # AGENT ACTIONS
    # =====================================================

    def on_agent_action(self, action, **kwargs: Any) -> Any:
        logger.info(
            f"[AGENT ACTION] "
            f"Tool={action.tool} "
            f"Input={action.tool_input}"
        )

    def on_agent_finish(self, finish, **kwargs: Any) -> None:
        logger.info(
            f"[AGENT FINISH] "
            f"Output={finish.return_values}"
        )

        logger.info("-" * 80)

    # =====================================================
    # LLM
    # =====================================================

    def on_llm_start(self, serialized, prompts, **kwargs):
        logger.info(f"[LLM START] Prompts={prompts}")

    def on_llm_end(self, response, **kwargs):
        logger.info(f"[LLM END]")

    def on_llm_error(self, error, **kwargs):
        logger.error(f"[LLM ERROR] {error}")

    # =====================================================
    # STREAMING
    # =====================================================

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(token, end="", flush=True)