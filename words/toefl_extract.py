words = []
toefl_file = "toefl.txt"
with open(toefl_file,'r') as f:
    for line in f:
        entry = line.rstrip('\r\n').split('[')[0]
        print(entry)

