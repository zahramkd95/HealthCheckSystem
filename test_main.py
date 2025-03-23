import unittest
from unittest.mock import patch, mock_open
import yaml
from main import load_config, check_health, monitor_endpoints
from logger import logging
import requests

#TestLoadConfig checks if load config is compatible and if it raises appropriate Exceptions
class TestLoadConfig(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="key: value")
    def test_load_config_success(self, mock_file):
        # Test successful loading of YAML file
        result = load_config("dummy_path.yaml")
        self.assertEqual(result, {"key": "value"})
        mock_file.assert_called_once_with("dummy_path.yaml", "r")

    @patch("builtins.open", side_effect=FileNotFoundError("FileNotFound"))
    @patch.object(logging, "error")
    def test_load_config_file_not_found(self, mock_log_error, mock_file):
        # Test when file is not found
        result = load_config("non_existent.yaml")
        self.assertIsNone(result)
        mock_log_error.assert_called_once_with(
            "An error occurred while loading the config: " + str(FileNotFoundError("FileNotFound"))
        )

    @patch("builtins.open", new_callable=mock_open, read_data="invalid_yaml: [")
    @patch.object(logging, "error")
    def test_load_config_invalid_yaml(self, mock_log_error, mock_file):
        # Test when YAML file has invalid content
        with patch("yaml.safe_load", side_effect=yaml.YAMLError("Invalid YAML content")):
            result = load_config("invalid.yaml")
            self.assertIsNone(result)
            mock_log_error.assert_called_once_with(
                "An error occurred while loading the config: "
                "Invalid YAML content"
            )


#TestCheckHealth checks behaviors for various latency and response code simulations
class TestCheckHealth(unittest.TestCase):

    @patch("main.requests.request")
    def test_check_health_up(self, mock_request):
        # Test when the endpoint is UP
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        endpoint = {"url": "http://example.com", "method": "GET"}
        with patch("time.time", side_effect=[0, 0.3]):  # Simulate latency of 300ms
            result = check_health(endpoint)
            self.assertEqual(result, "UP")


    @patch("main.requests.request")
    def test_check_health_down_due_to_status_code(self, mock_request):
        # Test when the endpoint is DOWN due to status code
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 500
        mock_request.return_value = mock_response

        endpoint = {"url": "http://example.com", "method": "GET"}
        with patch("time.time", side_effect=[0, 0.3]):  # Simulate latency of 300ms
            result = check_health(endpoint)
            self.assertEqual(result, "DOWN")


    @patch("main.requests.request")
    def test_check_health_down_due_to_latency(self, mock_request):
        # Test when the endpoint is DOWN due to high latency
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        endpoint = {"url": "http://example.com", "method": "GET"}
        with patch("time.time", side_effect=[0, 1]):  # Simulate latency of 1000ms
            result = check_health(endpoint)
            self.assertEqual(result, "DOWN")

    @patch("main.requests.request", side_effect=requests.RequestException)
    def test_check_health_down_due_to_exception(self, mock_request):
        # Test when the endpoint is DOWN due to a RequestException
        endpoint = {"url": "http://example.com", "method": "GET"}
        result = check_health(endpoint)
        self.assertEqual(result, "DOWN")

#TestMonitorEndpoints checks if availability % is accurate for each domain
class TestMonitorEndpoints(unittest.TestCase):
    
    @patch("main.load_config")
    @patch("main.check_health")
    @patch("main.logging.info")
    @patch("main.time.sleep", side_effect=KeyboardInterrupt)  # Simulate stopping the loop
    def test_monitor_endpoints(self, mock_sleep, mock_log_info, mock_check_health, mock_load_config):
        # Mock a variation of configuration data with multiple methods and endpoints
        mock_load_config.return_value = [
            {"url": "http://example.com/careers", "method": "GET"},
            {"url": "http://test.com", "method": "GET"},
            {"url": "http://example.com", "method": "GET"},
            {"url": "http://test.com/testing", "method": "POST"},
            {"url": "http://test.com/somemoretesting", "method": "POST"},
        ]

        # Mock different health check results
        mock_check_health.side_effect = ["UP", "DOWN", "DOWN", "UP", "UP"]

        # Call the function `monitor_endpoints`
        with self.assertRaises(KeyboardInterrupt):  # Simulate user stopping the loop
            monitor_endpoints("dummy_path.yaml")

        # Verify load_config was called with the correct file path
        mock_load_config.assert_called_once_with("dummy_path.yaml")

        # Verify check_health was called for each endpoint
        mock_check_health.assert_any_call({"url": "http://example.com/careers", "method": "GET"})
        mock_check_health.assert_any_call({"url": "http://test.com", "method": "GET"})
        mock_check_health.assert_any_call({"url": "http://example.com", "method": "GET"})
        mock_check_health.assert_any_call({"url": "http://test.com/testing", "method": "POST"})
        mock_check_health.assert_any_call({"url": "http://test.com/somemoretesting", "method": "POST"})

        # Verify logging of availability percentages with correct domain names
        mock_log_info.assert_any_call("example.com has 50% availability percentage")
        mock_log_info.assert_any_call("test.com has 67% availability percentage")

        # Verify retry message was logged
        mock_log_info.assert_any_call("--- Retrying in 15 seconds... ---")


if __name__ == "__main__":
    unittest.main()