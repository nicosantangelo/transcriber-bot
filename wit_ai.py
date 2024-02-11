# pylint: disable=missing-module-docstring, missing-function-docstring
import os
from pydub import AudioSegment
from wit import Wit

API_ENDPOINT = "https://api.wit.ai/speech"


def main():
    token = os.environ["TOKEN"]
    client = Wit(token)

    ogg2wav("file_18.oga")

    resp = None
    with open("file_18.wav", "rb") as f:
        resp = client.speech(f, {"Content-Type": "audio/wav"})

    print("Yay, got Wit.ai response: " + str(resp))


def ogg2wav(ofn):
    wfn = ofn.replace(".oga", ".wav")
    x = AudioSegment.from_file(ofn)
    x.export(wfn, format="wav")


if __name__ == "__main__":
    main()
