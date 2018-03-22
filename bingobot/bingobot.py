import os
import re
from slackclient import SlackClient


access_token = open("bingobot_access_token", 'r').readline()[:-1]
#slack_client = SlackClient(os.environ.get('BINGOBOT_ACCESS_TOKEN'))
slack_client = SlackClient(access_token)

HELP_FILE = "bingobot_help.txt"
RTM_READ_DELAY = 1 # 1 second delay

def execute_message(channel, message, regex):
    match = re.match(message, regex)
    if match is None:
        print("Error: not understood")
        return
    # Get groups

    # To make a new board: Take in name and array of bingo cards
    if match.group(1) == "makenew":
        make_new(match.group(2))

    if match.group(1) == "help":
        helpmessage = open(HELP_FILE, 'r').read()
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=helpmessage
        )

if __name__ == "__main__":
    print("access token: ", access_token)
    trigger = "!bingobot (.+)(.*)"

    if slack_client.rtm_connect(with_team_state=False):
        print("Bingobot Running!")
        while True:
            events = slack_client.rtm_read()
            for event in events:
                #isSelf = False
                #if "bot_id" in event:
                #    isSelf = event["bot_id"]==thinkbot_id
                #if event["type"] == "message" and not isSelf:
                if event["type"] == "message":
                    channel = event["channel"]
                    check = execute_message(event["text"],trigger)

            time.sleep(RTM_READ_DELAY)
