# coding=utf-8

in_file = '/speech/epoch13_transcriptions/greedy_ep13_test_transcriptions.csv'
#in_file = '/Users/MaggieEzzat/Desktop/greedy_ep13_test_transcriptions.csv'
out_file = '/speech/epoch13_transcriptions/greedy_ep13_test_input_to_transformer.txt'
#out_file = '/Users/MaggieEzzat/Desktop/greedy_ep13_test_input_to_transformer.txt'

with open(in_file, 'r') as in_f:
    content=in_f.readlines()
    with open(out_file, 'w') as out_f:
        for item in content:
            item = item.split(",")
            out_f.write(item[1]+ '\n')
