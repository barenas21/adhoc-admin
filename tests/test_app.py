import os
import unittest
from unittest.mock import patch, Mock
import responses

# Import the file/module that you want to test
from app import app

class TestSlackApp(unittest.TestCase):

    @responses.activate
    def test_handle_adhoc_admin(self):
        # Mock the environment variables that your app needs
        with patch.dict(os.environ, {"SLACK_BOT_TOKEN": "fake-token", "SLACK_SIGNING_SECRET": "fake-secret"}):
            # Mock the /slack/events endpoint that Slack will call
            responses.add(
                responses.POST,
                "https://slack.com/api/slack/events",
                json={"ok": True},
                status=200
            )
            
            # Construct a fake request body similar to what Slack sends
            fake_body = {
                "token": "verification_token",
                "team_id": "T1234567",
                "api_app_id": "A1234567",
                "event": {
                    "type": "command",
                    "command": "/adhoc-admin",
                    "text": "request",
                    "user_id": "U1234567",
                    "channel_id": "C1234567",
                },
                "type": "event_callback",
                "event_id": "Ev1234567",
                "event_time": 1234567890
            }
            
            # Mock the logger to check if the correct info is being logged
            mock_logger = Mock()
            
            # Call the handle_adhoc_admin function with the mocked data
            app.handle_adhoc_admin(ack=lambda: None, body=fake_body, logger=mock_logger)
            
            # Assert that the logger was called with the fake_body
            mock_logger.info.assert_called_with(fake_body)

if __name__ == "__main__":
    unittest.main()
