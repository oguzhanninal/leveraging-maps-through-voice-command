import io
import openai
from decouple import config

import os

# base directory of the whole app
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_transcript():
    """
    creates a string transcript of the audio user-recorded audio using whisper
    """

    # connect to whisper
    client = openai.AzureOpenAI(
        api_key=config("WHISPER_API_KEY"),
        api_version="2024-06-01",
        azure_endpoint="https://teodo-m91b9nxu-eastus2.cognitiveservices.azure.com/",
    )

    # path to local .wav file
    # from the user-created recording
    local_audio_file_path = os.path.join(base_dir, 'recorded_audio.wav')

    # open local .wav file in binary mode
    with open(local_audio_file_path, "rb") as audio_file:
        # create BytesIO object from audio
        audio_bytes = audio_file.read()
        audio_file_io = io.BytesIO(audio_bytes)
        audio_file_io.name = "audio.wav"  # OpenAI API needs a filename with extension

        # transcribe
        transcript = client.audio.transcriptions.create(
            model="whisper",
            file=audio_file_io,
        )

    print("input transcript: " + transcript.text)
    # write to an instruction log 
    with open("instruction_log.txt", "a") as l_f:
        l_f.write(transcript.text + "\n")

    # return the transcription
    return transcript.text

if __name__== "__main__":
    create_transcript()