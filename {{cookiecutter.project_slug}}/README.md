# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

<!-- toc -->

- [Requirements](#requirements)
- [Development](#development)
  * [Local development](#local-development)
  * [Tests](#tests)
  * [Migrations](#migrations)

<!-- tocstop -->

## Requirements

* Python 3.8+

## Development

### Local development

First, create a `.env` file with the following content:
```bash
POSTGRES_USER=<YOUR-POSTGRES-USER>
POSTGRES_PWD=<YOUR-POSTGRES-PWD>
POSTGRES_DB=<YOUR-DB-NAME>

LOGGING_LEVEL=INFO
```

Then, start the stack with Docker Compose:
```bash
# Build services
docker-compose build

# Create and start containers
docker-compose up -d
```

Now you can open your browser and interact with these URLs:
* Automatic interactive documentation with Swagger UI: http://localhost:8080/docs
* Alternative automatic documentation with ReDoc: http://localhost:8080/redoc
* Pgweb, PostgreSQL web administration: http://localhost:8081


### Tests

Start the stack & run tests with this command:

```Bash
./scripts/test-local.sh
```

If your stack is already up, you just want to run the tests, you can use:

```bash
docker-compose exec api /app/scripts/tests-start.sh
```

That `/app/scripts/tests-start.sh` script just calls `pytest` after making sure that the rest of the stack is running. If you need to pass extra arguments to `pytest`, you can pass them to that command and they will be forwarded.

For example, to stop on first error:

```bash
docker-compose exec api bash /app/scripts/tests-start.sh -x
```

#### Test Coverage

Because the test scripts forward arguments to `pytest`, you can enable test coverage HTML report generation by passing `--cov-report=html`.

To run the local tests with coverage HTML reports:

```Bash
sh ./scripts/test-local.sh --cov-report=html
```

To run the tests in a running stack with coverage HTML reports:

```bash
docker-compose exec api bash /app/scripts/tests-start.sh --cov-report=html
```

### Migrations

After changing a model (for example, adding a column), create a revision, e.g.:
```bash
docker-compose run api alembic revision --autogenerate -m "Add column last_name to User model"
```

After creating the revision, run the migration in the database (this is what will actually change the database):
```bash
$ docker-compose run api alembic upgrade head
```
