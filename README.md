# Strava pipeline

This pipeline downloads Strava activities using the Strava API, saves them to a CSV file, and pushes them to a Postgres database. The script is designed to be run periodically to keep the database up-to-date with the user's Strava activities.

The pipeline connects to the Postgres database using the `psycopg2` module and retrieves the most recent activity time from the `start_date_history` table. It then uses the Strava API to fetch activities starting from the most recent activity time. If there are no new activities to process, a message is posted to a webhook and the pipeline exits.

If there are new activities to process, they're saved to a CSV file to the output directory specified in the configuration file. The activities are then pushed to the Postgres database. The last start date is also recorded in the `start_date_history` table using the `push_last_start_date` function. This lets the pipeline know where to start the next time it's run.

Finally, a success message is posted to a webhook, indicating that the pipeline completed successfully. If an error occurs during runtime, the error is logged and posted to the webhook.

Overall, this pipeline provides a simple way to keep a Postgres database up-to-date with a user's Strava activities. By running the pipeline periodically, the database can be kept in sync with the user's activities without requiring manual intervention.

## Installation and usage

### Prerequisites

* Create a [Strava App](https://www.strava.com/settings/api)
* [Authorize](https://developers.strava.com/docs/authentication/#tokenexchange) a Strava user to obtain a `refresh_token`
* Ensure [Postgres](https://www.postgresql.org/download) is installed on the target machine
* Create an incoming webhook for alerts

### Installation

Clone this repository:

```bash
git clone https://github.com/michaeljgallagher/strava_pipeline && cd strava_pipeline
```

Start the PostgreSQL interactive terminal:

```bash
psql -U <user>
```

From within the Postgres CLI, create the database and necessary tables by calling `setup.sql`:

```text
\i ./strava_pipeline/sql/setup.sql
```

Exit out of psql, then create and activate a Python virtual environment:

```bash
python -m venv env && source env/bin/activate
```

Update `pipeline.ini` with PostgreSQL settings, Strava API credentials, webhook URL, and absolute paths for CSV outputs and logs. Once that's been updated, it's a good idea to change permissions on this file to read only:

```bash
chmod 400 pipeline.ini
```

With the virtual environment activated and from within the root `strava_pipeline` directory, install via the `setup.py` script:

```bash
pip install --upgrade pip && pip install .
```

### Usage

From here, the pipeline can be run manually by calling `stravapipeline` when the virtual environment is activated. To automate this process, a cron job can be created that points to this command in the virtual environment:

```bash
30 10 * * 1 /path/to/strava_pipeline/env/bin/stravapipeline
```

## TODO

* Support for other types of SQL databases (e.g. MySQL)
* Support for other types of webhook services (e.g. Slack, Teams)
* Support for other types of flatfile outputs (e.g. JSON, XML)
* Since the pipeline only ever looks forward in time, have another pipeline that can backfill/reconcile data from a specified start date
* Add another step to the pipeline that loads the data into a data warehouse (e.g. Snowflake, BigQuery)
* Data visualization using a BI tool (e.g. Tableau, Power BI)
