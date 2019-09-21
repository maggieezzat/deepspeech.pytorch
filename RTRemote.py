import argparse
import json
import os
import subprocess
import sys
import time
import warnings

import torch

warnings.simplefilter("ignore")


if __name__ == "__main__":
    ALLOWED_EXTENSIONS = set(["wav", "mp3", "ogg", "webm"])
    parser = argparse.ArgumentParser(description="RT Remote transcription")
    parser.add_argument(
        "--audio-dir", help="Dir to audio files to predict on, the same in mic script"
    )
    parser.add_argument("--transcription", help="Transcription file")
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
    while True:
        try:
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
                try:
                    response = (
                        subprocess.check_output(
                            'curl -X POST http://52.250.111.102:8888/transcribe -H "Content-type: multipart/form-data" -F "file=@'
                            + audio_path
                            + '"'
                        )
                    )
                except:
                    print("Please Start the server")
                    time.sleep(60)
                response = json.loads(response.decode("utf-8", "ignore"))
                
                if response["status"] is "error":
                    print(response["message"])
                    continue
                else:
                    transcription = response["transcription"][0][0]

                print(transcription)
                line = audio_file.split(".")[0] + " --> " + transcription + "\n"
                with open(args.transcription, "a") as the_file:
                    the_file.write(line)
                os.remove(audio_path)
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
