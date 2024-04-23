from sklearn.feature_extraction.text import TfidfVectorizer

corpus = [ " the martian has landed on the latin pop sensation ricky martin",
           " discover new scientific insights from the Mars rover expedition" ]

vectorizer = TfidfVectorizer(stop_words='english')
#tokens = vectorizer.get_feature_names_out()
x = vectorizer.fit_transform(corpus)
#print(tokens)
print(x.toarray()[0])

