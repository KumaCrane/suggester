MAX_FOUND = 10
SUGGEST_FILE = "ruwords.txt"
SUGGESTER = None
DEBUG = True

from flask import Flask
from flask import request
app = Flask(__name__)

import json

class Suggester:
    def __init__(self, filename):
        with open(filename, encoding="utf-8") as f:
            self.words = list(f)

    def get(self, word):
        found = []
        for w in self.words:
            if w.startswith(word):
                found.append(w)
            if len(found) > MAX_FOUND:
                break
        return found


@app.route('/')
def suggest_handler():
    global SUGGESTER
    if SUGGESTER is None:
        SUGGESTER = Suggester(SUGGEST_FILE)

    w = request.args.get('w')
    found = SUGGESTER.get(w)
    return json.dumps(found, ensure_ascii=False), 200, {'Content-Type': 'text/json'}

if __name__ == '__main__':
    app.run(debug=DEBUG)