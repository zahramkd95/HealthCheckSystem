import time
from collections import defaultdict

import requests
import yaml

from logger import logging


# Function to load configuration from the YAML file
def load_config(file_path):
    """
    Loads a YAML configuration file and returns its contents as a dictionary.

    Args:
        file_path (str): The path to the YAML configuration file.

    Returns:
        dict: The contents of the YAML file as a dictionary.

    Raises:
        Exception: If an error occurs while loading the file, it logs the error message.
    """
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.error(f"An error occurred while loading the config: {e}")
        raise


# Function to perform health checks
def check_health(endpoint):
    """
    Checks the health of a given endpoint by making an HTTP request and evaluating
    the response status code and latency.

    Args:
        endpoint (dict): A dictionary containing the following keys:
            - 'url' (str): The URL of the endpoint to check.
            - 'method' (str, optional): The HTTP method to use (default is 'GET').
            - 'headers' (dict, optional): A dictionary of HTTP headers to include in the request.
            - 'body' (str, optional): The JSON encoded string body to include in request for POST/PUT.

    Returns:
        str: "UP" if the endpoint is healthy (status code is 2xx and latency is less than 500ms),
             otherwise "DOWN".
    """
    url = endpoint["url"]
    method = endpoint.get("method", "GET")
    headers = endpoint.get("headers", {})
    body = endpoint.get("body")

    try:
        start_time = time.time()
        response = requests.request(method, url, headers=headers, json=body)
        end_time = time.time()
        latency = round((end_time - start_time) * 1000)
        logging.debug(f"Response: {response} status code")
        logging.debug(f"Latency: {latency} ms")
        if (200 <= response.status_code < 300) and (latency < 500):
            return "UP"
        else:
            return "DOWN"
    except requests.RequestException:
        return "DOWN"


# Main function to monitor endpoints
def monitor_endpoints(file_path):
    """
    The function continuously checks and monitors the health of each endpoint in the configuration file.
    It calculates and logs the cumulative availability percentage for each domain.
    The process repeats every 15 seconds unless interrupted.

    Args:
        file_path (str): The path to the YAML configuration file containing endpoint details.

    Notes:
        - The config file should contain endpoint details in a format compatible with `load_config`.
        - The `check_health` function is used to determine the health status of each endpoint.
        - Availability % is calculated as the ratio of "up" responses to the total number of checks
          performed for each domain.
    """
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})  # To store availability count

    while True:
        for endpoint in config:
            domain = endpoint["url"].split("//")[-1].split("/")[0]
            result = check_health(endpoint)
            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

        # Log cumulative availability percentages
        for domain, stats in domain_stats.items():
            availability = round(100 * stats["up"] / stats["total"])
            logging.info(f"{domain} has {availability}% availability percentage")

        logging.info("--- Retrying in 15 seconds... ---")
        time.sleep(15)


# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        logging.error("Check your command! Is it `python monitor.py <config_file_path>`?")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        logging.info("\nMonitoring stopped by user.")
