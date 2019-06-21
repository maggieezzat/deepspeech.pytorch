import os
import re
import csv
import string
import pandas
import random
import num2words
import collections



#VOCAB

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

#END VOCAB


rootdir = "/speech/de_DE"


csv_output = []
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
         if(".csv" in file and file.startswith("metadata")):
            file_dir = os.path.join(subdir, file)
            #Too many csvs we are short on memory
            #os.system("mv "+file_dir +" /data/home/GPUAdmin1/asr/M-AILABS/csvs/" + file)
            with open(file_dir) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='|')
                for row in csv_reader:
                    print("filename: " + row[0])
                    print("transcript: " + row[2])
                    filename = row[0]
                    transcript = row[2]
                    transcript = clean_sentence(transcript)
                    wav_file_dir = "/speech/M-AILABS/"+ filename +".wav"
                    if(os.path.exists(wav_file_dir)):
                        csv_output.append((wav_file_dir, transcript))
                    
df = pandas.DataFrame(data=csv_output)
output_file = "/speech/M-AILABS/M-AILABS_all.csv"
df.to_csv(output_file, index=False, sep=",")
random.shuffle(csv_output)
csv_test = csv_output[0:5901]
csv_train = csv_output[5901:]        
df = pandas.DataFrame(data=csv_train)
output_file = "/data/home/GPUAdmin1/asr/train_csvs/M-AILABS_train.csv"
df.to_csv(output_file, index=False, sep=",")
df = pandas.DataFrame(data=csv_test)
output_file = "/data/home/GPUAdmin1/asr/test_csvs/M-AILABS_test.csv"
df.to_csv(output_file, index=False, sep=",")


#create dict from csvs
"""
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if(file.endswith(".wav")):
            file_dir = os.path.join(subdir, file)
            os.system("mv "+file_dir +" /data/home/GPUAdmin1/asr/M-AILABS/" + file)
"""