import chardet


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        confidence = result['confidence']
        return encoding, confidence


file_path = 'scrapper\heading.txt'
my_encoding, confidence = detect_encoding(file_path)

with open('scrapper\heading.txt', 'r', encoding=my_encoding) as f:
    lines = f.readlines()

file_path = 'scrapper\link.txt'
my_encoding, confidence = detect_encoding(file_path)

with open('scrapper\link.txt', 'r', encoding=my_encoding) as f:
    links = f.readlines()


link_l = []
for index, line in enumerate(links):
    tokens = line.strip()
    link_l.append(tokens)


def preprocess(document_text):
    terms = [term.lower() for term in document_text.strip().split()[1:]]
    return terms


vocab = {}
documents = []
for index, line in enumerate(lines):
    tokens = preprocess(line)
    documents.append(preprocess(line))
    tokens = set(tokens)
    for token in tokens:
        if token not in vocab:
            vocab[token] = 1
        else:
            vocab[token] += 1

vocab = dict(sorted(vocab.items(), key=lambda item: item[1], reverse=True))

print('Number of documents: ', len(documents))
print('Size of vocab: ', len(vocab))
print('Sample document: ', documents[0])

with open('Search engine\\TF-IDF\\vocab.txt', 'w') as f:
    for key in vocab.keys():
        f.write("%s\n" % key)

with open('Search engine\TF-IDF\idf-values.txt', 'w') as f:
    for key in vocab.keys():
        f.write("%s\n" % vocab[key])

with open('Search engine\TF-IDF\documents.txt', 'w') as f:
    for document in (documents):
        f.write("%s\n" % ' '.join(document))

with open('Search engine\TF-IDF\links.txt', 'w') as f:
    for document in (link_l):
        f.write("%s\n" % document)

inverted_index = {}
for index, document in enumerate(documents):
    for token in document:
        if token not in inverted_index:
            inverted_index[token] = [index]
        else:
            inverted_index[token].append(index)

with open('Search engine\TF-IDF\inverted_index.txt', 'w') as f:
    for key in inverted_index.keys():
        f.write("%s\n" % key)
        f.write("%s\n" % ' '.join([str(doc_id)
                for doc_id in inverted_index[key]]))
