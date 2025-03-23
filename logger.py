import logging 

logging.basicConfig(
    level=logging.INFO,  # Minimum level to log
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
    handlers=[logging.StreamHandler()]  # Stream handler for console output
)