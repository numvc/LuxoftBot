class MessageHandler:

    def __init__(self, channel):
        self.channel = channel
        self.botname = "lux_bot"
        self.timestamp = ""
        self.reaction_task_completed = False
        self.pin_task_completed = False

    def get_amount_files_error_message(self):
        return self.get_list_message("Error.", "Please attach only one file")

    def get_filetype_error_message(self):
        return self.get_list_message("Error.", "Please use .zip/.7z format")

    def get_upload_file_message(self):
        return self.get_list_message("Got it.", "I started to work with file. Wait...")

    def get_archive_without_picture_message(self):
        return self.get_list_message("Uppsyy.", "File doesn't have a picture!")

    def get_updated_file_message(self):
        return self.get_list_message("Done.", "Download updated file!")

    def get_no_such_command_message(self):
        return self.get_list_message("Upssyy...", "I dont know it. Write 'help'")

    def get_help_message(self, user):
        return self.get_blocks_message("Hi, " + user, "I can say hello and change your picture. " +
                                    "You should use my @'name' to communicate with me. " +
                                    "Attach an archive .zip/.7zip format with inner picture and " +
                                    "I will change color and size. Write help and I will remember my skills.")

    def get_message_hello(self, username):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.botname,
            "blocks": [
                {"type": "section", "text": {"type": "mrkdwn", "text": "Hello, " + username}},
            ],
        }

    def get_list_message(self, caption, text):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.botname,
            "blocks": [
                {"type": "section", "text": {"type": "mrkdwn", "text": caption+" "+text}}
            ],
        }

    def get_blocks_message(self, title, details):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.botname,
            "blocks": [
                {"type": "section", "text": {"type": "mrkdwn", "text": title}},
                {"type": "context", "elements": [{"type": "mrkdwn", "text": details}]},
            ],
        }

