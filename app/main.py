from flask import Flask, request, abort
from linebot.exceptions import InvalidSignatureError
from handler import Handler

import os
import requests
import json

import base64
import hashlib
import hmac


app = Flask(__name__)

#環境変数取得
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

@app.route("/callback", methods=['POST'])
def callback():
    print(1)
    body = request.get_json()

    # get request body as text
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        print(2)
        hash = hmac.new(CHANNEL_SECRET.encode('utf-8'),
                        request.get_data(as_text=True).encode('utf-8'),
                        hashlib.sha256).digest()
        signature = base64.b64encode(hash)
        if signature != request.headers['X-Line-Signature']:
            raise InvalidSignatureError
        for event in json.loads(body["events"]):
            Handler.handle(event)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)