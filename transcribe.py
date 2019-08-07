import argparse
import warnings

from opts import add_decoder_args, add_inference_args
from utils import load_model

warnings.simplefilter('ignore')

from decoder import GreedyDecoder

import torch

from data.data_loader import SpectrogramParser
from model import DeepSpeech
import os.path
import json


def decode_results(model, decoded_output, decoded_offsets):
    results = {
        "output": [],
        "_meta": {
            "acoustic_model": {
                "name": os.path.basename(args.model_path)
            },
            "language_model": {
                "name": os.path.basename(args.lm_path) if args.lm_path else None,
            },
            "decoder": {
                "lm": args.lm_path is not None,
                "alpha": args.alpha if args.lm_path is not None else None,
                "beta": args.beta if args.lm_path is not None else None,
                "type": args.decoder,
            }
        }
    }

    for b in range(len(decoded_output)):
        for pi in range(min(args.top_paths, len(decoded_output[b]))):
            result = {'transcription': decoded_output[b][pi]}
            if args.offsets:
                result['offsets'] = decoded_offsets[b][pi].tolist()
            results['output'].append(result)
    return results


def transcribe(audio_path, parser, model, decoder, device):
    spect = parser.parse_audio(audio_path).contiguous()
    spect = spect.view(1, 1, spect.size(0), spect.size(1))
    spect = spect.to(device)
    input_sizes = torch.IntTensor([spect.size(3)]).int()
    out, output_sizes = model(spect, input_sizes)
    decoded_output, decoded_offsets = decoder.decode(out, output_sizes)
    return decoded_output, decoded_offsets


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DeepSpeech transcription')
    parser = add_inference_args(parser)
    parser.add_argument('--audio-path', default='audio.wav',
                        help='Audio file to predict on')
    parser.add_argument('--offsets', dest='offsets', action='store_true', help='Returns time offset information')
    
    parser.add_argument('--auto-correct', default=False,
                        help='Use transformer auto correction on decoded output')
    
    parser = add_decoder_args(parser)
    args = parser.parse_args()
    device = torch.device("cuda" if args.cuda else "cpu")
    model = load_model(device, args.model_path, args.cuda)

    print(args.auto_correct)

    if args.decoder == "beam":
        from decoder import BeamCTCDecoder

        decoder = BeamCTCDecoder(model.labels, lm_path=args.lm_path, alpha=args.alpha, beta=args.beta,
                                 cutoff_top_n=args.cutoff_top_n, cutoff_prob=args.cutoff_prob,
                                 beam_width=args.beam_width, num_processes=args.lm_workers)
    else:
        decoder = GreedyDecoder(model.labels, blank_index=model.labels.index('_'))

    parser = SpectrogramParser(model.audio_conf, normalize=True)

    decoded_output, decoded_offsets = transcribe(args.audio_path, parser, model, decoder, device)

    if args.auto_correct == True:
        print("hello")
        from tensor2tensor.bin import t2t_decoder
        
        out_file = '/data/home/GPUAdmin1/asr/greedy_decoder_output.txt' 
        with open(out_file, 'w') as f:
            f.write(decoded_output)
        
        t2t_decoder.main(data_dir="/data/home/GPUAdmin1/t2t_data",
        problem="asr_correction",
        model="transformer",
        hparams_set="transformer_big",
        output_dir="/data/home/GPUAdmin1/t2t_train/asr_correction",
        decode_hparams="beam_size=4,alpha=0.6",
        decode_from_file=out_file,
        decode_to_file="/data/home/GPUAdmin1/asr/transformer_decoder_output.txt",
        t2t_usr_dir="/data/home/GPUAdmin1/asr/deepspeech.pytorch/transformer/")

        print("hi")


    print(json.dumps(decode_results(model, decoded_output, decoded_offsets)))
