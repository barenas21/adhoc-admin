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