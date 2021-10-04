## Project Description

Imagine that this is the early days of Wave's history, and that we are prototyping a new payroll system API. A front end (that hasn't been developed yet, but will likely be a single page application) is going to use our API to achieve two goals:

1. Upload a CSV file containing data on the number of hours worked per day per employee
1. Retrieve a report detailing how much each employee should be paid in each _pay period_

All employees are paid by the hour (there are no salaried employees.) Employees belong to one of two _job groups_ which determine their wages; job group A is paid $20/hr, and job group B is paid $30/hr. Each employee is identified by a string called an "employee id" that is globally unique in our system.

Hours are tracked per employee, per day in comma-separated value files (CSV).
Each individual CSV file is known as a "time report", and will contain:

1. A header, denoting the columns in the sheet (`date`, `hours worked`,
   `employee id`, `job group`)
1. 0 or more data rows

In addition, the file name should be of the format `time-report-x.csv`,
where `x` is the ID of the time report represented as an integer. For example, `time-report-42.csv` would represent a report with an ID of `42`.

You can assume that:

1. Columns will always be in that order.
1. There will always be data in each column and the number of hours worked will always be greater than 0.
1. There will always be a well-formed header line.
1. There will always be a well-formed file name.

A sample input file named `time-report-42.csv` is included in this repo.

### API Responsibilities:

We've agreed to build an API with the following endpoints to serve HTTP requests:

1. An endpoint for uploading a file.

   - This file will conform to the CSV specifications outlined in the previous section.
   - Upon upload, the timekeeping information within the file must be stored to a database for archival purposes.
   - If an attempt is made to upload a file with the same report ID as a previously uploaded file, this upload should fail with an error message indicating that this is not allowed.

2. An endpoint for retrieving a payroll report structured in the following way:

   _NOTE:_ It is not the responsibility of the API to return HTML, as we will delegate the visual layout and redering to the front end. The expectation is that this API will only return JSON data.

   - Return a JSON object `payrollReport`.
   - `payrollReport` will have a single field, `employeeReports`, containing a list of objects with fields `employeeId`, `payPeriod`, and `amountPaid`.
   - The `payPeriod` field is an object containing a date interval that is roughly biweekly. Each month has two pay periods; the _first half_ is from the 1st to the 15th inclusive, and the _second half_ is from the 16th to the end of the month, inclusive. `payPeriod` will have two fields to represent this interval: `startDate` and `endDate`.
   - Each employee should have a single object in `employeeReports` for each pay period that they have recorded hours worked. The `amountPaid` field should contain the sum of the hours worked in that pay period multiplied by the hourly rate for their job group.
   - If an employee was not paid in a specific pay period, there should not be an object in `employeeReports` for that employee + pay period combination.
   - The report should be sorted in some sensical order (e.g. sorted by employee id and then pay period start.)
   - The report should be based on all _of the data_ across _all of the uploaded time reports_, for all time.

As an example, given the upload of a sample file with the following data:

   | date       | hours worked | employee id | job group |
   | ---------- | ------------ | ----------- | --------- |
   | 2020-01-04 | 10           | 1           | A         |
   | 2020-01-14 | 5            | 1           | A         |
   | 2020-01-20 | 3            | 2           | B         |
   | 2020-01-20 | 4            | 1           | A         |

A request to the report endpoint should return the following JSON response:

   ```json
   {
     "payrollReport": {
       "employeeReports": [
         {
           "employeeId": "1",
           "payPeriod": {
             "startDate": "2020-01-01",
             "endDate": "2020-01-15"
           },
           "amountPaid": "$300.00"
         },
         {
           "employeeId": "1",
           "payPeriod": {
             "startDate": "2020-01-16",
             "endDate": "2020-01-31"
           },
           "amountPaid": "$80.00"
         },
         {
           "employeeId": "2",
           "payPeriod": {
             "startDate": "2020-01-16",
             "endDate": "2020-01-31"
           },
           "amountPaid": "$90.00"
         }
       ]
     }
   }
   ```

We consider ourselves to be language agnostic here at Wave, so feel free to use any combination of technologies you see fit to both meet the requirements and showcase your skills. We only ask that your submission:

- Is easy to set up
- Can run on either a Linux or Mac OS X developer machine
- Does not require any non open-source software

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
