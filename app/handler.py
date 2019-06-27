import requests
import os
import json
import time


END_POINT = "https://api.line.me/v2/bot/message/reply"
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
class Handler:

    def __init__(self, event):
        self.event = event
        self.reply_token = event["replyToken"]
        self.event_type = event["type"]
        self.user_id = event["source"]["userId"]
    
    def handle(self):
        if self.event_type == "message":
            self._reply(self.event["message"]["text"])
        if self.event_type == "follow":
            self._greet()

    def _greet(self):
        user_profile = self._get_profile(self.user_id)
        display_name = user_profile["displayName"]
        custom_res = self._get_custom_res(display_name)
        self._send(custom_res)


    def _reply(self, msg):
        reply = self._get_reply(msg)
        self._send(reply)

    def _send(self, msg):
        msg_body = json.dumps({
            "replyToken": self.reply_token,
            "messages": [
                {
                    "type":"text",
                    "text":msg
                }
            ]
        })
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + CHANNEL_ACCESS_TOKEN
        }
        return requests.post(
            END_POINT,
            params={'access_token': CHANNEL_ACCESS_TOKEN},
            headers=headers,
            data=msg_body
        )
    
    def _get_profile(self, user_id):
        url = f'https://api.line.me/v2/bot/profile/{user_id}'
        header = {
            "Authorization": "Bearer " + CHANNEL_ACCESS_TOKEN
        }
        res = requests.get(url, headers=header, timeout=(0.3, 1))
        if res.status_code == 200:
            return res.json()
        else:
            print(res)
    
    def _get_reply(self, msg):
        if msg == "hello":
            return "fuck off"
        else:
            return "yeaaah, bebe"
    
    def _get_custom_res(self, display_name):
        if display_name == "Garcia":
            return "graaacie"
        if "Vi" in display_name:
            return "it's the Voo!"

