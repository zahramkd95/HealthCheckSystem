import logging 

#Adding logger to post to console ouptut with clear timestamps, levels and messages. 

logging.basicConfig(
    level=logging.INFO,  # Minimum level to log 
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    handlers=[logging.StreamHandler()]  # Stream handler to post in console
)
