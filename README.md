### Documentation:

#### Requirements

- Python 3.6
- pip3
- make
- virtualenv (or Docker)
- PostgreSQL (If running in production mode)


#### Environment Configuration

In order to make things easier for testing purposes, a file named `.env.template` has been provided at
the project root level, which contains all of the environment variables used by the project. Please
rename it to `.env` and update it with the values you want. The project will be using `python-dotenv` in order to translate the values in that file into the application as environment variables.

The difference between development (dev) and production (prod) modes, in the context of this project, is the type of database being used. If running in development mode, the project will be using SQLite, whereas
PostgreSQL will be used when running it in production mode.

That being said, if `prod` is the value specified for `$ENVIRONMENT`, then make sure PostgreSQL is properly setup and all the values for `$DB_` variables are set correctly. If you leave any value in the `.env` file empty, the corresponding default value will be used instead, which can be found in `app/constants/config.py`.

**Note:** Make sure the environment is properly configured before moving into the next step.

#### Setup: virtualenv

```shell
$ make setup && make run
```

The above does the equivalent of the following:
```shell
$ virtualenv -p python3.6 .venv
$ source .venv/bin/activate
$ pip install -r requirements/common.txt
$ ./scripts/run.sh
```

**Note:** The `virtualenv` setup assumes that you want to run the project in _development_ mode, thus installing the common requirements. If you want to run the project with `virtualenv` and `PostgreSQL`, install the requirements via:

```shell
$ pip install -r requirements/prod.txt
```
#### Setup: Docker
```shell
$ make docker-build && make docker-run
```

**Note:** The `docker` setup assumes that you want to run the project in _production_ mode.

### Questionnaire
* How did you test that your implementation was correct?
   I implemented unit tests to test both the report generation process and the processing of the .csv file, which were based on input-output comparisons between expectations based on the input value and the actual result (output) of the methods implemented.

* If this application was destined for a production environment, what would you add or change?
   In the context of implementing an application for the real-world, I would suggest at least the following adjustments:
  * Implement an authentication protocol (i.e. OAuth2);
  * Use a third-party tool to safeguard sensitive values for environment variables like `SECRET_KEY` and the DB connection specifications (i.e. AWS Secrets Manager);
  * Have the Database in a different server;
  * Deploy the application within clusters for better load management (i.e. AWS ECS).

* What compromises did you have to make as a result of the time constraints of this challenge?
  * I ended up spending a bit more time than initially intended because I wanted to deliver a well-organized, easy-to-setup project, with multiple levels of configuration. That being said, I used SQLite throughout the vast majority of development time in order to make up for the time spent with configuration and organizing the application;
  * I did not implement a proper DB migration integration between SQLAlchemy and Flask (i.e. Alembic);
  * I did not worry about data privacy;
