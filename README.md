__HealthCheckSystem Setup Instructions__

Before reading further, it is highly recommended to use a virtual environment (venv). Please read the following [guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) for setup and activation based on your operating system. 

Please note. All of the commands listed are relative to the root folder.

*__Step 1:__*  Install requirements 

    pip install -r requirements.txt

*__Step 2:__*  Make sure to run the following command to run the health check 

    python main.py /path/to/config.yaml

  For example:

    python main.py sample_input/sample_input_yaml


> **_NOTE:_**  If you would like to run this command against a sample yaml, two seperate yaml files are added to the `sample_input` folder [sample_input_yaml and sample_input_2_yaml]

*Expected Sample output for `sample_input_yaml`*
```
2025-03-23 23:18:39,233 - INFO - main.py - 99 - fetch.com has 67% availability percentage
2025-03-23 23:18:39,233 - INFO - main.py - 99 - www.fetchrewards.com has 0% availability percentage
2025-03-23 23:18:39,233 - INFO - main.py - 101 - --- Retrying in 15 seconds... ---
2025-03-23 23:18:55,520 - INFO - main.py - 99 - fetch.com has 67% availability percentage
2025-03-23 23:18:55,520 - INFO - main.py - 99 - www.fetchrewards.com has 0% availability percentage
2025-03-23 23:18:55,520 - INFO - main.py - 101 - --- Retrying in 15 seconds... ---
2025-03-23 23:19:11,429 - INFO - main.py - 99 - fetch.com has 67% availability percentage
2025-03-23 23:19:11,430 - INFO - main.py - 99 - www.fetchrewards.com has 33% availability percentage
2025-03-23 23:19:11,430 - INFO - main.py - 101 - --- Retrying in 15 seconds... ---

```

*Expected Sample output for `sample_input_2_yaml`*

```
2025-03-23 23:19:53,749 - INFO - main.py - 99 - dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com has 25% availability percentage
2025-03-23 23:19:53,749 - INFO - main.py - 101 - --- Retrying in 15 seconds... ---
2025-03-23 23:20:10,345 - INFO - main.py - 99 - dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com has 25% availability percentage
2025-03-23 23:20:10,346 - INFO - main.py - 101 - --- Retrying in 15 seconds... ---
2025-03-23 23:20:27,234 - INFO - main.py - 99 - dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com has 25% availability percentage
```

__Testing & Development Instructions__

- To run unit tests, you can run the follow command:

    `python test_main.py`


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
