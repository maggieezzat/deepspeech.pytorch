import argparse
import json
import os
import subprocess
import sys
import time
import warnings

import requests
import requests.exceptions
import torch

warnings.simplefilter("ignore")


if __name__ == "__main__":
    ALLOWED_EXTENSIONS = set(["wav", "mp3", "ogg", "webm"])
    parser = argparse.ArgumentParser(description="RT Remote transcription")
    parser.add_argument(
        "-a",
        "--audio-dir",
        help="Dir to audio files to predict on, the same in mic script",
    )
    parser.add_argument("-t", "--transcription", help="Transcription file")
    parser.add_argument(
        "--offsets",
        dest="offsets",
        action="store_true",
        help="Returns time offset information",
    )
    args = parser.parse_args()

    if args.audio_dir is None or args.transcription is None:
        parser.print_help()
        sys.exit()

    print("Starting")
    counter = 0
    s = "|"
    enter = False
    URL = "http://52.250.111.102:8888/transcribe"
    server = True
    while True:
        try:
            if server:
                try:
                    r = requests.get(URL)
                    server = False
                except requests.exceptions.ConnectionError:
                    print("Please Start the server")
                    time.sleep(10)
                    continue
            audio_files = [
                f
                for f in os.listdir(args.audio_dir)
                if os.path.isfile(os.path.join(args.audio_dir, f))
                and ((f.split(".")[1]).lower() in ALLOWED_EXTENSIONS)
            ]
            if len(audio_files) > 0:
                audio_file = audio_files[0]
                audio_path = os.path.join(args.audio_dir, audio_file)

                size1 = os.path.getsize(audio_path)
                time.sleep(1)
                size2 = os.path.getsize(audio_path)
                if size1 != size2:
                    continue

                try:
                    os.rename(audio_path, audio_path)
                    print("Reading file : " + audio_file)
                except OSError as e:
                    print('Access-error on file "' + audio_file + '"! \n' + str(e))
                    continue

                # suggested edit : use python requests lib instead
                try:
                    f = open(audio_path, "rb")
                    files = {"file": f}
                    response = requests.post(URL, files=files)

                except (
                    requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout,
                ):
                    print("Please Start the server")
                    time.sleep(3)
                    server = True
                    continue
                finally:
                    f.close()

                # response = json.loads(response.decode("utf-8", "ignore"))
                response = response.json()
                if response["status"] == "error":
                    print(response["message"])
                    continue
                elif response["status"] == "OK":
                    transcription = response["transcription"][0][0]
                else:
                    print("Well, that was not expected")
                    continue

                line = audio_file.split(".")[0] + " --> " + transcription + "\n"

                if not os.path.isfile(args.transcription):
                    if not os.path.isdir(args.transcription):
                        parser.print_help()
                        sys.exit()
                    args.transcription = os.path.join(
                        args.transcription, "transcription.txt"
                    )

                with open(args.transcription, "a") as the_file:
                    the_file.write(line)
                try:
                    os.remove(audio_path)
                except:
                    print("remove not working")
                print(transcription)
                print()
            else:
                if enter:
                    print()
                    enter = False
                if counter == 0 or counter == 4:
                    s = "|"
                elif counter == 1 or counter == 5:
                    s = "/"
                elif counter == 2 or counter == 6:
                    s = "-"
                elif counter == 3 or counter == 7:
                    s = "\\"
                print("Waiting for files " + s, end="\r")
                time.sleep(0.5)
                counter += 1
                if counter > 7:
                    counter = 0
        except:
            if counter == 0 or counter == 4:
                s = "|"
            elif counter == 1 or counter == 5:
                s = "/"
            elif counter == 2 or counter == 6:
                s = "-"
            elif counter == 3 or counter == 7:
                s = "\\"
            print("Please start the microphone script " + s, end="\r")
            time.sleep(0.5)
            counter += 1
            if counter > 7:
                counter = 0
            enter = True
