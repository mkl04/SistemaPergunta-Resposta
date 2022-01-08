#
# Copyright 2018-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from flask import Flask, render_template, request, jsonify
from chatbot import get_question, end, get_opening_message
import json
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--port", default=8070)
args = parser.parse_args()

app = Flask(__name__)

# state that the conversation with the chatbot is in
states = {
    1: get_question,
    5: end
}


@app.route("/", methods=["POST", "GET", "HEAD"])
def chat():
    if request.method == "POST":
        # Process an ongoing conversation
        data = json.loads(request.data)
        input_text = data["input"]
        state = int(data["state"])

        # gets name of the next function based on state that conversation with chatbot is in
        get_next_text = states.get(state)
        response, new_state = get_next_text(input_text)

        return jsonify({"response": response, "state": new_state})

    else:
        # Start a conversation
        return render_template("index.html", display_text=get_opening_message(), state=1)


if __name__ == "__main__":
    app.run(port=args.port, debug=True, host='localhost')