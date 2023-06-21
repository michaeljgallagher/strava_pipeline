import configparser
import logging
import os
import time
from collections import namedtuple
from datetime import datetime

import psycopg2

from strava_pipeline.utils.flatfile import save_to_csv
from strava_pipeline.utils.postgres import (
    get_most_recent,
    push_csv_to_postgres,
    push_last_start_date,
)
from strava_pipeline.utils.strava_api import (
    get_access_token,
    get_activities,
    get_start_date,
)
from strava_pipeline.utils.webhook import Message, post_to_webhook


def main():
    # Read config file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(current_dir, "pipeline.ini")
    parser = configparser.ConfigParser()
    parser.read(config_file_path)
    config = namedtuple("config", parser.sections())(
        **{
            section: namedtuple(section, options)(*parser[section].values())
            for section, options in (x for x in parser.items() if x[0] != "DEFAULT")
        }
    )

    output_dirs = config.output_dirs
    webhook_url = config.webhook.webhook_url

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
    logger.info("Strava pipeline started")

    try:
        # Connect to Postgres, get most recent activity time
        with psycopg2.connect(**config.postgres._asdict()) as conn:
            most_recent = get_most_recent(conn, "start_date_history", "last_start_date")
            logger.info(f"Fetching activities starting from: {most_recent}")

            # Get access token and fetch activities
            access_token = get_access_token(
                config.strava.client_id,
                config.strava.client_secret,
                config.strava.refresh_token,
            )
            activities = get_activities(access_token, most_recent)
            logger.info(f"Fetched {len(activities)} activities")

            # If no activities, post to webhook and exit
            if not activities:
                logger.warning("No new activities to process. Exiting.")
                post_to_webhook(webhook_url, Message.no_records_message())
                return

            # Save activities to flat file
            save_to_csv(
                activities,
                f"{output_dirs.csv}/{now}.csv",
                config.fields.raw_columns.split(", "),
                config.fields.csv_columns.split(", "),
            )
            logger.info(
                f"Saved {len(activities)} activities to {output_dirs.csv}/{now}.csv"
            )

            # Push activities to Postgres
            push_csv_to_postgres(conn, f"{output_dirs.csv}/{now}.csv", "activities")
            logger.info(
                f"Pushed {len(activities)} activities to strava_etl_db.activities"
            )

            # Push last start date to Postgres
            last_start_date = get_start_date(activities[-1])
            push_last_start_date(
                conn, last_start_date, "start_date_history", "last_start_date"
            )
            logger.info(f"Recorded {last_start_date} to history table.")

            # Post success message to webhook
            post_to_webhook(webhook_url, Message.success_message(len(activities), now))
            logger.info("Strava pipeline completed successfully")

    except Exception as e:
        logger.exception("An error occurred during Strava pipeline:\n" + str(e))
        post_to_webhook(webhook_url, Message.error_message(now))


if __name__ == "__main__":
    main()
