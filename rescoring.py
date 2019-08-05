import kenlm


def rescore_sent(utterances, no_paths=100, rescoring_lm="/lm_corpus/mt_sixgram.binary"):
    """
    takes as an input the output sentences from the beam search lm and scores them with a bigger lm
    to return the most probable one
    """
    rescoring_results = [[] for j in range(len(utterances))]
    model = kenlm.LanguageModel(rescoring_lm)
    for utterance in range(len(utterances)):
        maxScore = float("-inf")
        maxIndex = -1
        for i in range(min(no_paths, len(utterances[utterance]))):
            score = model.score(utterances[utterance][i])
            if score > maxScore:
                maxScore = score
                maxIndex = i
        rescoring_results[utterance].append(utterances[utterance][maxIndex])

    return rescoring_results
