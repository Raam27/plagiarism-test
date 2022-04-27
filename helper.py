import os
    
def read(path):
    filelist = os.listdir(path)
    sentences = []
    for i in filelist:
        if i.endswith(".go"):  # You could also add "and i.startswith('f')
            with open(path + i, 'r') as f:
                # print(f.read())
                sentence = f.read()
                # print(sentence)
                sentences.append(sentence)
    return sentences