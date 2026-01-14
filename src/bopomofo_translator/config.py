import os
import logging
from dataclasses import dataclass

@dataclass
class Config:
    HOTKEY: str = os.getenv("BOPOMOFO_HOTKEY", "ctrl+alt+v")
    GOOGLE_API_URL: str = os.getenv("GOOGLE_API_URL", "https://www.google.com/inputtools/request")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

config = Config()

def setup_logging():
    """Configures the logging system."""
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
