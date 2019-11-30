import os
import time
import slack
from messagehandler import MessageHandler
from comands import *
import requests
import zipfile
from PIL import Image, ImageDraw

bot_id = None


COMMANDS = {"hello", "help", "do"}    # добавить help, do
PICTURE_TYPES = {"png", "jpg"}



@slack.RTMClient.run_on(event='message')
def on_message(**payload):
    data = payload['data']
    print(data)
    channel_id = data['channel']
    web_client = payload['web_client']
    text = data.get('text', []).lower()


    if f'@{bot_id.lower()}' in text:
        parse_comand(text, data, bot_id, web_client, channel_id)



# получение url файла
#@slack.RTMClient.run_on(event='file_shared')
def on_file_sharing(**payload):
    data = payload['data']
    file_id = data['file_id']

    web_client = payload['web_client']
    file_inf = web_client.files_info(token=slack_token, file=file_id)['file']
    file_name = file_inf['name']
    file_type = file_inf['filetype']

    channel_id = data['channel_id']
    message_handler = MessageHandler(channel_id)

    url = file_inf['url_private_download']

    if file_type not in ARCH_TYPES:
        message = message_handler.get_filetype_error_message()

    else:
        change_file(download_file(url))
        response = web_client.files_upload(
            channels=channel_id,
            file="response.zip",
            file_type="zip",
            title="response.zip")
        assert response["ok"]
        message = message_handler.get_upload_file_message()

    web_client.chat_postMessage(**message)




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
            print('Exception:\n', traceback.format_exc())