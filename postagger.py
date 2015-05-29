import nltk


# This a Parts of Speech Tagger which tags every single word(stem) in sentence
class POSTagger(object):
    def __init__(self):
        # self.wnl = nltk.WordNetLemmatizer()
        self.stemmer = nltk.PorterStemmer()

    def pos_tag(self, sentences):
        """
        input format: list of lists of words
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        output format: list of lists of tagged tokens. Each tagged tokens has a
        stem and a list of tags
            e.g: [[('this', ['DT']), ('be', ['VB']), ('a', ['DT']), ('sentence', ['NN'])],
        """

        pos = [nltk.pos_tag(sentence) for sentence in sentences]

        pos = [[(self.stemmer.stem(word), [postag]) for (word, postag) in sentence] for sentence in pos]
        return pos
