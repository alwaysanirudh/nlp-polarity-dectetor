import json
from splitter import Splitter
from postagger import POSTagger
from dicttagger import DictionaryTagger

global dicttagger


def value_of(tag):
    if tag == 'positive':
        return 1

    if tag == 'negative':
        return -1
    return 0


# Calculate the score for an single sentence
def sentence_score(sentence_tokens, previous_token, total_score):

    if not sentence_tokens:
        return total_score
    else:
        current_token = sentence_tokens[0]

        tags = current_token[1]
        token_score = sum([value_of(tag) for tag in tags])
        if previous_token is not None:
            previous_tags = previous_token[1]
            if 'inc' in previous_tags:
                token_score *= 2.0
            elif 'dec' in previous_tags:
                token_score /= 2.0
            elif 'inv' in previous_tags:
                token_score *= -1.0
        return sentence_score(sentence_tokens[1:], current_token, total_score + token_score)


# Calucate the score for a input paragraph
def sum_score(sentences):
    return sum([sentence_score(sentence, None, 0.0) for sentence in sentences])


# Do all the text processing and return its polarity
def process_text(text):
        splitter = Splitter()
        postagger = POSTagger()

        # Split the sentences to words
        splitted_sentences = splitter.split(text)

        # Do Parts of Speech Tagging on the words
        pos_tagged_sentences = postagger.pos_tag(splitted_sentences)

        dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
        return sum_score(dict_tagged_sentences)


if __name__ == '__main__':
        # Create  an object of the Dict tagger
        dicttagger = DictionaryTagger(['data/positive.yml', 'data/negative.yml', 'data/inc.yml', 'data/dec.yml', 'data/inv.yml'])

        # # Load the testing json file
        # with open('data/test.json') as data_file:
        #     data = json.load(data_file)

        # # Interate over the texts print the output
        # for test in data:
        #     print 'Input: ' + test['text']
        #     print 'Actualy Polarity: ' + test['label']
        #     print 'Calculated Polarity: ' + process_text(test['text'])

        text = raw_input("Enter something: ")
        print 'Calculated Polarity: ' + str(process_text(text))
