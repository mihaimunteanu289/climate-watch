# Function to lemmatize a text
def lemmatize_text(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc])

# Lemmatize the 'article_text' column
df['article_text_lemma'] = df['article_text'].apply(lemmatize_text)
regions_lemma = [lemmatize_text(i) for i in regions]
counties_lemma = [lemmatize_text(i) for i in counties]

# Function to stem text
def stem_text(text):
    return " ".join(stemmer.stem(word) for word in text.split())

# Stem the 'article_text' column
df['article_text_stem'] = df['article_text'].apply(stem_text)
regions_stem = [stem_text(i) for i in regions]
counties_stem = [stem_text(i) for i in counties]