


class TextProcessor:



    @staticmethod
    def remove_word_dividers(text):
        return text.translate(str.maketrans("\t\r\n", "   "))


    @staticmethod
    def remove_el_intonations(text):
        return text.translate(str.maketrans("άέήίόύώϊΐϋΰ", "αεηιουωιιυυ"))

    @staticmethod
    def remove_numbers(text):
        return text.translate(str.maketrans("0123456789", "          "))


    @staticmethod
    def remove_symbols(text):
        return text.translate(str.maketrans("&*@\^\"%+-=#$|_~", "               "))


    @staticmethod
    def remove_punctuations(text):
        return text.translate(str.maketrans("’'[](){}⟨⟩:,،、‒-–.…!<>«»-?‘’“”'\";/⁄`", "                                    "))


    @staticmethod
    def remove_english(text):
        return text.translate(str.maketrans("abcdefghijklmnopqrstuvwxyz", "                          "))

