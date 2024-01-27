import os

from dotenv import load_dotenv
from slack_bolt import App


# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Listens to incoming slash commands "/adhoc-admin request"
@app.command("/adhoc-admin")
def handle_adhoc_admin(ack, body, logger):
    ack()
    logger.info(body)

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
