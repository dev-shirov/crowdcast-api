import logging
from enum import Enum
from typing import Type, Dict
import regex as re


def enum2csv(clazz: Type[Enum], sep: str = ",") -> str:
    words = [str(item.value) for item in clazz]
    return sep.join(words)


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger

def field(pattern: str, text: str, key_name: str) -> Dict[str, list[str]]: 

    matches = re.findall(pattern, text)
    
    return {key_name: [match.split(":")[1] for match in matches]}
