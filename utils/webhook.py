import requests


def post_to_webhook(webhook_url, message):
    """
    Posts a message to a webhook URL.

    :param webhook_url: The URL of the webhook.
    :type webhook_url: str
    :param message: The message to post.
    :type message: str
    :raises RuntimeError: If there is an error posting the message.
    """
    res = requests.post(webhook_url, json={"content": message})
    if res.status_code != 204:
        raise RuntimeError(res.text)


class Message:
    @staticmethod
    def success_message(num, ts):
        message = (
            "**✅ Successfully ran Strava ETL pipeline. ✅**\n\n"
            + f"Inserted `{num}` activities into `strava_etl_db.activities`.\n"
            + f"Records also written to `{ts}.csv`."
        )
        return message

    @staticmethod
    def no_records_message():
        message = "⚠️ No new activities found on today's Strava ETL run. ⚠️"
        return message

    @staticmethod
    def error_message(ts):
        message = (
            "**❌ An error occurred during Strava ETL pipeline ❌**\n\n"
            + f"Check logs located in `{ts}.log` for more details."
        )
        return message
