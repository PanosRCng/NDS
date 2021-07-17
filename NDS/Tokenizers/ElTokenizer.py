from NDS.Tokenizers.Tokenizer import Tokenizer
from Core.TextProcessor import TextProcessor




class ElTokenizer(Tokenizer):


    def tokenize(self, text, tokens_min_length=None):

        cl_text = text.lower()
        cl_text = TextProcessor.remove_english(cl_text)
        cl_text = TextProcessor.remove_punctuations(cl_text)
        cl_text = TextProcessor.remove_symbols(cl_text)
        cl_text = TextProcessor.remove_el_intonations(cl_text)
        cl_text = TextProcessor.remove_numbers(cl_text)
        cl_text = TextProcessor.remove_word_dividers(cl_text)

        return self.tokens(cl_text, tokens_min_length)


    def tokens(self, text, tokens_min_length=None):

        tokens = [token.strip() for token in text.split(' ') if token != '']

        if tokens_min_length is not None:
            return [token for token in tokens if len(token) >= tokens_min_length]

        return tokens


