from messagehandler import MessageHandler
import requests
import zipfile
import os
import re
from PIL import Image, ImageDraw

ARCH_TYPES = {"zip", "binary"}
slack_token = os.environ["SLACK_TOKEN"]
TO_SAVE_ARCH = "C:/All/LuxoftBot/"

#определяет тип команды
def  parse_comand(text, data, bot_id, web_client, channel_id):
    message_handler = MessageHandler(data['channel'])
    user = data['user']

    if ("hello" in text) and (f'@{bot_id.lower()}' in text):
        web_client.chat_postMessage(**message_handler.get_message_hello(user))

    if ("do" in text) and (f'@{bot_id.lower()}' in text):
        print("I found file")
        file_shared(data, web_client, message_handler, channel_id)

    if ("help" in text) and (f'@{bot_id.lower()}' in text):
        web_client.chat_postMessage(**message_handler.get_help_message(user))

    if ("help" not in text) and ("do" not in text) and ("hello" not in text): # изменить на свитч кейс
        web_client.chat_postMessage(**message_handler.get_no_such_command_message())

def file_shared(data, web_client, message_handler, channel_id):
    file_data = data['files']
    print(file_data)
    if len(file_data) == 1:
        file_id = file_data[0]['id']
        file_name = file_data[0]['name']
        file_type = file_data[0]['filetype']
        url_to_down = file_data[0]['url_private_download']
        if (file_type in ARCH_TYPES):
            web_client.chat_postMessage(**message_handler.get_upload_file_message())
            download_file(url_to_down, file_name)
            flag = change_file(file_name, web_client, message_handler)
            if flag == "true":
                send_file(web_client, channel_id)
                web_client.chat_postMessage(**message_handler.get_updated_file_message())
        else:
            web_client.chat_postMessage(**message_handler.get_filetype_error_message())
    else:
        web_client.chat_postMessage(**message_handler.get_amount_files_error_message())

# cкачивает архив
def download_file(url, file_name):
    request = requests.get(url, headers={'Authorization': 'Bearer %s' % slack_token})
    with open(TO_SAVE_ARCH+file_name, 'wb') as f:
        for chunk in request.iter_content():
            f.write(chunk)
    print("downloaded")

# извлекает картинку/и, изменяет(другими функциями), создает и заполняет новый архив
def change_file(filename, web_client, message_handler):
    if zipfile.is_zipfile(filename):
        z = zipfile.ZipFile(filename, 'r')                          # для чтения
        zw = zipfile.ZipFile(TO_SAVE_ARCH + "response.zip", 'w')    # для записи
        picture_names = []

        # извлекаем все картинки, если их несколько
        for info in z.infolist():
            if re.match(r'([.|\w|\s|-])*\.(?:jpg|gif|png)', info.filename):
                picture_names.append(info.filename)
                z.extract(info)
        if len(picture_names) == 0:
            web_client.chat_postMessage(**message_handler.get_archive_without_picture_message())
            return "false"
        # изменяем каждую картинку, сохраняя имя
        for current_picture in picture_names:
            resize_image(current_picture, current_picture, (256, 256))
            white_black(current_picture, current_picture)
            zw.write(current_picture)
        print("changed")
        z.close()
        zw.close()
        return "true"

    else:
        print("It's not ZIP!")
        return "false"


# изменяет картинку и сохраняет
def resize_image(input_image_path,
                 output_image_path,
                 size):
    original_image = Image.open(input_image_path)
    resized_image = original_image.resize(size)
    resized_image.show()
    resized_image.save(output_image_path)

# отправляет измененный файл
def send_file(web_client, channel_id):
    response = web_client.files_upload(
        channels=channel_id,
        file="response.zip",
        file_type="zip",
        title="response.zip")
    assert response["ok"]

# делает картинку черно-белой
def white_black(source_name, result_name):
    mode = 5
    image = Image.open(source_name)  # Открываем изображение.
    draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    pix = image.load()  # Выгружаем значения пикселей.

    if (mode == 5):
        factor = 80
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                S = a + b + c
                if (S > (((255 + factor) // 2) * 3)):
                    a, b, c = 255, 255, 255
                else:
                    a, b, c = 0, 0, 0
                draw.point((i, j), (a, b, c))

    image.save(result_name, "png")
    del draw