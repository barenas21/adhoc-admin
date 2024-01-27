import os
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient  # Import WebClient here
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initializes your app with your bot token
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.message(":wave:")
def say_hello(message, say):
    user = message['user']
    say(f"Hi there, <@{user}>!")

@app.event("app_mention")
def handle_app_mention_events(body, logger):
    logger.info(body)

@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)

@app.command("/request")
def handle_command(ack, body, client, logger):
    try:
        ack()
        channel_id = body['channel_id']  # Capture the channel ID
        trigger_id = body['trigger_id']
        open_modal(client, trigger_id, channel_id, logger) # Listens to incoming commands via "request"
        logger.info(body)
    except Exception as e:
        logger.error(f"Error handling slash command: {e}")

def open_modal(client: WebClient, trigger_id: str, channel_id: str,logger):
    try:
        # Define the modal
        modal = {
            "type": "modal",
            "callback_id": "modal-identifier",
            "title": {"type": "plain_text", "text": "Adhoc Request"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "private_metadata": str(channel_id),  # Add channel_id to the modal's private metadata
            "blocks": [
                {
                    "type": "input",
                    "block_id": "request_block",
                    "element": {"type": "plain_text_input", "action_id": "request"},
                    "label": {"type": "plain_text", "text": "Request"}
                },
                {
                    "type": "input",
                    "block_id": "urgency_block",
                    "element": {
                        "type": "static_select",
                        "action_id": "urgency",
                        "options": [
                            {
                                "text": {"type": "plain_text", "text": "P1 - High urgency"},
                                "value": "P1"
                            },
                            {
                                "text": {"type": "plain_text", "text": "P2 - Medium urgency"},
                                "value": "P2"
                            },
                            {
                                "text": {"type": "plain_text", "text": "P3 - Low urgency"},
                                "value": "P3"
                            }
                        ]
                    },
                    "label": {"type": "plain_text", "text": "Urgency"}
                },
                {
                    "type": "input",
                    "block_id": "impact_block",
                    "element": {"type": "plain_text_input", "multiline": True, "action_id": "business_impact"},
                    "label": {"type": "plain_text", "text": "Business Impact"}
                }
            ]
        }
        client.views_open(trigger_id=trigger_id, view=modal)
    except SlackApiError as e:
        logger.error(f"Error opening modal: {e}")

request_counter = 0

@app.view("modal-identifier")
def handle_modal_submission(ack, body, client, logger):
    global request_counter
    ack()

    channel_id = body['view']['private_metadata']  # Retrieve the channel ID from private metadata

    # Extract submission data
    submission = body['view']['state']['values']
    request_text = submission['request_block']['request']['value']
    urgency = submission['urgency_block']['urgency']['selected_option']['value']
    business_impact = submission['impact_block']['business_impact']['value']
    user_id = body["user"]["id"]

    # Generate and format request ID
    request_counter = (request_counter + 1) % 1000
    request_id = f"{request_counter:03}"

    # Post the summary message to the same channel where the command was issued
    try:
        client.chat_postMessage(
            channel=channel_id,  # Use the captured channel ID
            text=f"Request ID: {request_id}\nUser: <@{user_id}>\nRequest: {request_text}\nUrgency: {urgency}\nBusiness Impact: {business_impact}"
        )
    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")

@app.command("/request")
def handle_command(ack, body, client, logger):
    try:
        ack()
        channel_id = body['channel_id']  # Capture the channel ID
        trigger_id = body['trigger_id']
        open_modal(client, trigger_id, channel_id, logger) # Listens to incoming commands via "request"
        logger.info(body)
    except Exception as e:
        logger.error(f"Error handling slash command: {e}")

# Start the app in Socket Mode
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()