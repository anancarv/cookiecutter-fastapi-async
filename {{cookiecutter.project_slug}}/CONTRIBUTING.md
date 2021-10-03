# Development - Contributing

# Requirements
* [pre-commit][pre-commit]: For identifying code issues before submission to code review

## Developing

To start working on this project, here are some guidelines to set up your environment:
  1. `git clone https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_slug}}.git`
  2. `cd {{cookiecutter.project_slug}}`
  3. [Install poetry][poetry]
  4. Activate virtualenv`poetry shell`
  5. Install dependencies: `poetry install`
  6. Run `pre-commit install --install-hooks` to install [precommit hooks][pre-commit]

After having installed pre-commit, before each commit, pre-commit hooks are run to:
* Check code formatting
* Check code typing
* Find common security issues

## Tests

Start the stack & run tests with this command:
```Bash
./scripts/test-local.sh
```

Please, make sure to write tests for each feature you want to implement.

[pre-commit]: https://github.com/pre-commit/pre-commit
[poetry]: https://python-poetry.org/docs/#installation
