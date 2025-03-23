__HealthCheckSystem Setup Instructions__

Before reading further, it is highly recommended to use a virtual environment (venv). Please read the following [guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) for setup and activation based on your operating system. 

*__Step 1:__*  Install requirements 

    pip install -r /path/to/requirements.txt

*__Step 2:__*  Make sure to run the following command to run the health check 

    python /path/to/main.py /path/to/config.yaml


> **_NOTE:_**  If you would like to run this command against a sample yaml, two seperate yaml files are added to the `sample_input` folder [sample_input_yaml and sample_input_2_yaml]

*Expected Sample output for `sample_input_yaml`*
```
2025-03-23 13:57:14,640 - INFO - fetch.com has 67% availability percentage
2025-03-23 13:57:14,640 - INFO - www.fetchrewards.com has 0% availability percentage
2025-03-23 13:57:14,640 - INFO - --- Retrying in 15 seconds... ---
2025-03-23 13:57:30,815 - INFO - fetch.com has 67% availability percentage
2025-03-23 13:57:30,815 - INFO - www.fetchrewards.com has 0% availability percentage
2025-03-23 13:57:30,815 - INFO - --- Retrying in 15 seconds... ---

```

*Expected Sample output for `sample_input_2_yaml`*

```
2025-03-23 13:56:16,466 - INFO - dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com has 25% availability percentage
2025-03-23 13:56:16,466 - INFO - --- Retrying in 15 seconds... ---
2025-03-23 13:56:33,179 - INFO - dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com has 25% availability percentage
2025-03-23 13:56:33,180 - INFO - --- Retrying in 15 seconds... --- 
```

__Testing & Development Instructions__

- To run unit tests, you can run the follow command:

    `python /path/to/test_main.py`


- Setup precommit hooks by installing pre-commit. This will set up the hooks so that black, flake8 and other formatting tools will run automatically on git commit (before committing any changes)

    `pre-commit install`

- If you want to run the hooks manually, run the following command:

    `pre-commit run --all-files`

*Expected output:*

```
black....................................................................Passed
flake8...................................................................Passed
isort....................................................................Passed
end-of-file-fixer........................................................Passed
trailing-whitespace-fixer................................................Passed
```