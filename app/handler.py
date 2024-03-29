import requests
import os
import json
import time
from random import randint
from openai_bot.bot import get_response


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
            reply = self._get_reply()
        if self.event_type == "follow":
            reply = self._get_follow_reply(self._get_profile(self.user_id))
        self._send(reply)

    def _send(self, reply):
        if type(reply) != list:
            reply = [reply]
        msg_body = json.dumps({
            "replyToken": self.reply_token,
            "messages": [self._construct_message(r) for r in reply]
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
    
    def _get_reply(self):
        prompt = self.event["message"]["text"]
        return get_response(prompt)

    def _get_follow_reply(self, display_name):
        with open('app/response.json') as f:
            response = json.load(f)
        if display_name == "default":
            num_choices = len(response)
            choice = randint(0, num_choices-1)
            return response[display_name][choice]
        else:
            return response[display_name]
    
    def _construct_message(self, res):
        message = {"type": res["type"]}
        if res["type"] == "image":
            message["originalContentUrl"] = res["response"]
            message["previewImageUrl"] = res["response"]
        elif self.event_type == "message" and self.event["message"]["text"].split("!")[0].lower() == "bust a nut":
            message["text"] = "なんだ、想ちゃんじゃん"
        else:
            message["text"] = res["response"]
        return message
