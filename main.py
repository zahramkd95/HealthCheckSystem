import yaml
import requests
import time
from logger import logging
from collections import defaultdict


# Function to load configuration from the YAML file
def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.error(f"An error occurred while loading the config: {e}")

# Function to perform health checks
def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET')
    headers = endpoint.get('headers',{})
    body = endpoint.get('body')

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
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

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
        logging.info("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        logging.info("\nMonitoring stopped by user.")