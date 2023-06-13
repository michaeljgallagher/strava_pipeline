import pytest
from utils.webhook import Message, post_to_webhook


def test_post_to_webhook(requests_mock):
    webhook_url = "https://example.com/webhook"
    requests_mock.post(webhook_url, status_code=204)
    message = "Test message"
    post_to_webhook(webhook_url, message)
    assert requests_mock.last_request.method == "POST"
    assert requests_mock.last_request.url == webhook_url
    assert requests_mock.last_request.json() == {"content": message}
    assert requests_mock.call_count == 1


def test_post_to_webhook_error(requests_mock):
    webhook_url = "https://example.com/webhook"
    requests_mock.post(webhook_url, status_code=500)
    message = "Test message"
    with pytest.raises(RuntimeError):
        post_to_webhook(webhook_url, message)


def test_message_success():
    num = 10
    ts = "2021-01-01"
    expected_output = "**✅ Successfully ran Strava pipeline. ✅**\n\nInserted `10` activities into `strava_etl_db.activities`.\nRecords also written to `2021-01-01.csv`."
    assert Message.success_message(num, ts) == expected_output


def test_message_no_records():
    expected_output = "⚠️ No new activities found on today's Strava pipeline run. ⚠️"
    assert Message.no_records_message() == expected_output


def test_message_error():
    ts = "2021-01-01"
    expected_output = "**❌ An error occurred when running the Strava pipeline. ❌**\n\nCheck logs located in `2021-01-01.log` for more details."
    assert Message.error_message(ts) == expected_output
