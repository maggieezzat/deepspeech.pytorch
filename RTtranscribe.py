import argparse
import warnings

from opts import add_decoder_args, add_inference_args
from utils import load_model

warnings.simplefilter("ignore")

from decoder import GreedyDecoder

import torch

from data.data_loader import SpectrogramParser
from model import DeepSpeech
import os
import json
from transcribe import transcribe
import time


def decode_results(model, decoded_output, decoded_offsets):
    results = {
        "output": [],
        "_meta": {
            "acoustic_model": {"name": os.path.basename(args.model_path)},
            "language_model": {
                "name": os.path.basename(args.lm_path) if args.lm_path else None
            },
            "decoder": {
                "lm": args.lm_path is not None,
                "alpha": args.alpha if args.lm_path is not None else None,
                "beta": args.beta if args.lm_path is not None else None,
                "type": args.decoder,
            },
        },
    }

    for b in range(len(decoded_output)):
        for pi in range(min(args.top_paths, len(decoded_output[b]))):
            result = decoded_output[b][pi]
            if args.offsets:
                result["offsets"] = decoded_offsets[b][pi].tolist()
            results["output"].append(result)
    return results


if __name__ == "__main__":
    ALLOWED_EXTENSIONS = set(["wav", "mp3", "ogg", "webm"])
    parser = argparse.ArgumentParser(description="RT transcription")
    parser = add_inference_args(parser)
    parser.add_argument(
        "--audio-dir", default="/speech/test_RT", help="Audio files to predict on"
    )
    parser.add_argument(
        "--offsets",
        dest="offsets",
        action="store_true",
        help="Returns time offset information",
    )
    parser = add_decoder_args(parser)
    args = parser.parse_args()
    device = torch.device("cuda" if args.cuda else "cpu")
    model = load_model(device, args.model_path, args.cuda)

    if args.decoder == "beam":
        from decoder import BeamCTCDecoder

        decoder = BeamCTCDecoder(
            model.labels,
            lm_path=args.lm_path,
            alpha=args.alpha,
            beta=args.beta,
            cutoff_top_n=args.cutoff_top_n,
            cutoff_prob=args.cutoff_prob,
            beam_width=args.beam_width,
            num_processes=args.lm_workers,
        )
    else:
        decoder = GreedyDecoder(model.labels, blank_index=model.labels.index("_"))

    parser = SpectrogramParser(model.audio_conf, normalize=True)

    print("Starting")
    counter = 0
    s = "|"
    while True:
        audio_files = [
            f
            for f in os.listdir(args.audio_dir)
            if os.path.isfile(os.path.join(args.audio_dir, f))
            and ((f.split(".")[1]).lower() in ALLOWED_EXTENSIONS)
        ]
        if len(audio_files) > 0:
            audio_file = audio_files[0]
            audio_path = os.path.join(args.audio_dir, audio_file)
            try:
               testfile = open(audio_path, "r+")
            except IOError:
                print("Used")
            testfile.close()
            """
            size1 = os.path.getsize(audio_path)
            time.sleep(1)
            size2 = os.path.getsize(audio_path)
            if size1 != size2:
                continue
            """
            decoded_output, decoded_offsets = transcribe(
                audio_path, parser, model, decoder, device
            )
            transcription = decode_results(model, decoded_output, decoded_offsets)[
                "output"
            ][0]
            print(transcription)
            line = audio_file.split(".")[0] + " --> " + transcription + "\n"
            with open("/speech/transcriptions.txt", "a") as the_file:
                the_file.write(line)
            os.remove(audio_path)
            print()
        else:
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
