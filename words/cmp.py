file1 = "Ielts.csv"
file2 = "toefl_list.txt"
sets = set()
with open(file1,'r') as f:
    for line in f:
        word = line.rstrip('\r\n ')
        sets.add(word)

counter = 0
with open(file2,'r') as f:
    for line in f:
        word = line.rstrip('\r\n ')
        if word not in sets:
            print(word)
            counter = counter + 1
            sets.add(word)
print(counter)



