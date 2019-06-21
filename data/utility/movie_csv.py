# from pydub import AudioSegment
import os
import re
import string

# =================== functions ===================


def getms(time):
    time = time.split(":")
    ms = int(time[0]) * 3600000
    ms += int(time[1]) * 60000
    seconds = time[2].split(",")
    ms += int(seconds[0]) * 1000
    ms += int(seconds[1])
    return ms


def clean(string, start, end=None):
    # future work : take a list of start and end to call just once
    # the start and the end char are the same z.B : '♪'
    if end == None:
        end = start
    tmp = string.split(start, 1)
    out = tmp[0]
    tmp = tmp[1].split(end, 1)
    # if there is more than one occurance 
    if start in tmp[1] and end in tmp[1]:
        out += clean(tmp[1], start, end)
    else:
        out += tmp[1]
    return out


# =================== Vocab ===================

#   Number patterns
int_pattern = re.compile(r"[0-9]+")
float_pattern = re.compile(r"[0-9]+[,\.][0-9]+")

#   Allowed characters a-zA-Z'äüö
allowed = list(string.ascii_lowercase)
allowed.append("'")
allowed.append(" ")
allowed.extend(list("äöü"))

#   Replacement characters
replacer = {
    "àáâãåāăąǟǡǻȁȃȧ": "a",
    "æǣǽ": "ä",
    "çćĉċč": "c",
    "ďđ": "d",
    "èéêëēĕėęěȅȇȩε": "e",
    "ĝğġģǥǧǵ": "g",
    "ĥħȟ": "h",
    "ìíîïĩīĭįıȉȋ": "i",
    "ĵǰ": "j",
    "ķĸǩǩκ": "k",
    "ĺļľŀł": "l",
    "м": "m",
    "ñńņňŉŋǹ": "n",
    "òóôõøōŏőǫǭǿȍȏðο": "o",
    "œ": "ö",
    "ŕŗřȑȓ": "r",
    "śŝşšș": "s",
    "ţťŧț": "t",
    "ùúûũūŭůűųȕȗ": "u",
    "ŵ": "w",
    "ýÿŷ": "y",
    "źżžȥ": "z",
    "ß": "ss",
    "-­": " ",
}

#   Various replacement rules
special_replacers = {
    " $ ": "dollar",
    " £ ": "pfund",
    "m³": "kubikmeter",
    "km²": "quadratkilometer",
    "m²": "quadratmeter",
}

replacements = {}
replacements.update(special_replacers)

for all, replacement in replacer.items():
    for to_replace in all:
        replacements[to_replace] = replacement


def clean_sentence(sentence):
    """
    Clean the given sentence.
    1. split into words by spaces
    2. numbers to words
    3. character/rule replacements
    4. delete disallowed symbols
    4. join with spaces
    """

    def clean_word(word):
        """
        Clean the given word.
        1. numbers to words
        2. character/rule replacements
        3. delete disallowed symbols
        """

        def replace_symbols(word):
            """ Apply all replacement characters/rules to the given word. """
            result = word

            for to_replace, replacement in replacements.items():
                result = result.replace(to_replace, replacement)

            return result

        def remove_symbols(word):
            """ Remove all symbols that are not allowed. """
            result = word
            bad_characters = []

            for c in result:
                if c not in allowed:
                    bad_characters.append(c)

            for c in bad_characters:
                result = result.replace(c, "")

            return result

        def word_to_num(word):
            """ Replace numbers with their written representation. """
            result = word

            match = float_pattern.search(result)

            while match is not None:
                num_word = num2words.num2words(
                    float(match.group().replace(",", ".")), lang="de"
                ).lower()
                before = result[: match.start()]
                after = result[match.end() :]
                result = " ".join([before, num_word, after])
                match = float_pattern.search(result)

            match = int_pattern.search(result)

            while match is not None:
                num_word = num2words.num2words(int(match.group()), lang="de")
                before = result[: match.start()]
                after = result[match.end() :]
                result = " ".join([before, num_word, after])
                match = int_pattern.search(result)

            return result

        def get_bad_character(text):
            """ Return all characters in the text that are not allowed. """
            bad_characters = set()

            for c in text:
                if c not in allowed:
                    bad_characters.add(c)

            return bad_characters

        word = word.lower()
        word = word_to_num(word)
        word = replace_symbols(word)
        word = remove_symbols(word)

        bad_chars = get_bad_character(word)

        if len(bad_chars) > 0:
            print('Bad characters in "{}"'.format(word))
            print("--> {}".format(", ".join(bad_chars)))

        return word

    words = sentence.strip().split(" ")
    cleaned_words = []

    for word in words:
        cleaned_word = clean_word(word)
        cleaned_words.append(cleaned_word)

    return " ".join(cleaned_words)


# =================== Main ===================
directory = "D:/Freitags/dark/Dark"
output_file = "D:/Freitags/dark/dark.csv"
transcript_dir = os.path.join(directory, "Transcript")
audio_dir = os.path.join(directory, "Audio")
csv = []
# loop over all transcription files and create csv
for file in os.listdir(transcript_dir):
    with open(os.path.join(transcript_dir, file), "r", encoding="utf-8") as f:
        lines = f.readlines()
    lines = [l.strip() for l in lines]
    sequences = []
    tmp = []
    # sequences is list of each transcript for a wav segment
    for line in lines:
        if line == "":
            sequences.append(tmp)
            tmp = []
        else:
            tmp.append(line)
    # process the transcription
    for s in sequences:
        number = s[0].strip()
        filename = file + "_" + number
        time = s[1]
        time = time.split(" ")
        timefrom = getms(time[0])
        timeto = getms(time[-1])
        transcriptl = s[2:]
        transcript = ""
        for t in transcriptl:
            transcript += t + " "
        print(transcript)
        # --TODO remove things between [] and ♪
        if "[" in transcript and "]" in transcript:
            transcript = clean(transcript, "[", "]")
        if "♪" in transcript:
            transcript = clean(transcript, "♪")
        transcriptclean = clean_sentence(transcript)
        # --TODO if the whole wav is non talk igneore it i.e continue
        if (
            transcriptclean.strip() == ""
            or transcriptclean.strip() == "netflix präsentiert"
        ):
            print("====Empty====")
            continue
        print(transcriptclean)
        # TODO segment the wav file and put it in the csv
        wav_file_dir = number + ""
        csv.append((wav_file_dir, transcriptclean))

        break
"""

with open(output_file, "w") as f:
    for line in csv:
        f.write(line[0] + "," + line[1] + "\n")
"""

"""
lines = [l.strip() for l in lines]



t_line = lines[0]
t_line = t_line.split(' ')
old_file = t_line[1]
new_file = t_line[0]
t1 = float(t_line[2])
t2 = float(t_line[3])
#t1 = 1038
#t2 = 1042


newAudio = AudioSegment.from_wav( old_file +".wav")
newAudio = newAudio[t1:t2]
newAudio.export(new_file + '.wav', format="wav")
"""
