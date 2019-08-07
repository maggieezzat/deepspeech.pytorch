def add_decoder_args(parser):
    beam_args = parser.add_argument_group("Beam Decode Options",
                                          "Configurations options for the CTC Beam Search decoder")
    beam_args.add_argument('--top-paths', default=1, type=int, help='number of beams to return')
    beam_args.add_argument('--beam-width', default=10, type=int, help='Beam width to use')
    beam_args.add_argument('--lm-path', default=None, type=str,
                           help='Path to an (optional) kenlm language model for use with beam search (req\'d with trie)')
    beam_args.add_argument('--alpha', default=0.8, type=float, help='Language model weight')
    beam_args.add_argument('--beta', default=1, type=float, help='Language model word bonus (all words)')
    beam_args.add_argument('--cutoff-top-n', default=40, type=int,
                           help='Cutoff number in pruning, only top cutoff_top_n characters with highest probs in '
                                'vocabulary will be used in beam search, default 40.')
    beam_args.add_argument('--cutoff-prob', default=1.0, type=float,
                           help='Cutoff probability in pruning,default 1.0, no pruning.')
    beam_args.add_argument('--lm-workers', default=1, type=int, help='Number of LM processes to use')
    beam_args.add_argument('--rescore', dest='rescore', action='store_true', help='Use language model rescoring')
    beam_args.add_argument('--rescore-lm',default = "/lm_corpus/all_4gram.binary", dest='rescore_lm',type =str, help='Language model path used for rescoring')
    return parser


def add_inference_args(parser):
    parser.add_argument('--cuda', action="store_true", help='Use cuda to test model')
    parser.add_argument('--decoder', default="greedy", choices=["greedy", "beam"], type=str, help="Decoder to use")
    parser.add_argument('--model-path', default='models/deepspeech_final.pth',
                        help='Path to model file created by training')
    return parser


def add_training_args(parser):
    parser.add_argument('--train-manifest', metavar='DIR',
                    help='path to train manifest csv', default='data/train_manifest.csv')
    parser.add_argument('--val-manifest', metavar='DIR',
                        help='path to validation manifest csv', default='data/val_manifest.csv')
    parser.add_argument('--sample-rate', default=16000, type=int, help='Sample rate')
    parser.add_argument('--batch-size', default=20, type=int, help='Batch size for training')
    parser.add_argument('--num-workers', default=4, type=int, help='Number of workers used in data-loading')
    parser.add_argument('--labels-path', default='labels.json', help='Contains all characters for transcription')
    parser.add_argument('--window-size', default=.02, type=float, help='Window size for spectrogram in seconds')
    parser.add_argument('--window-stride', default=.01, type=float, help='Window stride for spectrogram in seconds')
    parser.add_argument('--window', default='hamming', help='Window type for spectrogram generation')
    parser.add_argument('--hidden-size', default=800, type=int, help='Hidden size of RNNs')
    parser.add_argument('--hidden-layers', default=5, type=int, help='Number of RNN layers')
    parser.add_argument('--rnn-type', default='gru', help='Type of the RNN. rnn|gru|lstm are supported')
    parser.add_argument('--epochs', default=70, type=int, help='Number of training epochs')
    parser.add_argument('--cuda', dest='cuda', action='store_true', help='Use cuda to train model')
    parser.add_argument('--lr', '--learning-rate', default=3e-4, type=float, help='initial learning rate')
    parser.add_argument('--momentum', default=0.9, type=float, help='momentum')
    parser.add_argument('--max-norm', default=400, type=int, help='Norm cutoff to prevent explosion of gradients')
    parser.add_argument('--learning-anneal', default=1.1, type=float, help='Annealing applied to learning rate every epoch')
    parser.add_argument('--silent', dest='silent', action='store_true', help='Turn off progress tracking per iteration')
    parser.add_argument('--checkpoint', dest='checkpoint', action='store_true', help='Enables checkpoint saving of model')
    parser.add_argument('--checkpoint-per-batch', default=0, type=int, help='Save checkpoint per batch. 0 means never save')
    parser.add_argument('--visdom', dest='visdom', action='store_true', help='Turn on visdom graphing')
    parser.add_argument('--tensorboard', dest='tensorboard', action='store_true', help='Turn on tensorboard graphing')
    parser.add_argument('--log-dir', default='visualize/deepspeech_final', help='Location of tensorboard log')
    parser.add_argument('--log-params', dest='log_params', action='store_true', help='Log parameter values and gradients')
    parser.add_argument('--id', default='Deepspeech training', help='Identifier for visdom/tensorboard run')
    parser.add_argument('--save-folder', default='models/', help='Location to save epoch models')
    parser.add_argument('--model-path', default='models/deepspeech_final.pth',
                        help='Location to save best validation model')
    parser.add_argument('--continue-from', default='', help='Continue from checkpoint model')
    parser.add_argument('--finetune', dest='finetune', action='store_true',
                        help='Finetune the model from checkpoint "continue_from"')
    parser.add_argument('--augment', dest='augment', action='store_true', help='Use random tempo and gain perturbations.')
    parser.add_argument('--noise-dir', default=None,
                        help='Directory to inject noise into audio. If default, noise Inject not added')
    parser.add_argument('--noise-prob', default=0.4, help='Probability of noise being added per sample')
    parser.add_argument('--noise-min', default=0.0,
                        help='Minimum noise level to sample from. (1.0 means all noise, not original signal)', type=float)
    parser.add_argument('--noise-max', default=0.5,
                        help='Maximum noise levels to sample from. Maximum 1.0', type=float)
    parser.add_argument('--no-shuffle', dest='no_shuffle', action='store_true',
                        help='Turn off shuffling and sample from dataset based on sequence length (smallest to largest)')
    parser.add_argument('--no-sortaGrad', dest='no_sorta_grad', action='store_true',
                        help='Turn off ordering of dataset on sequence length for the first epoch.')
    parser.add_argument('--no-bidirectional', dest='bidirectional', action='store_false', default=True,
                        help='Turn off bi-directional RNNs, introduces lookahead convolution')
    parser.add_argument('--dist-url', default='tcp://127.0.0.1:1550', type=str,
                        help='url used to set up distributed training')
    parser.add_argument('--dist-backend', default='nccl', type=str, help='distributed backend')
    parser.add_argument('--world-size', default=1, type=int,
                        help='number of distributed processes')
    parser.add_argument('--rank', default=0, type=int,
                        help='The rank of this process')
    parser.add_argument('--gpu-rank', default=None,
                        help='If using distributed parallel for multi-gpu, sets the GPU for the process')
    parser.add_argument('--seed', default=123456, type=int, help='Seed to generators')
    parser.add_argument('--mixed-precision', action='store_true',
                        help='Uses mixed precision to train a model (suggested with volta and above)')
    parser.add_argument('--static-loss-scale', type=float, default=1,
                        help='Static loss scale for mixed precision, ' +
                            'positive power of 2 values can improve FP16 convergence,' +
                            'however dynamic loss scaling is preferred.')
    parser.add_argument('--dynamic-loss-scale', action='store_true',
                        help='Use dynamic loss scaling for mixed precision. If supplied, this argument supersedes ' +
                            '--static_loss_scale. Suggested to turn on for mixed precision')