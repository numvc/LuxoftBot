import os
import time
import slack
from messagehandler import MessageHandler
from comands import *

bot_id = None

COMMANDS = {"hello", "help", "do"}
PICTURE_TYPES = {"png", "jpg"}

@slack.RTMClient.run_on(event='member_joined_channel')
def on_adiing_user(**payload):
    data = payload['data']
    web_client = payload['web_client']
    message_handler = MessageHandler(data['channel'])
    web_client.chat_postMessage(**message_handler.get_help_message(data['user']))

@slack.RTMClient.run_on(event='message')
def on_message(**payload):
    data = payload['data']
    print(data)
    channel_id = data['channel']
    web_client = payload['web_client']
    text = data.get('text', []).lower()

    if f'@{bot_id.lower()}' in text:
        parse_comand(text, data, bot_id, web_client, channel_id)

if __name__ == '__main__':
    isrun = False
    while True:
        try:
            slack_token = os.environ["SLACK_TOKEN"]
            rtm_client = slack.RTMClient(token=slack_token)
            slack_client = slack.WebClient(token=slack_token)
            bot_id = slack_client.api_call("auth.test")["user_id"]
            print("Bot started")
            isrun = True
            rtm_client.start()
        except TimeoutError:
            print("Server problems")
        except BaseException:
            print("Something wrong. Restarting")
