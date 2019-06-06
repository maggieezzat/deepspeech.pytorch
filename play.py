a = ("1", "one")
b = ("2", "two")
l = [a,b]

output_file = "/home/maggie/test.csv"

with open(output_file, 'w+') as f:
    for line in l:
        print(line)
        f.write(line[0]+","+line[1])
        print(line[0]+","+line[1])