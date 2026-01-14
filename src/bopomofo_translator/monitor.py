import time
import keyboard
import pyperclip
import logging
from .core import BopomofoService
from .config import config, setup_logging

logger = logging.getLogger(__name__)

def on_hotkey_action():
    """
    Triggered when hotkey is pressed.
    Reads clipboard, translates content, and replaces it via paste simulation.
    """
    try:
        original_text = pyperclip.paste()
        if not original_text:
            return

        logger.debug(f"Clipboard content detected: {original_text[:20]}...")

        # Prefer online translation for better accuracy
        translated_text = BopomofoService.online_translate(original_text)

        if translated_text == original_text:
            logger.debug("Translation skipped or failed.")
            return

        pyperclip.copy(translated_text)
        
        # Allow OS clipboard to update before pasting
        time.sleep(0.1) 
        keyboard.send('ctrl+v')
        
        logger.info(f"Replaced text: {translated_text[:20]}...")

    except Exception as e:
        logger.error(f"Runtime Error: {e}", exc_info=True)

def main():
    setup_logging()
    
    logger.info("Clipboard Service Started.")
    logger.info(f"Listening for hotkey: {config.HOTKEY}")
    print(f"Service running. Hotkey: {config.HOTKEY} | Press Ctrl+C to stop.")

    try:
        keyboard.add_hotkey(config.HOTKEY, on_hotkey_action)
        keyboard.wait()
    except KeyboardInterrupt:
        logger.info("Service stopped by user.")
    except Exception as e:
        logger.critical(f"Service crashed: {e}", exc_info=True)

if __name__ == "__main__":
    main()
