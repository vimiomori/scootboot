class Handler:

    def __init__(self, event):
        self.reply_token = event["replyToken"]
        self.event_type = event["type"]
        self.user_id = event["source"]["userId"]
    
    def handle():
        pass