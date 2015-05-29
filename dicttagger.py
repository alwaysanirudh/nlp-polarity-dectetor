import yaml


# This a Dictionary Tagger which tags every single word(stem) based on defined dictionaies
class DictionaryTagger(object):
    def __init__(self, dictionary_paths):
        # Open all the files and read
        files = [open(path, 'r') for path in dictionary_paths]
        dictionaries = [yaml.load(dict_file) for dict_file in files]

        # Close the files
        map(lambda x: x.close(), files)

        # Start The Dictionary building
        self.dictionary = {}
        self.max_key_size = 0
        for curr_dict in dictionaries:
            for key in curr_dict:
                if key in self.dictionary:
                    self.dictionary[key].extend(curr_dict[key])
                else:
                    self.dictionary[key] = curr_dict[key]
                    self.max_key_size = max(self.max_key_size, len(key))

    # Tag the POS tagged sentences based on dictionay
    def tag(self, postagged_sentences):
        return [self.tag_sentence(sentence) for sentence in postagged_sentences]

    # Tag a single sentence based on dictionary
    def tag_sentence(self, sentence):
        """
        the result is only one tagging of all the possible ones.
        The resulting tagging is determined by these two priority rules:
            - longest matches have higher priority
            - search is made from left to right
        """
        tag_sentence = []
        n = len(sentence)
        if self.max_key_size == 0:
            self.max_key_size = n
        i = 0
        while (i < n):
            j = min(i + self.max_key_size, n)   # avoid overflow
            tagged = False
            while (j > i):
                literal = ' '.join([word[0] for word in sentence[i:j]]).lower()

                if literal in self.dictionary:
                    is_single_token = j - i == 1
                    original_position = i
                    i = j
                    taggings = [tag for tag in self.dictionary[literal]]
                    tagged_expression = (literal, taggings)
                    if is_single_token:  # if the tagged literal is a single token, conserve its previous taggings:
                        original_token_tagging = sentence[original_position][1]
                        tagged_expression[1].extend(original_token_tagging)
                    tag_sentence.append(tagged_expression)
                    tagged = True
                else:
                    j = j - 1
            if not tagged:
                tag_sentence.append(sentence[i])
                i += 1
        return tag_sentence
