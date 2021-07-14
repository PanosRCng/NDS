from abc import ABC, abstractmethod
import importlib


class Tokenizer(ABC):

    @staticmethod
    def create(tokenizer_name):
        TokenizerModule = importlib.import_module('NDS.Tokenizers.' + tokenizer_name)
        TokenizerClass = getattr(TokenizerModule, tokenizer_name)

        return TokenizerClass()


    @abstractmethod
    def tokenize(self, text, tokens_min_length=None):
        pass


    @abstractmethod
    def tokens(self, text, tokens_min_length=None):
        pass


