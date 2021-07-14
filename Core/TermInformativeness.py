import math



class TermInformativeness:


    @staticmethod
    def normalised_idf(NDoc, Dk):
        return math.log10( ((NDoc - Dk) + 0.5) / (Dk + 0.5) )





