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
