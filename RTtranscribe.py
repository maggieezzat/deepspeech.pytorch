import argparse
import warnings

from opts import add_decoder_args, add_inference_args
from utils import load_model

warnings.simplefilter("ignore")

from decoder import GreedyDecoder

import torch

from data.data_loader import SpectrogramParser
from model import DeepSpeech
import os.path
import json
from transcribe import transcribe, decode_results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DeepSpeech transcription")
    parser = add_inference_args(parser)
    parser.add_argument(
        "--audio-path", default="audio.wav", help="Audio files to predict on"
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

    audio_files = (args.audio_path).split(",")
    print("Starting")
    for af in audio_files:
        decoded_output, decoded_offsets = transcribe(af, parser, model, decoder, device)
        print(json.dumps(decode_results(model, decoded_output, decoded_offsets)))
