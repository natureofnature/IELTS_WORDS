from PyDictionary import PyDictionary
dictionary=PyDictionary()
write_to = 'full.txt'
with open('Ielts.csv','r') as f:
    with open(write_to,'w') as wf:
        for line in f:
            word = line.rstrip('\r\n')
            meaning = dictionary.meaning(word)
            wf.write(word+"`"+str(meaning)+'\n')
            print(word,meaning)
            wf.flush()
            
