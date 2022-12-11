import csv
import pandas as pd
from datetime import datetime, timedelta
# absolute_path = os.path.dirname(os.path.abspath(__file__))
# file_path = absolute_path + '/chat_history/punani_history.txt'

PEOPLE = ["スコフリン Scott", "crista", "Tucker", "Baby Dp", "Viみお🐬⁩⁩"]
date_format = "%H:%M"

def process(df, writer):
    p = None
    record = {}
    for ind in df.index:
        s = dict(
            time=df['time'][ind],
            who=df['who'][ind],
            message=df['message'][ind]
        )
        if not p:
            p = s
            continue
        ptime, pwho, pmessage = p.values()
        stime, swho, smessage = s.values()
        pdt = datetime.strptime(ptime, date_format)
        sdt = datetime.strptime(stime, date_format)
        same_convo = sdt - pdt < timedelta(hours=1)
        # completed one prompt and response
        if record.get("prompt") and record.get("response") and pwho != swho:
            writer.writerow([record["prompt"], record["response"]])
            record = {}
        # start a new prompt and response if at a new convo
        if not same_convo:
            record["prompt"] = smessage
            p = s
            continue
        # if prompt and response is empty, start a new prompt and response
        if not record.get("prompt"):
            record["prompt"] = pmessage
        # if the same person is still writing the prompt, append the message to the prompt
        if not record.get("response") and pwho == swho:
            record["prompt"] = record.get("prompt") + "\n" + smessage
        # if a new person is responding, make the message the response
        if not record.get("response") and pwho != swho:
            record["response"] = smessage
        # if the same person is still wrinting the response, append the message to the response
        if record.get("response") and pwho == swho:
            record["response"] = record.get("response") + "\n" + smessage
        p = s

def main():
    with pd.read_csv('../chat_history/punani_history.csv', chunksize=900) as reader:
        with open("../training_data/training_data.csv", "w") as f:
            write = csv.writer(f)
            write.writerow(["prompt", "completion"])
            for chunk in reader:
                process(chunk, write)

if __name__ == "__main__":
    main()
