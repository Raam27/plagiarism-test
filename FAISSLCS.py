from sentence_transformers import SentenceTransformer
import faiss
from helper import read
from LCS import lcs

def findMostSimilar(query,arr):
    similarity=0
    mostSimilar=-1
    # print(arr)
    for i in (arr):
        similarContent = sentences[i]
        currentSimilarity = lcs(query,similarContent)
        print(currentSimilarity)
        if similarity < currentSimilarity:
            similarity=currentSimilarity
            mostSimilar = i
            print('most similar',mostSimilar)
            print('similarity rate(similarity/len(theSimilarContent)): %d/%d'%(similarity,len(similarContent)))
            similarityPercentage = float(similarity/len(similarContent))
            print("{:.2%}".format(similarityPercentage))

            print('similarity rate(similarity/len(query)): %d/%d'%(similarity,len(query)))
            similarityPercentage = float(similarity/len(query))
            print("{:.2%}".format(similarityPercentage))

            print("[ %s ]" % sentences[mostSimilar])   

if __name__ == "__main__":
    with open("query.txt", encoding='utf8') as a:
        query = a.read()

    sentences = read("./data/")
    
    # remove duplicates and NaN
    sentences = [word for word in list(set(sentences)) if type(word) is str]

    model = SentenceTransformer('bert-base-nli-mean-tokens')

    # transform to vector
    sentence_embeddings = model.encode(sentences)

    d = sentence_embeddings.shape[1]

    index = faiss.IndexFlatL2(d)
    faiss.normalize_L2(sentence_embeddings)
    index.add(sentence_embeddings)
    
    k=2
    xq = model.encode([query])
    faiss.normalize_L2(xq)

    # get k nearest neighbor
    D, I = index.search(xq,k)
    
    # check similarity for query and k most similar data with LCS
    findMostSimilar(query,I[0])
    faissPercentage = 25 * (4-D)
    print('faiss percentage = ', faissPercentage)
