import csv
import Levenshtein as Lev
from data.clean_text import clean_sentence


def werC(s1, s2):
    """
    Computes the Word Error Rate, defined as the edit distance between the
    two provided sentences after tokenizing to words.
    Arguments:
        s1 (string): space-separated sentence
        s2 (string): space-separated sentence
    """

    # build mapping of words to integers
    b = set(s1.split() + s2.split())
    word2char = dict(zip(b, range(len(b))))

    # map the words to a char array (Levenshtein packages only accepts
    # strings)
    w1 = [chr(word2char[w]) for w in s1.split()]
    w2 = [chr(word2char[w]) for w in s2.split()]

    return Lev.distance("".join(w1), "".join(w2))


def cerC(s1, s2):
    """
    Computes the Character Error Rate, defined as the edit distance.

    Arguments:
        s1 (string): space-separated sentence
        s2 (string): space-separated sentence
    """
    s1, s2, = s1.replace(" ", ""), s2.replace(" ", "")
    return Lev.distance(s1, s2)


def compare(transcripts, references):
    """
    Inputs : arrays of transcriptions and references to compare
    """
    total_wer = 0
    total_cer = 0
    num_tokens = 0
    num_chars = 0
    for x in range(len(references)):
        transcript, reference = transcripts[x], references[x]
        wer_inst = werC(transcript, reference)
        cer_inst = cerC(transcript, reference)
        total_wer += wer_inst
        total_cer += cer_inst
        num_tokens += len(reference.split())
        num_chars += len(reference)

    wer = float(total_wer) / num_tokens
    cer = float(total_cer) / num_chars

    return (wer, cer)

    ## TODO remove <UNK>
    ## TODO clean sentence


test = {}
with open("/home/GPUAdmin1/asr/test.csv", encoding="utf-8-sig") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    for row in csv_reader:
        test[row[0]] = row[1]

transcripts = []
transcribed_paths = []
references = []

with open("/speech/kaldi_transcriptions.txt", "r", encoding="utf-8-sig") as txt:
    for line in txt:
        split = line.split("\t", 1)
        split[1] = split[1].replace("<UNK>", "")
        transcripts.append(clean_sentence(split[1]))
        transcribed_paths.append(split[0])
        references.append(test[split[0]])

if len(transcripts) != len(references):
    print("NOT ALL DATA IS TRANSCRIBED")
    with open("/speech/missing.txt", "a") as f:
        for key in test:
            if key not in transcribed_paths:
                f.write(key + "\n")

    print("missing wav files found in /speech/missing.txt")


else:
    print(compare(transcripts, references))

