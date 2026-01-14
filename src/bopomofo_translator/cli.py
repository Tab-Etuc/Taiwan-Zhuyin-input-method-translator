import argparse
import sys
import logging
from .core import BopomofoService
from .config import setup_logging

logger = logging.getLogger(__name__)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Bopomofo Translator CLI Tool",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        'text', 
        nargs='*', 
        help='The raw text input (e.g., "ji394su3"). If empty, starts interactive mode.'
    )
    
    parser.add_argument(
        '--local', '-l', 
        action='store_true', 
        help='Force offline mode (Shows Bopomofo symbols only).'
    )
    
    return parser.parse_args()

def interactive_session(use_local=False):
    mode_str = "OFFLINE" if use_local else "ONLINE"
    print(f"Bopomofo Translator Interactive Mode ({mode_str})")
    print("Type 'exit' to quit.")
    print("-" * 30)
    
    logger.debug(f"Starting interactive session in {mode_str} mode")

    while True:
        try:
            user_input = input("Input > ").strip()
            if user_input.lower() in ('exit', 'quit'):
                break
            
            if not user_input:
                continue

            if use_local:
                result = BopomofoService.local_decode(user_input)
            else:
                result = BopomofoService.online_translate(user_input)
            
            print(f"Output: {result}")
            
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            print(f"Error: {e}")

def main():
    setup_logging()
    args = parse_arguments()

    if args.text:
        # One-off command mode
        input_str = " ".join(args.text)
        logger.debug(f"Processing one-off input: {input_str}")
        
        if args.local:
            print(BopomofoService.local_decode(input_str))
        else:
            print(BopomofoService.online_translate(input_str))
    else:
        # Interactive mode
        interactive_session(use_local=args.local)

if __name__ == "__main__":
    main()
