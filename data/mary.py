from clean_text import clean_sentence


with open("/lm_corpus/German_sentences_8mil_filtered_maryfied.txt", "r") as text:
    with open("/lm_corpus/mary.txt","w") as out_file:
            for line in text:
                sent = clean_sentence(line)
                out_file.write(sent+"\n")

