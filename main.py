import configparser
import logging
import os
import time
from collections import namedtuple
from datetime import datetime

import psycopg2

from utils.flatfile import save_to_csv
from utils.postgres import get_most_recent, push_csv_to_postgres, push_last_start_date
from utils.strava_api import get_access_token, get_activities, get_start_date
from utils.webhook import Message, post_to_webhook

# Read config file
current_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_dir, "pipeline.ini")
parser = configparser.ConfigParser()
parser.read(config_file_path)
pg_config = namedtuple("pg_config", parser["postgres"].keys())(
    *parser["postgres"].values()
)
strava_config = namedtuple("strava_config", parser["strava"].keys())(
    *parser["strava"].values()
)
fields = namedtuple("fields", parser["fields"].keys())(*parser["fields"].values())
output_dirs = namedtuple("output_dirs", parser["output_dirs"].keys())(
    *parser["output_dirs"].values()
)
webhook_url = parser.get("webhook", "webhook_url")

# Get current time (UTC)
now = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

# Set up logging
os.makedirs(output_dirs.logs, exist_ok=True)
logging.Formatter.converter = time.gmtime
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(f"{output_dirs.logs}/{now}.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# Log start of the script
logger.info("Strava ETL pipeline started")

try:
    # Connect to Postgres, get most recent activity time
    conn = psycopg2.connect(
        database=pg_config.database,
        user=pg_config.username,
        password=pg_config.password,
        host=pg_config.host,
        port=pg_config.port,
    )
    most_recent = get_most_recent(conn, "start_date_history", "last_start_date")
    logger.info(f"Fetching activities starting from: {most_recent}")

    # Get access token and fetch activities
    access_token = get_access_token(
        strava_config.client_id,
        strava_config.client_secret,
        strava_config.refresh_token,
    )
    activities = get_activities(access_token, most_recent)
    logger.info(f"Fetched {len(activities)} activities")

    # If no activities, post to webhook and exit
    if not activities:
        logger.warning("No new activities to process. Exiting.")
        post_to_webhook(webhook_url, Message.no_records_message())
        exit()

    # Save activities to flat file
    save_to_csv(
        activities,
        f"{output_dirs.csv}/{now}.csv",
        fields.raw_columns.split(", "),
        fields.csv_columns.split(", "),
    )
    logger.info(f"Saved {len(activities)} activities to {output_dirs.csv}/{now}.csv")

    # Push activities to Postgres
    push_csv_to_postgres(conn, f"{output_dirs.csv}/{now}.csv", "activities")
    logger.info(f"Pushed {len(activities)} activities to strava_etl_db.activities")

    # Push last start date to Postgres
    last_start_date = get_start_date(activities[-1])
    push_last_start_date(conn, last_start_date, "start_date_history", "last_start_date")
    logger.info(f"Recorded {last_start_date} to history table.")

    # Close connection
    conn.close()
    logger.info("Closed connection to Postgres")

    # Post success message to webhook
    post_to_webhook(webhook_url, Message.success_message(len(activities), now))
    logger.info("Strava ETL pipeline completed successfully")

except Exception as e:
    logger.exception("An error occurred during Strava ETL pipeline:\n" + str(e))
    post_to_webhook(webhook_url, Message.error_message(now))
    raise e
