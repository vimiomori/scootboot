import requests
import os
import json
import time


END_POINT = "https://api.line.me/v2/bot/message/reply"
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
class Handler:

    def __init__(self, event):
        self.event = event
        self.event_type = event["type"]
        self.user_id = event["source"]["userId"]
    
    def handle(self):
        if self.event_type == "unfollow":
            return
        else:
            self.reply_token = self.event["replyToken"]
        if self.event_type == "message":
            self._reply(self.event["message"]["text"])
        if self.event_type == "follow":
            self._greet()

    def _greet(self):
        custom_res = self._get_custom_res(self._get_profile(self.user_id)["displayName"])
        message = self._construct_message(custom_res)
        self._send(custom_res)

    def _reply(self, msg):
        reply = self._get_reply(msg)
        self._send(reply)

    def _send(self, custom_res):
        msg_body = json.dumps({
            "replyToken": self.reply_token,
            "messages": [self._construct_message(custom_res)]
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
        with open('app/response.json') as f:
            nicknames = json.load(f)
        return nicknames[display_name]
    
    def _construct_message(self, res):
        message = {"type": res.type}
        if res.type == "img":
            message["originalContentUrl"] = res.response
        else:
            message["message"] = res.response
        return message
