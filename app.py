from flask import Flask, jsonify, request, render_template

from ai.use_openai import generate_instruction_object
from ai.use_whisper import create_transcript
from ai.generate_pos import generate_pos
import ast
from pprint import pprint
import json
import pandas as pd

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route('/get_string')
def get_string():

    # get most recent instruction from the instruction log
    with open('instruction_log.txt', 'r') as f:
        lines = f.read().splitlines()
        last_line = lines[-1]

    print("instructions:")
    print(last_line)

    # encode the instructions from gpt instance
    # as object 
    inst = generate_instruction_object(last_line)
    print("instruction object:")
    print(inst)

    inst_dict = ast.literal_eval(inst)

    data = generate_pos(inst_dict)
    print("data: ")
    pprint(data)

    output = {
        "type": inst_dict['Object_Type'],
        "coords": [entry['positions'] for entry in data],
    }

    return output

@app.route('/get_string_t')
def get_string_t():
    """testing"""
    function_call_input = {
        'Object_Type': 'Tank',
        'StartLat': 51.4556,
        'StartLong': 7.0116,
        'EndLat': 50.7374,
        'EndLong': 7.0982,
    }

    data = generate_pos(function_call_input)

    test = {
        "type": function_call_input['Object_Type'],
        "coords": [entry['positions'] for entry in data],
        "color": "green"
    }

    return test

@app.route('/upload', methods=['POST'])
def upload():
    audio_data = request.files['audio_data']  # get audio data from the request
    audio_data.save('recorded_audio.wav')  # save the audio data
    create_transcript() # create the transcript 
    return jsonify({"message": "Audio saved successfully!"})

# instruction log
@app.route('/lines')
def lines():
    with open('instruction_log.txt', 'r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    return jsonify(lines)

if __name__ == '__main__':
    app.run(debug=True)