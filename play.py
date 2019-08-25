#4 utterances
target_strings = [["1st most probleble for utt_1", "2nd most probable for utt_1", "3rd most probable for utt_1"],
                    ["1st most probleble for utt_2", "2nd most probable for utt_2", "3rd most probable for utt_2"],
                    ["1st most probleble for utt_3", "2nd most probable for utt_3", "3rd most probable for utt_3"],
                    ["1st most probleble for utt_4", "2nd most probable for utt_4", "3rd most probable for utt_4"]]


for x in range(len(target_strings)):
    print(x)
    print()
    reference = target_strings[x][0]
    if x==2:
        target_strings.remove(target_strings[x])


print(target_strings)