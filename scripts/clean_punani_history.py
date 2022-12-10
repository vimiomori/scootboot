import csv
# absolute_path = os.path.dirname(os.path.abspath(__file__))
# file_path = absolute_path + '/chat_history/punani_history.txt'

PEOPLE = ["スコフリン Scott", "crista", "Tucker", "Baby Dp", "Viみお🐬⁩⁩"]

def main():
    contents = None
    with open("../chat_history/punani_history.txt", "r") as f:
        contents = f.read()
    lines = contents.split("\n")
    
    header = ["time", "who", "message"]
    with open("../chat_history/punani_history.csv", "w") as f:
        write = csv.writer(f)
        write.writerow(header)
        for l in lines:
            row = l.split("\t")
            if not (len(row) > 2 and row[1] in PEOPLE) or row[2] == "[Photo]":
                continue
            write.writerow(row)

# https://chatterbot.readthedocs.io/en/stable/examples.html
if __name__ == "__main__":
    main()