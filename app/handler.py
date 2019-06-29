import requests
import os
import json
import time
from random import randint


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
            reply = self._get_reply("default")
        if self.event_type == "follow":
            reply = self._get_reply(self._get_profile(self.user_id))
        self._reply(reply)

    def _reply(self, reply):
        if type(reply) == list:
            r = None
            for res in reply:
                r = self._send(res)
            return r
        else:
            return self._send(reply)

    # def _reply(self, msg):
    #     reply = self._get_reply(msg)
    #     self._send(reply)

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
            return res.json()["displayName"].encode('ascii', 'ignore').decode('ascii')
        else:
            print(res)
    
    def _get_reply(self, display_name):
        with open('app/response.json') as f:
            response = json.load(f)
        if display_name == "default":
            num_choices = len(response)
            choice = randint(0, num_choices)
            return response[display_name][choice]
        else:
            display_name = "スコフリン Scott"
            return response[display_name]
    
    def _construct_message(self, res):
        print(res)
        message = {"type": res["type"]}
        if res["type"] == "img":
            message["originalContentUrl"] = res["response"]
        else:
            message["text"] = res["response"]
        return message
