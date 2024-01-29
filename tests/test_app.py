import os
import unittest
from unittest.mock import patch, Mock
import responses

# Import the file/module that you want to test
from ./app import app


class TestSlackApp(unittest.TestCase):
    @responses.activate
    def test_handle_command(self):
        # Mock the environment variables that your app needs
        with patch.dict(os.environ, {"SLACK_BOT_TOKEN": "fake-token", "JIRA_SERVER": "fake-server", "JIRA_USER_EMAIL": "fake-email", "JIRA_API_TOKEN": "fake-token"}):
            # Mock the Slack API responses
            responses.add(
                responses.POST,
                "https://slack.com/api/views.open",
                json={"ok": True},
                status=200
            )
            responses.add(
                responses.POST,
                "https://slack.com/api/chat.postMessage",
                json={"ok": True},
                status=200
            )

            # Construct a fake request body similar to what Slack sends for a slash command
            fake_body = {
                "token": "verification_token",
                "team_id": "T1234567",
                "api_app_id": "A1234567",
                "command": "/request",
                "text": "test request",
                "user_id": "U1234567",
                "channel_id": "C1234567",
                "trigger_id": "123456789.987654321"
            }

            # Mock the logger to check if the correct info is being logged
            mock_logger = Mock()

            # Call the handle_command function with the mocked data
            app.handle_command(ack=lambda: None, body=fake_body, client=Mock(), logger=mock_logger)

            # Assert that the logger was called with the fake_body
            mock_logger.info.assert_called_with(fake_body)


if __name__ == "__main__":
    unittest.main()
