from Stopwords import Stopwords



def main():

    test = 'γενικα στη βιολογια αεροβιος χαρακτηριζεται τυπικα οποιοσδηποτε μικροοργανισμος η πολυκυτταρος οργανισμος που ειναι ικανος για μεταβολισμο μονο με την παρουσια οξυγονου δηλαδη που λαμβανει ελευθερο μοριο οξυγονου που απαιτειται για αεροβικη αναπνοη αεροβιοι οργανισμοι ειναι σχεδον ολοι οι πολυκυτταροι οργανισμοι οπως ζωα και φυτα με εξαιρεση καποια κατωτερης μορφης παρασιτων τα ενδοπαρασιτα'

    print(test.split(' '))
    print('\n')
    print([token for token in test.split(' ') if token not in Stopwords.get('el')])






if __name__ == '__main__':
    main()