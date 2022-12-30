# Rates Task

## Database Setup

We have provided a simple Docker setup for you, which will start a
PostgreSQL instance populated with the assignment data. You don't have
to use it, but you might find it convenient. If you decide to use
something else, make sure to include instructions on how to set it up.

You can execute the provided Dockerfile by running:

```bash
docker build -t ratestask .
```

This will create a container with the name _ratestask_, which you can
start in the following way:

```bash
docker run -p 0.0.0.0:5432:5432 --name ratestask ratestask
```

You can connect to the exposed Postgres instance on the Docker host IP address,
usually _127.0.0.1_ or _172.17.0.1_. It is started with the default user `postgres` and `ratestask` password.

```bash
PGPASSWORD=ratestask psql -h 127.0.0.1 -U postgres
```

alternatively, use `docker exec` if you do not have `psql` installed:

```bash
docker exec -e PGPASSWORD=ratestask -it ratestask psql -U postgres
```

Keep in mind that any data written in the Docker container will
disappear when it shuts down. The next time you run it, it will start
with a clean state.

## Application Setup

1. Run `poetry install` to install the dependencies using poetry
2. Set the environment variables `FLASK_APP` and `FLASK_ENV` with the appropriate values based on the environment.
3. Also set the required environment variables that are required in the `config.py` file. Eg. `DATABASE_URI`
   For example, in a \*nix development environment following command can be used to set the environment variables.

```bash
export FLASK_APP=app:create_app('local')
export FLASK_DEBUG=true
export DATABASE_URI=<local-uri>
```

## Install pre-commit hooks

After cloning the repository, run the following command to install pre-commit hook. This automatically runs
[black](https://pypi.org/project/black/) and [flake8](https://flake8.pycqa.org/en/latest/) tools, which
perform code formatting. Make sure to add the formatted files to git again.

```
poetry run pre-commit install
```

## Starting the server

Start the flask server by running `flask run` from the terminal.

## Running Tests

`pytest` command can be used to run all the unit test cases.
