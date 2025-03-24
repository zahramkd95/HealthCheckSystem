import logging

# Adding logger to post to console o/p with clear timestamps,filenames, line numbers,levels and messages.

logging.basicConfig(
    level=logging.INFO,  # Minimum level to log
    format="%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s",  # Log format
    handlers=[logging.StreamHandler()],  # Stream handler to post in console
)
