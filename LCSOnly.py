from helper import read
from LCS import lcs

if __name__ == "__main__":
    with open("query.txt", encoding='utf8') as a:
        query = a.read()
        
    sentences = read("./data")
    sentences = [word for word in list(set(sentences)) if type(word) is str]
    # for i in range (len(sentences)):
    #     print("[sentence %d is %s]" % (i,sentences[i]))

    similarity=0
    mostSimilar=-1
    print(len(sentences))
    for i in range(0,len(sentences)-1):
        similarContent = sentences[i]
        cSimilar = lcs(query,similarContent)
        if similarity < cSimilar:
            similarity=cSimilar
            mostSimilar = i
            print('most similar',i)
    
    print(sentences[mostSimilar])
