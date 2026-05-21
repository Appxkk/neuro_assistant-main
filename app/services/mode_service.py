import os
from dotenv import load_dotenv

load_dotenv()

_current_llm_mode = os.getenv("LLM_MODE", "local_parser")


def get_llm_mode() -> str:
    return _current_llm_mode


def set_llm_mode(mode: str) -> str:
    global _current_llm_mode

    allowed_modes = ["local_parser", "ollama"]

    if mode not in allowed_modes:
        raise ValueError("Недопустимый режим LLM")

    _current_llm_mode = mode
    return _current_llm_mode