import requests


def post_to_webhook(webhook_url: str, message: str) -> None:
    """
    Posts a message to a webhook URL.

    :param webhook_url: The URL of the webhook.
    :param message: The message to post.
    :raises RuntimeError: If there is an error posting the message.
    """
    res = requests.post(webhook_url, json={"content": message})
    if res.status_code != 204:
        raise RuntimeError(res.text)


class Message:
    """
    A class for creating messages related to the Strava pipeline.
    """

    @staticmethod
    def success_message(num: int, ts: str) -> str:
        """
        Returns a success message for the Strava pipeline.

        :param num: The number of activities inserted into the database.
        :param ts: The timestamp of the pipeline run.
        :return: The success message.
        """
        message = (
            "**✅ Successfully ran Strava pipeline. ✅**\n\n"
            + f"Inserted `{num}` activities into `strava_etl_db.activities`.\n"
            + f"Records also written to `{ts}.csv`."
        )
        return message

    @staticmethod
    def no_records_message() -> str:
        """
        Returns a message indicating that no new activities were found on today's Strava pipeline run.

        :return: The message.
        """
        message = "⚠️ No new activities found on today's Strava pipeline run. ⚠️"
        return message

    @staticmethod
    def error_message(ts: str) -> str:
        """
        Returns an error message for when an error occurred during the Strava pipeline.

        :param ts: The timestamp of the pipeline run.
        :return: The error message.
        """
        message = (
            "**❌ An error occurred when running the Strava pipeline. ❌**\n\n"
            + f"Check logs located in `{ts}.log` for more details."
        )
        return message
