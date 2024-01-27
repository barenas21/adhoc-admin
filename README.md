# adhoc-admin
This is a repo for the adhoc-admin app that will help engineers properly queue up asks and create the appropriate resources.

# dependencies
- Slack App token
- Slack bot token
- Jira token

# steps

## set up Slack app
- Create a new Slack app
- Enable Socket Mode
- Configure App-Level tokens as SLACK_APP_TOKEN
    - connections:write
    - Use token as App Token
- Configure Bot tokens
    - Use OAuth bot token as SLACK_BOT_TOKEN
- Setup slash commands
    - /request
- Enable Event Subscriptions
    - Subscribe to bot events
        - app_mention:read
        - channels:history
        - group:history
        - im:history
        - mpimi:history
- Enable 'Allow users to send Slash commands and messages from the messages tab' under App Home.

Set up your Jira Kanban board and create custom fields for an urgency dropdown and a business impact paragraph field.

# code breakdown

## Initialization and Configuration:

Import necessary modules and libraries.
Load environment variables using dotenv.
Initialize the Slack app with the bot token.
Set up the Jira client with server details and authentication.

## Slack Event Handlers:

@app.message(":wave:"): Responds to messages containing the wave emoji.
@app.event("app_mention"): Handles events where the app is mentioned.
@app.event("message"): Handles all message events for logging or additional processing.

## Slack Command Handling:

@app.command("/request"): Triggers on the /request command and opens a modal for user input.

## Modal Management:

def open_modal(...): Defines and opens a modal in response to the /request command. This modal collects user input like the request, urgency, and business impact.

## User Information Retrieval:

def get_slack_user_info(...): Fetches the Slack user's real name or username.
def get_slack_user_email(...): Retrieves the email address of the Slack user.

## Mapping Slack User to Jira Reporter:

def map_email_to_jira_username(...): Converts the Slack user's email to a Jira username format.

## Handling Modal Submission and Jira Issue Creation:

@app.view("modal-identifier"): Processes the user's input from the modal submission. It generates a formatted request ID and creates a Jira issue with the relevant details. It also posts a summary of the request back to the Slack channel.

## Error Handling:

Various try-except blocks to handle potential errors from Slack and Jira API calls, and to log these errors for debugging.

## App Execution:

The final section checks if the script is the main program and starts the app in Socket Mode.

Each section is responsible for handling specific aspects of the app, from initialization and event listening to user interaction and external API integrations. This structure helps keep the code organized and makes it easier to manage and debug.