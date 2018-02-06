import os
import time
import re
import random
from slackclient import SlackClient


slack_client = SlackClient(os.environ.get('THINKBOT_ACCESS_TOKEN'))
thinkbot_id = "B94NAGFU3"

# Constants
RTM_READ_DELAY = 1 # 1 second delay
EXAMPLE_COMMAND = "Do"
MENTION_REGEX = ".+"

def check_message(message,regex):
    match = re.match(regex, message)
    if match is not None:
        return True
    return False

def handle_message(channel):
    responses = [":thinking_face:",":thaenkin:",":thonk:",":fronk:",":mcthonk:",
    ":cog:",":lab6:"]
    response = random.choice(responses)
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response
    )

if __name__ == "__main__":
    regex = "The definition of .*"
    if slack_client.rtm_connect(with_team_state=False):
        print("Thinkbot connected and running!")
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            events = slack_client.rtm_read()
            for event in events:
                isSelf = False
                if "bot_id" in event:
                    isSelf = event["bot_id"]==thinkbot_id
                if event["type"] == "message" and not isSelf:

                    channel = event["channel"]
                    check = check_message(event["text"],regex)
                    check_rust = check_message(event["text"], ".*[r|R]ust.*")
                    if check:
                        handle_message(channel)
                    if check_rust:
                        slack_client.api_call(
                            "chat.postMessage",
                            channel=channel,
                            text=":thinkrust:"
                        )

            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
