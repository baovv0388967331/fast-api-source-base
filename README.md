## Coding convention

- [Pylint](https://pylint.pycqa.org/en/)
    - Check command: `pylint src/app src/tests`
- [Flake8](https://flake8.pycqa.org/en/)
    - Check command: `flake8 . --show-source --statistics`
- [Isort](https://pycqa.github.io/isort/)
    - Auto format command: `isort .`
    - Check command: `isort --check-only .`
- [Black](https://github.com/psf/black)
    - Auto format command: `black .`
    - Check command: `black --check .`

## Unittest
- Run test
    - Check command: `poetry run pytest ./`
- Coverage test
    - Check command: `pytest --cov=src --cov-report=term-missing`

