def clean(string, start, end):
    for i in range(0, len(start)):
        string = cleanh(string, start[i], end[i])
    return string

def cleanh(string, start, end):
    tmp = string.split(start, 1)
    out = tmp[0]
    tmp = tmp[1].split(end, 1)
    # if there is more than one occurance
    if start in tmp[1] and end in tmp[1]:
        out += cleanh(tmp[1], start, end)
    else:
        out += tmp[1]
    return out

transcript = "(Mann) <i>Ich wusste [immer,] dass der ♪Tag meiner♪ Abrechnung ♪kommt♪.</i>"
transcript = clean(transcript, ["<", "[", "(", "♪"], [">", "]", ")", "♪"])
print(transcript)

a = " Ich wusste  dass der  Abrechnung kommt."
print(a)