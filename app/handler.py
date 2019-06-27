import requests
import os
import json


END_POINT = "https://api.line.me/v2/bot/message/reply"
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
class Handler:

    def __init__(self, event):
        self.reply_token = event["replyToken"]
        self.event_type = event["type"]
        self.user_id = event["source"]["userId"]
    
    def handle(self):
        msg_body = json.dumps({
            "to": self.user_id,
            "messages": [
                {
                    "type":"text",
                    "text":"hello"
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

